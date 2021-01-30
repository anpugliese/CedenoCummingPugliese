import datetime
import json
from time import strptime

#Timetable class to manage the availability of the supermarkets

class Timetable():
    def __init__(self, json_timetable=None): #, openingHour, closingHour, openingHourHoliday, closingHourHoliday):
        if json_timetable:
            self.openingHour = datetime.datetime.strptime(json_timetable["openingHour"], '%H:%M:%S').time()
            self.closingHour = datetime.datetime.strptime(json_timetable["closingHour"], '%H:%M:%S').time()
            self.openingHourHoliday = datetime.datetime.strptime(json_timetable["openingHourHoliday"], '%H:%M:%S').time()
            self.closingHourHoliday = datetime.datetime.strptime(json_timetable["closingHourHoliday"], '%H:%M:%S').time()
            
        else:
            self.openingHour = datetime.time(8, 0, 0)
            self.closingHour = datetime.time(20, 0, 0)
            self.openingHourHoliday = datetime.time(9, 0, 0)
            self.closingHourHoliday = datetime.time(18, 0, 0)

    #Compare current time with a supermarket's timetable
    def isAvailable(self):
        currentDateTime = datetime.datetime.now()
        currentTime = currentDateTime.time()
        if currentTime > self.openingHour and currentTime < self.closingHour:
            return True
        else:
            return False

    #Parse from dictionary to Json
    def toJson(self):
        dictionary = {
            "openingHour": self.openingHour.strftime("%X"), 
            "closingHour": self.closingHour.strftime("%X"),
            "openingHourHoliday": self.openingHourHoliday.strftime("%X"),
            "closingHourHoliday": self.closingHourHoliday.strftime("%X"),
        }

        json_object = json.dumps(dictionary)
        return json_object