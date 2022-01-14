#from typing import Counter
from mysql.connector import cursor
import pyrebase
from pynput.keyboard import Key,Controller
from datetime import date, datetime
from threading import Timer
#Import Library
import time
import schedule
import mysql.connector
import RPi.GPIO as GPIO

#Database configuration
DB_HOST = "localhost"
DB_USER = "AC2"
DB_PASS = "biomechlab2021"
DB_DATA = "rfid"
DB_PORT = "3306"

#Set up firebase
firebaseConfig = {
  "apiKey": "AIzaSyDIVZpkltz4SqMdDjIsz1rQfglvwEklgDo",
  "authDomain": "smart-bag-f74be.firebaseapp.com",
  "databaseURL": "https://smart-bag-f74be-default-rtdb.firebaseio.com",
  "projectId": "smart-bag-f74be",
  "storageBucket": "smart-bag-f74be.appspot.com",
  "messagingSenderId": "669735670893",
  "appId": "1:669735670893:web:b04df1b54ea830ee845b64",
  "measurementId": "G-XDJDVFL44F"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

#Create empty list
Id_list = []
Status_list = []
State_1 = 1
State_2 = 0


#LED Set up
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT)
#GPIO.setwarnings(False)
#GPIO.output(18,0)

#Update data every 10s
def update_data(tagId, Status_list):
   db.child("ID").child(tagId).update({"Status":Status_list})
    
def Update_RFID(Status_list, Id_list):
    Caplocks()
    for i in range(0,len(Id_list)):
#         if Status_list[i] == State_1:
        update_data(Id_list[i], Status_list[i])
    print("Update sucessfully")
    time.sleep(5)
    count = 0
    for k in range(0, len(Id_list)):
        if Status_list[k] == State_1:
            count += 1
        else:
            count += 0
    print(count)
    if count >= 3:
#         print("Turn off the red LED")
         print("Turn on the green LED")
          #GPIO.output(18,1)
    else:
         print("Turn on the red LED")
          #GPIO.output(18,0)
    print(Status_list)
    
    
    for j in range(0,len(Id_list)):
        Status_list[j] = State_2
    print(Status_list)
    Caplocks()
    
    
#Check license
def check_license():
    key = db.child("License").child("Key").get()
    return key.val()


#Import data from database into the handling list
data = db.child("ID").shallow().get()
Id_list = list(data.val())
#for k in range(0, len(Id_list)):
    #Status_list.append(0)
#Status_list[0,len(Id_list)] = Status_list.append(0)
#print(Status_list)
def import_data():
    for i in data.val():
        Status = db.child("ID").child(i).child("Status").get()
        #Status_list.append(Status.val())
        Status_list.append(0)

#Turn on RFID Reader
def Caplocks():
    keyboard = Controller()
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)

def Activate():
    keyboard = Controller()
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)

def Pass():
    enter = Controller()
    enter.press('2')
    enter.press('2')
    enter.press('7')
    enter.press('1')
    enter.press('9')
    enter.press(Key.enter)
    enter.release(Key.enter)

#Compare and get data into handling list
def RFID_Reader(Status_list, Id_list):
    #Turn on RFID
    #Caplocks()
    #22719
    #Caplocks()

    #Start to read ID tag
    set_timer = 4
    t = Timer(set_timer, Pass)
    t.start()
    tagId_untransformed = input("Enter the RFID tag: ")
    t.cancel()
    tagID= tagId_untransformed.split('227')[1]
    print("RFID Tag is: " + str(tagID))
    
    #Compare ID tag to ID list
    for i in range (0,len(Id_list)):
        if tagID == Id_list[i]:
            Status_list[i] = State_1
        elif Status_list[i] != State_2:
            Status_list[i] = State_1
        else:
            Status_list[i] = State_2
#---------------------------MAIN PROGRAM----------------------------------

if __name__ == "__main__":
    Caplocks()
    license_key = 2021
    if check_license() == license_key:
        print("Your key is valid")
        import_data()
        schedule.every(1).seconds.do(RFID_Reader, Status_list, Id_list)
        schedule.every(10).seconds.do(Update_RFID, Status_list, Id_list)
        #schedule.every(5).seconds.do(Caplocks)
            
        while True:
            #Caplocks()
            #Caplocks()
            schedule.run_pending()
            time.sleep(1)
            #Caplocks()
    else:
        while(True):
            print("Error... Your system has been disabled")
            
            time.sleep(2)
            #GPIO.output(18,1)
            
            time.sleep(1)
            #GPIO.output(18,0)