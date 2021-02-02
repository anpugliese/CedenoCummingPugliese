from main import db
from sqlalchemy.dialects.postgresql import JSON
from timetable import Timetable

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
    def __init__(self, name, lat, lon):
        self.name = name
        self.address = None
        self.logo = None
        self.lat = lat
        self.lon = lon
        self.max_capacity = 20
        self.timetable = Timetable().toJson()
        self.waiting_time = 0
        self.mean_shopping_time = 10 



    def __repr__(self):
        return '<id {}>'.format(self.id)

class Section(db.Model):
    __tablename__ = 'Section'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, max_capacity):
        self.name = name
        self.max_capacity = max_capacity

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Request(db.Model):
    __tablename__ = 'Request'

    id = db.Column(db.Integer, primary_key=True)
    supermarket_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    type_id = db.Column(db.String(), nullable=False) #2 options: 'ASAP' or 'Booking'... can be also True or False

    def __init__(self, supermarket_id, type_id):
        self.supermarket_id = supermarket_id
        self.time = time
        self.type_id = type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Shopping(db.Model):
    __tablename__ = 'Shopping'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    request_id = db.Column(db.Integer, nullable=False)
    supermarket_id = db.Column(db.Integer, nullable=False)
    enter_time = db.Column(db.DateTime, nullable=False)
    #Maybe also exit time -> exit_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, request_id, supermarket_id, enter_time):
        self.username = username
        self.request_id = request_id
        self.supermarket_id = supermarket_id
        self.enter_time = enter_time

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Waiting(db.Model):
    __tablename__ = 'Waiting'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    request_id = db.Column(db.Integer, nullable=False)
    supermarket_id = db.Column(db.Integer, nullable=False)
    

    def __init__(self, username, request_id, supermarket_id):
        self.username = username
        self.request_id = request_id
        self.supermarket_id = supermarket_id

    def __repr__(self):
        return '<id {}>'.format(self.id)