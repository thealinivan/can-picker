#Importing all the required libraries
import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import sqlite3
from datetime import datetime
#importing time to manage timeout when scaning the rfid.
import time
#Creating an object of the SimpleMFRC522 to enable scanning and writing to the tin tag
gpio.setwarnings(False)
CardReader = SimpleMFRC522()
mineArea = "M14/08"

def reqRFIDValidation():
    print ('Scanning Tin...')
    timeout = time.time() + 3
    try:
        while time.time() < timeout:
       	#reading in the card id 
            id, text = CardReader.read()
            CardReader.write(mineArea)
            print (id)
            print (text)
            #Opening the database connection
            #Setting the timestamp value
            if (id):
                datenow = datetime.now()
                datetimestamp = datenow.strftime('%Y-%m-%-d %H:%M:%S')
                con = sqlite3.connect('TinTrackingDB.db')
                cur = con.cursor()
                cur.execute("INSERT INTO TinDetails(Id,RFID,CurrentStatus,DiamondMaterial,DateStamp) VALUES (null,?,'New Tin',?,?)",(id,mineArea,datetimestamp,))
                tinfk= cur.lastrowid
                cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp,SealValidation) VALUES (null,?,'New Tin',?,0)",(tinfk,datetimestamp,))
                cur.execute("select Id from TinDetails where RFID=:rfid", {"rfid": id})
                tinfk=cur.fetchone()
                print(tinfk)
                con.commit()
                con.close()
                gpio.cleanup()
                True
                break
            time.sleep(1)
    except:
        print('somethig went wrong with RFID reading or database')
        return False
    #finally:
        
    