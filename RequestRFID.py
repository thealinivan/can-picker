#Importing all the required libraries
#RPI gpio library 
import RPi.GPIO as gpio
#rfid reader and writer library
from mfrc522 import SimpleMFRC522
#importing time to manage timeout when scaning the rfid.
import time
#database library
import sqlite3
#date time library for the time stamp
from datetime import datetime
#Creating an object of the SimpleMFRC522 to enable scanning and writing to the tin tag
CardReader = SimpleMFRC522()
#mine area sample data writen to the tin
mineArea= "M28/03"
IdRead = False
gpio.setwarnings(False)

def reqRFIDValidation():
    timeoutval = time.time() + 5
    while time.time() < timeoutval:
        time.sleep(1)
        try:
            print ('Scanning Tin...')
            status, TagType = CardReader.read_no_block()
            #print (status)
            if status == None:
                print ('no RFID found ')
                IdRead = False
            elif status != None:
                #reading in the value and writing to the tin tag
                id, text = CardReader.read()
                CardReader.write(mineArea)
                print ('RFID found ')
                datenow = datetime.now()
                datetimestamp = datenow.strftime('%Y-%m-%-d %H:%M:%S')
                #Opening the database connection
                con = sqlite3.connect('TinTrackingDB.db')
                cur = con.cursor()
                 #inserting into tin details the tin values
                cur.execute("INSERT INTO TinDetails(Id,RFID,CurrentStatus,DiamondMaterial,DateStamp) VALUES (null,?,'New Tin',?,?)",(id,mineArea,datetimestamp,))
                tinfk= cur.lastrowid
                #Updating the tin history for tin tracking
                cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp,SealValidation) VALUES (null,?,'New Tin',?,0)",(tinfk,datetimestamp,))
                #commiting the database changes 
                con.commit()
                con.close()
                IdRead = True
                break
        finally:
            gpio.cleanup()
            time.sleep(1)
    return IdRead
        