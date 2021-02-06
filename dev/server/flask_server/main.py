import os
import json
import secrets
import datetime
import string
import re
from datetime import timedelta
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from sqlalchemy import desc, and_
from sqlalchemy.sql import func
import numpy as np
import requests
#Authenticate function for JWT
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password, password):
        return user

#Identity function for JWT
def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=12) #Session time
db = SQLAlchemy(app)
jwt = JWT(app, authenticate, identity) #JWT Json Web Token to manage sessions, by default managed in /auth (POST request)
CORS(app)

#This must be declared after declaring db
from models import User, Supermarket, Waiting, Shopping, Record
from timetable import Timetable

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

#Register function to save users in the database, usernames(or emails) are unique
@cross_origin(origin='*')
@app.route('/register', methods=['POST'])
def register():
    try:
        print(request.json)    
        username = request.json.get('username')
        password = request.json.get('password')
        print(username, password)
        user = User(username, password)
        db.session.add(user) 
        db.session.commit()
        return {"message": f"user {user.username} has been created."}, 201
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

#Populate database with supermarkets from supermarkets.json, only used once while developing 
# @cross_origin(origin='*')
# @app.route('/supermarkets', methods=['GET'])
# def supermarket():
#     try:
#         f = open("data/supermarkets.json")
#         supermarkets_dict = json.loads(f.read())
#         for supermarket in supermarkets_dict:
#             name = supermarket["name"]
#             lat = supermarket["lat"]
#             lon = supermarket["lon"]
#             sp = Supermarket(name, lat, lon)
#             db.session.add(sp) 
#             db.session.commit()
#         return {"message": "supermarket have been created."}, 201
#     except Exception as ex:
#         print(ex)
#         return {"error": "Error"}, 400

#Retrieve all supermarkets (filter only in frontend)
@cross_origin(origin='*')
@app.route('/supermarkets_list', methods=['GET'])
def supermarkets_list():
    try:
        sp_list = Supermarket.query.all()
        json_list = []
        for supermarket in sp_list:
            current_timetable = Timetable(json_timetable=json.loads(supermarket.timetable))
            #if current_timetable.isAvailable():
            if True:
                sp = {
                    "name": supermarket.name,
                    "address" : supermarket.address,
                    "logo" : supermarket.logo,
                    "lat" : supermarket.lat,
                    "lon" : supermarket.lon,
                    "max_capacity" : supermarket.max_capacity,
                    "timetable" : supermarket.timetable,
                    "waiting_time" : supermarket.waiting_time,
                    "mean_shopping_time" : supermarket.mean_shopping_time,
                }
                json_list.append(sp)
        return {"supermarkets": json_list}
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

def averageTime(supermarket):
    delta_times = []
    records = Record.query.filter_by(supermarket_id=supermarket.id).all()
    for record in records:
        delta_times.append(record.delta_time)
    avg_time=np.mean(np.array(delta_times))
    records_count=len(records)
    if records_count>0:
        return avg_time
    else:
        return supermarket.mean_shopping_time*60

def isAvailable(supermarket_id):
    people_shopping=Shopping.query.filter_by(supermarket_id=supermarket_id).count()
    supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
    if people_shopping<supermarket.max_capacity:
        return True
    else:
        return False

@cross_origin(origin='*')
@app.route('/lineup', methods=['POST'])
def lineup():
    try:
        print(request.json)
        username = request.json.get('username')
        supermarket_id = request.json.get('supermarket_id')
        date_time = datetime.datetime.now()
        requests = Waiting.query.filter_by(username=username).count()
        requests += Shopping.query.filter_by(username=username).count()
        people_waiting=Waiting.query.filter_by(supermarket_id=supermarket_id).count()
        supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
        wait_time=int(people_waiting*averageTime(supermarket))+300
        if requests < 1:
            token = username#secrets.token_hex(8)
            waitingreq = Waiting(username, token, supermarket_id, date_time, date_time, wait_time)
            db.session.add(waitingreq)
            db.session.commit()
            return {"message": "Line-up has been created."}, 201
        else:
            return {"error": "You already Have a Request."}, 401
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400


