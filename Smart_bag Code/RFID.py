import RPi.GPIO as GPIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
from mfrc522 import SimpleMFRC522


#VARIABLES AND CALLBACK FUNCTION
reader = SimpleMFRC522()
GPIO.setwarnings(False)
gc = gspread.service_account(filename = "users.json")
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1_FranxE4OZcJEI9B8jVgt_KATEsnzwS8jy7mJkEnrqc/edit#gid=0")
wsheet = gsheet.worksheet("Sheet 1")

def write():
    text = input("Please enter new user's name: ")
    print("Please place the card to complete writing")
    id, name = reader.write(text)
    print("Data" + name + " writing is completed")
    
def read():
    while True:
        print("Reading ... Please place the card ... ")
        id, text = reader.read()
        print("ID: %s \n Text: %s" % (id,text))
        

def update(pos,value):
    wsheet.update(pos, value)
    print("Data is updated")
    
def new(data):
    rows = len(wsheet.get())
    wsheet.insert_row(data,rows + 1)
    print("New data is inserted")
    
def get_id():
    print("Get all ID")
    return wsheet.col_values(1)

def destroy():
    GPIO.cleanup()