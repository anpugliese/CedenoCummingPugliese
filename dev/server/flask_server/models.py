from .main import db
from .timetable import Timetable
from sqlalchemy.dialects.postgresql import JSON

#Definition of the class User to create a user inside the table users
class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, username, password): 
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Supermarket(db.Model):
    __tablename__ = 'Supermarket'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=True)
    logo = db.Column(db.String(), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    timetable = db.Column(db.JSON, nullable=False)
    waiting_time = db.Column(db.Integer, nullable=False, server_default='0') #Time in minutes managed as integers
    mean_shopping_time = db.Column(db.Integer, nullable=False, server_default='10') #Mean shopping time to be updated when a user finishes the shopping
    #Constructor of the class supermarket...specify the proccess of creating a new supermarket
    def __init__(self, name, lat, lon, logo):
        self.name = name
        self.address = None
        self.logo = logo
        self.lat = lat
        self.lon = lon
        self.max_capacity = 2
        self.timetable = Timetable().toJson()
        self.waiting_time = 0
        self.mean_shopping_time = 5 



    def __repr__(self):
        return '<id {}>'.format(self.id)

<<<<<<< HEAD
=======

>>>>>>> main
class Shopping(db.Model):
    __tablename__ = 'Shopping'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    token = db.Column(db.String(), nullable=False)
    supermarket_id = db.Column(db.Integer, nullable=False)
    enter_time = db.Column(db.DateTime, nullable=False)
<<<<<<< HEAD
=======
    #Maybe also exit time -> exit_time = db.Column(db.DateTime, nullable=False)
>>>>>>> main

    def __init__(self, username, token, supermarket_id, enter_time):
        self.username = username
        self.token = token
        self.supermarket_id = supermarket_id
        self.enter_time = enter_time

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Waiting(db.Model):
    __tablename__ = 'Waiting'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    token = db.Column(db.String(), nullable=False)
    supermarket_id = db.Column(db.Integer, nullable=False)
    req_time = db.Column(db.DateTime, nullable=False)
    shop_time = db.Column(db.DateTime, nullable=False)
<<<<<<< HEAD
    wait_time = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
=======
    wait_time = db.Column(db.Integer, nullable=True)
    type_id = db.Column(db.Integer, nullable=True)

>>>>>>> main

    def __init__(self, username, token, supermarket_id, req_time, shop_time, wait_time, type_id):
        self.username = username
        self.token = token
        self.supermarket_id = supermarket_id
        self.req_time = req_time
        self.shop_time = shop_time
        self.wait_time = wait_time
        self.type_id = type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Record(db.Model):
    __tablename__ = 'Record'
    id = db.Column(db.Integer, primary_key=True)
    enter_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=False)
    supermarket_id = db.Column(db.Integer, nullable=False)
    delta_time = db.Column(db.Integer, nullable=False)
    

    def __init__(self, enter_time, exit_time, supermarket_id, delta_time):
        self.enter_time = enter_time
        self.exit_time = exit_time
        self.supermarket_id = supermarket_id
        self.delta_time = delta_time

    def __repr__(self):
        return '<id {}>'.format(self.id)