#Booking function for selected supermarket
@cross_origin(origin='*')
@app.route('/booking', methods=['POST'])
@jwt_required()
def booking():
    try:
        print(request.json)
        username = request.json.get('username')
        supermarket_id = request.json.get('supermarket_id')
        shop_time_raw = request.json.get('shop_time')
        shop_time = datetime.datetime.strptime(shop_time_raw, '%Y-%m-%d %H:%M')
        date_time = datetime.datetime.now()
        time_to_turn = (shop_time - date_time).seconds+300
        requests = Waiting.query.filter_by(username=username).count()
        requests += Shopping.query.filter_by(username=username).count()
        maxBookings = Waiting.query.filter_by(supermarket_id=supermarket_id, shop_time=shop_time).count()
        # supermarket=Supermarket.query.filter_by(id=supermarket_id).first()

        if maxBookings > 1:
            return {"message": "Booking Time is Full."}, 400
        if requests < 1:
            token = username#secrets.token_hex(8)
            waitingreq = Waiting(username, token, supermarket_id, date_time, shop_time, time_to_turn)
            db.session.add(waitingreq)
            db.session.commit()
            return {"message": "Booking has been created."}, 201
        else:
            return {"error": "You already have a booking."}, 401
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

def isTurn(username,supermarket_id):
    dt_now = datetime.datetime.now()
    userWithTurn=db.session.query(Waiting).filter(
        and_(Waiting.shop_time <= dt_now+datetime.timedelta(minutes=5),Waiting.supermarket_id == supermarket_id)).order_by(
            Waiting.req_time).first()
    if userWithTurn!=None and userWithTurn.username==username and isAvailable(supermarket_id):
        return True
    else:
        return False
def updateWaitingTime(supermarket_id):
    supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
    if isAvailable(supermarket_id):
        supermarket.waiting_time = 0
    else:
        peopleShopping=Shopping.query.filter_by(supermarket_id=supermarket_id).count()
        supermarket.waiting_time = averageTime(supermarket)*peopleShopping
    db.session.commit()



@cross_origin(origin='*')
@app.route('/getin', methods=['POST'])
def getin():
    try:
        print(request.json)
        token = request.json.get('token')
        waitingUser = Waiting.query.filter_by(token=token).first()
        if waitingUser!=None:
            username=waitingUser.username
            supermarket_id = request.json.get('supermarket_id')
            date_time = datetime.datetime.now()
            if isTurn(username,supermarket_id):
                
                db.session.delete(waitingUser)
                db.session.commit()
                shoppingreq = Shopping(username, token, supermarket_id, date_time)
                db.session.add(shoppingreq)
                db.session.commit()
                updateWaitingTime(supermarket_id)
                return {"message": "The door is opened. "+str(username)+" has entered to ID: "+str(supermarket_id)}, 201
            else:
                return {"error": "It is not your turn."}, 400
        else:
            return {"error": "Wrong token"}, 400
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

@cross_origin(origin='*')
@app.route('/getout', methods=['POST'])
def getout():
    try:
        print(request.json)
        token = request.json.get('token')
        shoppingUser = Shopping.query.filter_by(token=token).first()
        if shoppingUser!=None:
            username=shoppingUser.username
            supermarket_id = request.json.get('supermarket_id')
            
            date_time = datetime.datetime.now()
            enter_time = shoppingUser.enter_time
            db.session.delete(shoppingUser)
            db.session.commit()
            record = Record(supermarket_id, (date_time-enter_time).seconds)
            db.session.add(record)
            db.session.commit()
            updateWaitingTime(supermarket_id)
            return {"message": "The door is opened. "+str(username)+" has leaved from ID: "+str(supermarket_id)}, 201
        else:
            return {"error": "User is not Shopping"}, 400 
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400


@cross_origin(origin='*')
@app.route('/deleteall_w', methods=['POST'])
def deleteall_w():
    try:
        Waiting.query.delete()
        db.session.commit()
        return {"message": "All waiting users have been deleted"}, 201
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

@cross_origin(origin='*')
@app.route('/deleteall_s', methods=['POST'])
def deleteall_s():
    try:
        Shopping.query.delete()
        db.session.commit()
        return {"message": "All shopping users have been deleted"}, 201
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

@cross_origin(origin='*')
@app.route('/deleteall', methods=['POST'])
def deleteall():
    try:
        Waiting.query.delete()
        db.session.commit()
        Shopping.query.delete()
        db.session.commit()
        return {"message": "All waiting & shopping users have been deleted"}, 201
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400
