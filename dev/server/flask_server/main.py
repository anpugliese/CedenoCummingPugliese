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
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import and_
import numpy as np
import time
from flask_apscheduler import APScheduler

db = SQLAlchemy()

#This must be declared after declaring db
from .models import *
from .timetable import Timetable

#Authenticate function for JWT
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password, password):
        return user

#Identity function for JWT
def identity(payload):
    user_id = payload['identity']
    print(User.query.get(user_id))
    return User.query.get(user_id) is not None

# This function creates the app. The testing parameter changes the database url.
# The development server is created calling this function in the end of the file.
def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24) #Session time

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:password@127.0.0.1:5432/clup_test_DB" #URI to be changed in deployment
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:password@127.0.0.1:5432/clup_DB" #URI to be changed in deployment

    db.init_app(app)

    jwt = JWT(app, authenticate, identity) #JWT Json Web Token to manage sessions, by default managed in /auth (POST request)
    CORS(app)

    # initialize scheduler
    scheduler = APScheduler()
    # if you don't wanna use a config, you can set options here:
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    migrate = Migrate(app, db)

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
            return {"error": "Error"}, 500

    #Populate database with supermarkets from supermarkets.json, only used once while developing 
    # @cross_origin(origin='*')
    # @app.route('/supermarkets', methods=['GET'])
    # def supermarket():
    #     try:
    #         f = open("data/supermarkets.json")
    #         supermarkets_dict = json.loads(f.read())
    #         g = open("data/images.json")
    #         images_dict = json.loads(g.read())
    #         regex = re.compile('^[a-zA-Z0-9]*$')
    #         for supermarket in supermarkets_dict:
    #             name = supermarket["name"]
    #             aux=True
    #             for imgs in images_dict:
    #                 if imgs["name"] in re.sub('[^A-Za-z0-9]+', ' ', name).lstrip().lower():
    #                     logo=imgs["url"]
    #                     aux=False
    #                     break
    #             if aux:
    #                 logo="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Italian_traffic_signs_-_icona_supermercato.svg/1024px-Italian_traffic_signs_-_icona_supermercato.svg.png"
    #             lat = supermarket["lat"]
    #             lon = supermarket["lon"]
    #             sp = Supermarket(name, lat, lon, logo)
    #             db.session.add(sp) 
    #             db.session.commit()
    #         return {"message": "supermarket have been created."}, 201
    #     except Exception as ex:
    #         print(ex)
    #         return {"error": "Error"}, 400

    #Retrieve all supermarkets (filter only in frontend)
    @cross_origin(origin='*')
    @app.route('/supermarkets_list', methods=['GET'])
    @jwt_required()
    def supermarkets_list():
        try:
            sp_list = Supermarket.query.all()
            json_list = []
            for supermarket in sp_list:
                current_timetable = Timetable(json_timetable=json.loads(supermarket.timetable))
                #if current_timetable.isAvailable():
                if True:
                    sp = {
                        "id": supermarket.id,
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
            return {"error": "Error"}, 500

    # it computes the average shopping time in seconds in case there are records, otherwise it just returns the default value in the DB
    def averageTime(supermarket):
        delta_times = []
        records = Record.query.filter_by(supermarket_id=supermarket.id).all()
        suma = 0
        for record in records:
            delta_times.append(record.delta_time)
            suma += record.delta_time
        #avg_time=np.mean(np.array(delta_times))
        records_count=len(records)
        avg_time = 0
        if records_count > 0:
            avg_time = suma/records_count
        if records_count>0:
            return avg_time
        else:
            return supermarket.mean_shopping_time*60

    # it checks whether a supermarket is available or not
    def isAvailable(supermarket_id):
        people_shopping=Shopping.query.filter_by(supermarket_id=supermarket_id).count()
        supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
        if people_shopping<supermarket.max_capacity:
            return True
        else:
            return False

    @cross_origin(origin='*')
    @app.route('/lineup', methods=['POST'])
    @jwt_required()
    def lineup(): #line up request
        try:
            print(request.json)
            username = request.json.get('username')
            supermarket_id = request.json.get('supermarket_id')
            date_time = datetime.datetime.now()
            requests = Waiting.query.filter_by(username=username).count()
            requests += Shopping.query.filter_by(username=username).count() # total number of requests
            # total number of users shopping
            people_shopping=Shopping.query.filter_by(supermarket_id=supermarket_id).count() 
            # total number of users waiting
            people_waiting=Waiting.query.filter_by(supermarket_id=supermarket_id).count() 
            supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
            # if the user is the first in the queue of a full supermarket
            if people_waiting==0 and people_shopping==supermarket.max_capacity:
                wait_time=int(averageTime(supermarket))
            else:# any other case (people_waiting could be zero as well)
                wait_time=int(people_waiting*averageTime(supermarket))
            #estimated time in which it is the user's turn
            shop_time=date_time+datetime.timedelta(seconds=wait_time)
            #check that the user has only one request at a time
            if requests < 1:
                token = username#secrets.token_hex(8)
                waitingreq = Waiting(username, token, supermarket_id, date_time, shop_time, wait_time,0)#zero stands for line-up
                db.session.add(waitingreq)
                db.session.commit()
                return {"message": "Line-up has been created."}, 201
            else:
                return {"error": "You already Have a Request."}, 401
        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500

    #Booking function for selected supermarket
    @cross_origin(origin='*')
    @app.route('/booking', methods=['POST'])
    @jwt_required()
    def booking(): #booking request
        try:
            print(request.json)
            username = request.json.get('username')
            supermarket_id = request.json.get('supermarket_id')
            #raw user's booking time selection
            shop_time_raw = request.json.get('shop_time')
            #convert it to datetime format
            shop_time = datetime.datetime.strptime(shop_time_raw, '%Y-%m-%d %H:%M')
            date_time = datetime.datetime.now()
            #time left to have the turn from booking
            diff=shop_time - date_time   
            time_to_turn = diff.seconds + diff.days * 24 * 3600
            requests = Waiting.query.filter_by(username=username).count()
            requests += Shopping.query.filter_by(username=username).count()# total number of requests
            #all the bookings at the same time
            maxBookings = Waiting.query.filter_by(supermarket_id=supermarket_id, shop_time=shop_time).count() 
            supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
            #number of bookings cannot surpass the supermarket's capacity
            if maxBookings > supermarket.max_capacity:
                return {"message": "Booking Time is Full."}, 402
            #valid booking time range: from 1 hour to 1 week after now
            if shop_time < date_time+datetime.timedelta(minutes=60) or shop_time > date_time+datetime.timedelta(days=7):
                return {"message": "Invalid Booking Time."}, 403
            #check that the user has only one request at a time
            if requests < 1:
                token = username#secrets.token_hex(8)
                waitingreq = Waiting(username, token, supermarket_id, date_time, shop_time, time_to_turn,1)#one stands for booking
                db.session.add(waitingreq)
                db.session.commit()
                return {"message": "Booking has been created."}, 201
            else:
                return {"error": "You already have a request."}, 401
        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500
    # Function to obtain the secret token and send it to the QRCode page 
    @cross_origin(origin='*')
    @app.route('/qrcode', methods=['POST'])
    @jwt_required()
    def qrcode():
        try:
            # obtain username
            username = request.json.get('username')
            # obtain waiting times
            count_waiting_token = Waiting.query.filter_by(username=username).count()
            count_shopping_token = Shopping.query.filter_by(username=username).count()
            # obtain supermarket name based on the username
            supermarket_id_n = Waiting.query.filter_by(username=username).first()
            if supermarket_id_n!=None:
                supermarket_id_n = supermarket_id_n.supermarket_id
                supermarket_name = Supermarket.query.filter_by(id=supermarket_id_n).first()
                supermarket_name = supermarket_name.name

            # return the secret token and supermarket name for booking
            if count_waiting_token == 1:
                super_token = Waiting.query.filter_by(username=username).first()
                super_token = super_token.token
                return {"qr_code": super_token,
                        "supermarket_name": supermarket_name}
            
            # return the secret token and supermarket name for lineup
            elif count_shopping_token == 1:
                super_token = Shopping.query.filter_by(username=username).first()
                super_token = super_token.token
                return {"qr_code": super_token,
                        "supermarket_name": supermarket_name}

            else:
                return {"message": "You don't have any ticket."}, 201

        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500
    #Function to deliver waiting time to QRCode page
    @cross_origin(origin='*')
    @app.route('/remainingTime', methods=['POST'])
    @jwt_required()
    def remainingTime():
        try:
            # Query to obtain waiting time from Waiting table
            username = request.json.get('username')
            waiting_time_g = Waiting.query.filter_by(username=username).first()

            if waiting_time_g!=None:
                waiting_time = waiting_time_g.wait_time
                enter_time = waiting_time_g.enter_time
                #Calculate number of minutes
                mins = (round(waiting_time/3600, 4)-int(waiting_time/3600))
                #return JSON with minutes, hours and total waiting time
                return {"remain_time_min": int(mins*60),
                        "remain_time_hours": int(waiting_time/3600),
                        "wait_time": waiting_time,
                        "enter_time": enter_time,
                        }
            else:
                return {"message": "No QR code."}, 201


        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500

    
    # this returns true if the user has the oldest request on a specific supermarket
    def isTurn(username,supermarket_id):
        dt_now = datetime.datetime.now()
        userWithTurn=db.session.query(Waiting).filter(Waiting.supermarket_id == supermarket_id).order_by(
                Waiting.req_time).first()
        if userWithTurn!=None and userWithTurn.username==username and isAvailable(supermarket_id):
            return True
        else:
            return False

    # this updates the waiting times each time an user enters or leaves the supermarket
    def updateWaitingTime(supermarket_id):
        supermarket=Supermarket.query.filter_by(id=supermarket_id).first()
        userWithTurn=db.session.query(Waiting).filter(Waiting.supermarket_id == supermarket_id).order_by(
                    Waiting.req_time).first()
        if isAvailable(supermarket_id) and userWithTurn==None:
            supermarket.waiting_time = 0
            db.session.commit()
        elif isAvailable(supermarket_id) and userWithTurn!=None:
            dt_now=datetime.datetime.now()
            people_waiting=Waiting.query.filter_by(supermarket_id=supermarket_id).count()
            supermarket.waiting_time = int(averageTime(supermarket)*people_waiting/60)
            db.session.commit()
            if userWithTurn.type_id==0:
                userWithTurn.wait_time = 0
                db.session.commit()
            else:
                
                diff=userWithTurn.shop_time-dt_now
                time_to_turn = diff.seconds + diff.days * 24 * 3600
                userWithTurn.wait_time = time_to_turn
                db.session.commit()
            if userWithTurn.wait_time!=0:
                userWithTurn.shop_time=dt_now+datetime.timedelta(seconds=userWithTurn.wait_time)
                db.session.commit()
            else:
                diff=userWithTurn.shop_time-dt_now
                userWithTurn.enter_time = diff.seconds + diff.days * 24 * 3600+300
                db.session.commit()
            
        else:
            people_waiting=Waiting.query.filter_by(supermarket_id=supermarket_id).count()
            if userWithTurn!=None:
                supermarket.waiting_time = int(averageTime(supermarket)/60)
            else:
                supermarket.waiting_time = int(averageTime(supermarket)*people_waiting/60)
            db.session.commit()

    # given token and supermarket, the function removes it from Waiting and insert it on Shopping
    @cross_origin(origin='*')
    @app.route('/getin', methods=['POST'])
    def getin():
        try:
            print(request.json)
            token = request.json.get('token')
            # get request from that token
            waitingUser = Waiting.query.filter_by(token=token).first()
            if waitingUser!=None:
                username=waitingUser.username
                supermarket_id = request.json.get('supermarket_id')
                date_time = datetime.datetime.now()
                # check if the user has the oldest request in the queue to the supermarket (FCFS queueing)
                if isTurn(username,supermarket_id):
                    #update waiting time of the supermarket
                    updateWaitingTime(supermarket_id)
                    #delete from waiting table
                    db.session.delete(waitingUser)
                    db.session.commit()
                    #add to shopping table
                    shoppingreq = Shopping(username, token, supermarket_id, date_time)
                    db.session.add(shoppingreq)
                    db.session.commit()


                    return {"message": "The door is opened. "+str(username)+" has entered to ID: "+str(supermarket_id)}, 201
                else:
                    return {"error": "It is not your turn."}, 401
            else:
                return {"error": "Wrong token"}, 402
        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500

    # given a token and supermarket, this removes it from Shopping and insert a Record of total shop time in seconds
    @cross_origin(origin='*')
    @app.route('/getout', methods=['POST'])
    def getout():
        try:
            print(request.json)
            token = request.json.get('token')
            # get shopping user associated to the token scanned when the user leaves the supermarket
            shoppingUser = Shopping.query.filter_by(token=token).first()
            if shoppingUser!=None:
                username=shoppingUser.username
                supermarket_id = request.json.get('supermarket_id')
                #update waiting time of the supermarket
                updateWaitingTime(supermarket_id)
                date_time = datetime.datetime.now()
                enter_time = shoppingUser.enter_time
                #remove user from Shopping table
                db.session.delete(shoppingUser)
                db.session.commit()
                #registrate the record of the time that the user took in shopping for time estimation in the specific supermarket
                record = Record(enter_time, date_time, supermarket_id, (date_time-enter_time).seconds)
                db.session.add(record)
                db.session.commit()
                
                return {"message": "The door is opened. "+str(username)+" has leaved from ID: "+str(supermarket_id)}, 201
            else:
                return {"error": "User is not Shopping"}, 401
        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500

    #this function runs every one minute to update waiting time associated to the requests
    # also it removes from waiting table the expired requests
    @scheduler.task('interval', id='do_job_1', seconds=5)
    def control_waiting_time():
        app.app_context().push()
        dt_now = datetime.datetime.now()
 
        # delete expired requests
        expired_req=db.session.query(Waiting).filter(Waiting.shop_time < dt_now-datetime.timedelta(minutes=5))
        expired_req.delete()
        db.session.commit()
        
        # fetch supermarkets with waiting time greater than zero and that are present in the waiting table (no repetitions)
        supermarkets_id_query=db.session.query(Supermarket.id).filter(Supermarket.waiting_time >0).all()
        waintings_id_query=db.session.query(Waiting.supermarket_id).distinct().all()
        supermarkets_list=supermarkets_id_query + list(set(waintings_id_query) - set(supermarkets_id_query))
        ## loop on the supermarkets that are present in the waiting table and have waiting time greater than zero
        for req in supermarkets_list:
            updateWaitingTime(req[0])
            if not isAvailable(req[0]): #if the supermarket is full
                userWithTurn=db.session.query(Waiting).filter( #get the queue of the supermarket
                    and_(Waiting.supermarket_id == req[0],Waiting.shop_time <= dt_now+datetime.timedelta(minutes=5),Waiting.type_id==0)).order_by(
                        Waiting.req_time)
                supermarket=Supermarket.query.filter_by(id=req[0]).first()
                counter=1
                avg_time=averageTime(supermarket)
                # update the wait time of the users that are in the queue
                for user in userWithTurn:
                    if user.type_id==0:
                        user.wait_time=int(counter*avg_time)
                        db.session.commit()
                        counter+=1
                    else:
                        diff=user.shop_time-dt_now
                        time_to_turn = diff.seconds + diff.days * 24 * 3600
                        user.wait_time = time_to_turn
                        db.session.commit()
                    if user.wait_time!=0:
                        user.shop_time=dt_now+datetime.timedelta(seconds=user.wait_time)
                        db.session.commit()
                    else:
                        diff=user.shop_time-dt_now
                        user.enter_time = diff.seconds + diff.days * 24 * 3600+300
                        db.session.commit()
                    
        print("Waiting Time Control: "+time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
  
   # the followint is a function to delete the booking or lineup request
    @cross_origin(origin='*')
    @app.route('/cancelFun', methods=['POST'])    
    @jwt_required()
    def cancelFun():
        try:
            # query Wating table for a specific user
            username = request.json.get('username')
            #line to be deleted
            todel = Waiting.query.filter_by(username=username).first()
            # delete selected
            db.session.delete(todel)
            db.session.commit()
            return {"message": "Booking deleted!"}, 200

        except Exception as ex:
            print(ex)
            return {"error": "Error"}, 500

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
            return {"error": "Error"}, 500

    return app

app = create_app()
