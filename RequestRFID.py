#Importing all the required libraries
import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import sqlite3
from datetime import datetime
#Creating an object of the SimpleMFRC522 to enable scanning and writing to the tin tag
CardReader = SimpleMFRC522() 
print ('Scanning Tin...')
#Waiting for the UR10 to scan the rfid on the tin tag
datenow = datetime.now()
#Setting the timestamp value
datetimestamp = datenow.strftime('%Y-%m-%-d %H:%M:%S')
mineArea = "M14/08"


def reqRFIDValidation():
    try:
       	#reading in the card id 
       	id, text = CardReader.read()
       	CardReader.write(mineArea)
        print (id)
        print (text)
        #Opening the database connection
        con = sqlite3.connect('TinTrackingDB.db')
        cur = con.cursor()
        cur.execute("INSERT INTO TinDetails(Id,RFID,CurrentStatus,DiamondMaterial,DateStamp) VALUES (null,?,'New Tin',?,?)",(id,mineArea,datetimestamp,))
        tinfk= cur.lastrowid
        cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp) VALUES (null,?,'New Tin',?)",(tinfk,datetimestamp,))
        cur.execute("select Id from TinDetails where RFID=:rfid", {"rfid": id})
        tinfk=cur.fetchone()
        print(tinfk)
        con.commit()
        con.close()
        gpio.cleanup()
        return true
        
    except:
        print('somethig went wrong with RFID reading or database')
        return false
    #finally:
        
    