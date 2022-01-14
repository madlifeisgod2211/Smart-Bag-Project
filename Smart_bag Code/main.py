# IMPORT LIBRARY
import gspread
import pyrebase
import schedule
import mysql.connector
import RPi.GPIO as GPIO
import RFID
import time
from mfrc522 import SimpleMFRC522
from mysql.connector import cursor
from pynput.keyboard import Key, Controller
from datetime import date, datetime
from threading import Timer
from oauth2client.service_account import ServiceAccountCredentials

#                       WIRING DIAGRAM

# ---------------------- LED AND LOCKER ----------------------------
# ------------------------------------------------------------------
# --------------- LOCKER AND GREEN LED --> PIN   13 ----------------
# --------------- LOCK BUTTON          --> PIN   15 ----------------
# --------------- RED LED              --> PIN   11 ----------------
# ------------------------------------------------------------------
# -------------------------- RFID ----------------------------------
# --------------- 3.3V                 --> PIN   1  ----------------
# --------------- RST                  --> PIN   22 ----------------
# --------------- GND                  --> PIN   6  ----------------
# --------------- MISO                 --> PIN   21 ----------------
# --------------- MOSI                 --> PIN   19 ----------------
# --------------- SCK                  --> PIN   23 ----------------
# --------------- SDA                  --> PIN   24 ----------------
# ------------------------------------------------------------------


#                           PROGRAMMING FLOW

# ---------------------- UNCLOCK DOOR ------------------------------
# ------------------------------------------------------------------
# --------------- 1. WRITE RFID TAGS 
# --------------- 2. READ RFID TAGS : 
# ---------------           IF RFID TAGS ARE VALID:          -------
# ---------------                   UNCLOCK DOOR + GREEN LEĐ -------
# ---------------           ELSE:                            -------
# ---------------                   BUZZER()                 -------
# --------------- 3. CLOSE THE DOOR:                         -------
# ---------------           IF BUTTON IS PRESSED:            -------
# ---------------                   LOCK DOOR                -------
# --------------- 4. RUN RFID DESKTOP                        -------
# ------------------------------------------------------------------
# ----------------------- MEDICAL DEVICES IDENTIFICATION -----------
# --------------- 1. CHECK LICENSE KEY                           ---
# --------------- 2. GET DATA FROM DATABASE                      ---
# --------------- 3. ACTIVATE RFID (CAPLOCKS KEYBOARD)           ---
# --------------- 4. READ RFID TAGS (SAMPLING TIME 5S)           ---
# --------------- 5. COMPARE RFID TAGS ---> RETURN STATUS 0 OR 1 ---
# --------------- 6. CLOSE RFID                                  ---
# --------------- 7. UPDATE DATA INTO DATABASE ---------------------
# ------------------------------------------------------------------

# DATABASE CONFIGURATION
DB_HOST = "localhost"
DB_USER = "AC2"
DB_PASS = "biomechlab2021"
DB_DATA = "rfid"
DB_PORT = "3306"

# SET UP FIREBASE
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

# SET UP BUTTON AND LED
locker = 13
button = 15
red_led = 11


# SET UP LED AND SOLENOID LOCKER
GPIO.setmode(GPIO.BOARD)
GPIO.setup(locker,GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(locker,GPIO.LOW)
reader = SimpleMFRC522()
gc = gspread.service_account(filename = "users.json")
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1_FranxE4OZcJEI9B8jVgt_KATEsnzwS8jy7mJkEnrqc/edit#gid=0")
wsheet = gsheet.worksheet("Sheet 1")

# LED MODE
def setLED(mode):
    if mode == true:
        GPIO.output(locker, GPIO.HIGH)
        time.sleep(0.5)
    else:
        GPIO.output(locker, GPIO.LOW)
        time.sleep(0.5)

# INTIAL DATA
id_list  = []
rows = len(wsheet.get())
Id_list = []
Status_list = []
State_1 = 1
State_2 = 0

# MAIN PROGRAM
def main():

    # CREATE NEW USERS
    # while True:
    #     if (GPIO.input(button_write) == GPIO.HIGH):
    #         RFID.write()
    #         RFID.new([id,text])
    #         break
    
    # READ RFID TAGS
    id_list = RFID.get_id()
    #RFID.read()
    id = "abc"

    print(id)

    # COMPARE ID TAGS
    for i in range (1, rows):
        if (id == id_list[i]):
            # OPEN THE DOOR
            time.sleep(0.5)
            GPIO.output(locker, GPIO.HIGH)
            print("OPEN THE DOOR")
            break
        else:
            # CLOSE THE DOOR
            GPIO.output(locker, GPIO.LOW)
            GPIO.output(red_led, GPIO.HIGH)
            time.sleep(2)
            # WARNING LED
            GPIO.output(red_led, GPIO.LOW)
            print("PLEASE CHECK YOUR USER'S TAG")
            
    
    # CLOSE THE DOOR
    while True:
        if GPIO.input(button) == GPIO.HIGH:
            GPIO.output(locker, GPIO.HIGH)
            # WARNING LED
            GPIO.output(red_led, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(red_led, GPIO.LOW)
            print("CLOSE THE DOOR")

        else:
            
            time.sleep(1)

if __name__ == '__main__':
    try:
        RFID.get_id()
    except KeyboardInterrupt:
        RFID.destroy()