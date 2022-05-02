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


def updateTinData(sealVal):
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
                print ('RFID found ')
                datenow = datetime.now()
                datetimestamp = datenow.strftime('%Y-%m-%-d %H:%M:%S')
                #Opening the database connection
                con = sqlite3.connect('TinTrackingDB.db')
                cur = con.cursor()
                cur.execute("select Id from TinDetails where RFID=:rfid", {"rfid": id})
                tinFkRow = cur.fetchone()
                tinfk = tinFkRow[0]+1
                print(tinfk)
                cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp,SealValidation) VALUES (null,?,'Seal Validated',?,?)",(tinfk,datetimestamp,sealVal))
                if (sealVal): Packing = 'Valid Consignment'
                else: Packing = 'Invalid Consignment'
                cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp,SealValidation) VALUES (null,?,?,?,?)",(tinfk,Packing,datetimestamp,sealVal))
                con.commit()
                con.close()
                IdRead = True
                break
        finally:
            gpio.cleanup()
            time.sleep(1)
    return IdRead 
