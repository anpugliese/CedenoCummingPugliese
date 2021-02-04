import os
import json
import secrets
import datetime
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from sqlalchemy import desc
from sqlalchemy.sql import func

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
from models import User, Supermarket, Request, Waiting, Shopping, Record
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
""" @cross_origin(origin='*')
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
        return {"error": "Error"}, 400 """

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
    records=Record.query.filter_by(supermarket_id=supermarket.id)
    records_count=records.count()
    if records_count>0:
        return db.session(func.avg(Record.delta_time)).first()
    else:
        return supermarket.mean_shopping_time

def isAvailable(supermarket):
    people_shopping=Shopping.query.filter_by(supermarket_id=supermarket.id).count()
    print('people shopping '+str(people_shopping))
    if people_shopping<=supermarket.max_capacity:
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
        typeid = 'ASAP' 
        requests = Request.query.filter_by(username=username).count()
        
        if requests < 1:
            print(username, supermarket_id, date_time, typeid)
            lineup_token = secrets.token_bytes(10)
            lineupreq = Request(username, supermarket_id, date_time, typeid, lineup_token)
            db.session.add(lineupreq)
            db.session.commit()
            waitingreq = Waiting(username, lineup_token, supermarket_id, date_time)
            db.session.add(waitingreq)
            db.session.commit()
            supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
            if not isAvailable(supermarket):
                supermarket.waiting_time += averageTime(supermarket)
                print('está lleno')
                db.session.commit()
            return {"message": "Line-up has been created."}, 201
        else:
            return {"error": "You already Have a Booking."}, 400
    except Exception as ex:
        print(ex)
        return {"error": "Error"}, 400



# def isTurn(username,supermarket_id):
#     supermarket=Supermarket.query.filter_by(id=supermarket_id)
#     date_time_now = datetime.datetime.now()
#     waitingUser=Waiting.query.filter_by(supermarket_id=id).order_by(desc(Waiting.waiting_time))
    

#     if waitingUser!= None:
        
    
#     else:
#         return False


# @cross_origin(origin='*')
# @app.route('/getIn', methods=['POST'])
# def getIn():
#     try:
#         print(request.json)
#         token = request.json.get('token')
#         waitingUser = Waiting.query.filter_by(token=token)
#         username=waitingUser.username
#         supermarket_id = request.json.get('supermarket_id')
#         date_time = datetime.datetime.now()
#         if waitingUser.count()==1 and isAvailable(supermarket_id):
#             db.session.delete(waitingUser)
#             db.session.commit()
#             shoppingreq = Shopping(username, token, supermarket_id, date_time)
#             db.session.add(shoppingreq)
#             db.session.commit()
#             return {"message": "The door is opened. "+str(username)+" has entered to ID: "+str(supermarket_id)}, 201
#         else:
#             return {"error": "You already Have a Booking."}, 400
#     except Exception as ex:
#         print(ex)
#         return {"error": "Error"}, 400
# def getOut():
#     try:
#         print(request.json)
#         token = request.json.get('token')
#         shoppingUser = Shopping.query.filter_by(token=token)
#         username=shoppingUser.username
#         date_time = datetime.datetime.now()
#         if waitingUser.count()==1 and isAvailable(supermarket_id):
#             db.session.delete(waitingUser)
#             db.session.commit()
#             shoppingreq = Shopping(username, token, supermarket_id, date_time)
#             db.session.add(shoppingreq)
#             db.session.commit()
#             return {"message": "The door is opened. "+str(username)+" has entered to ID: "+str(supermarket_id)}, 201
#         else:
#             return {"error": "You already Have a Booking."}, 400
#     except Exception as ex:
#         print(ex)
#         return {"error": "Error"}, 400
