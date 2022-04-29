import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import sqlite3
from datetime import datetime
 

def updateTinData2(sealVal):
 #reading in the card id
    Packing =''
    gpio.setwarnings(False)
    CardReader = SimpleMFRC522()
    id, text = CardReader.read()
    #mineArea = "PacificOcean"
    #CardReader.write(mineArea)
    print (id)
    print (text)
    datenow = datetime.now()
    datetimestamp = datenow.strftime('%Y-%m-%-d %H:%M:%S')
    con = sqlite3.connect('TinTrackingDB.db')
    cur = con.cursor()
    #
    cur.execute("select Id from TinDetails where RFID=:rfid", {"rfid": id})
    tinFkRow = cur.fetchone()
    tinfk = tinFkRow[0]+1
    #tinfk = cur.lastrowid
    #cur.execute("Update TinHistory(SealValidation,Status) SET SealValidation=:SealVal,Status='Seal Validated' where RFID=:rfid", {"SealVal": SealVal},{"rfid": id})
    print(tinfk)
    cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp,SealValidation) VALUES (null,?,'Seal Validated',?,?)",(tinfk,datetimestamp,sealVal))
    if (sealVal): Packing = 'Valid Consignment'
    else: Packing = 'Invalid Consignment'
    cur.execute("INSERT INTO TinHistory(Id,TinFK,Status,DateStamp,SealValidation) VALUES (null,?,?,?,?)",(tinfk,Packing,datetimestamp,sealVal))
    con.commit()
    con.close()
    gpio.cleanup()
    
    
updateTinData2(True)