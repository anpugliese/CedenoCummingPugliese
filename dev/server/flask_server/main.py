import os
import json
import secrets
import datetime
from datetime import timedelta
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

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
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=12) #Session time
db = SQLAlchemy(app)
jwt = JWT(app, authenticate, identity) #JWT Json Web Token to manage sessions, by default managed in /auth (POST request)
CORS(app)

#This must be declared after declaring db
from models import User, Supermarket, Request
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

#Booking function for selected supermarket
@cross_origin(origin='*')
@app.route('/booking', methods=['POST'])
def booking():
    try:
        print(request.json)
        user_id = request.json.get('user_id')
        superid = request.json.get('superid')
        #date_time = request.json.get('timeid')
        date_time = datetime.datetime.now()
        typeid = 'Booking' 

        repeatedUser = Request.query.filter_by(user_id=user_id).first()
        maxBookings = Request.query.filter_by(time=date_time, supermarket_id=superid).count()
        
        if maxBookings > 3:
            return {"message": "Booking Time is Full."}, 201
        elif repeatedUser == None:
            print(user_id)
            print(user_id, superid, date_time, typeid)
            booking_token = secrets.token_bytes(10)
            bookingreq = Request(user_id, superid, date_time, typeid, booking_token)
            db.session.add(bookingreq)
            db.session.commit()
            return {"message": "Booking has been created."}, 201
        else:
            return {"error": "You already Have a Booking."}, 400
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400

#Populate database with supermarkets from supermarkets.json, only used once while developing 
"""@cross_origin(origin='*')
@app.route('/supermarkets', methods=['GET'])
def supermarket():
    try:
        f = open("data/supermarkets.json")
        supermarkets_dict = json.loads(f.read())
        for supermarket in supermarkets_dict:
            name = supermarket["name"]
            lat = supermarket["lat"]
            lon = supermarket["lon"]
            sp = Supermarket(name, lat, lon)
            db.session.add(sp) 
            db.session.commit()
        return {"message": "supermarket have been created."}, 201
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400"""

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
