import cv2
import numpy as np
import sqlite3
from time import sleep
from datetime import datetime
from image_processing import getOrientation
from image_processing import getContour
from math import atan2, cos, sin, sqrt, pi
from visualization import visualiseTinPos
from camera_calibration import undistortImage
from RequestRFID import reqRFIDValidation

import sys
import urlib

#cam src
pickingCam = 0
sealCam = 2
#frames stabilization limit
maxF = 50
#frame resolution
res = [960, 1280]
#px to mm conversiton rate
pxmm = 1.08285
#robot work object coordinate in (mm)
xR = 1050
yR = 600
zR = 150

#
rotationAngle = 0
gripperOpening = 0
shortAxis = 0
gripperDown = 0.1
#

#request empty tin / args - pose:current robot pose / return - pose:target pose
def requestEmptyTin(p):
    print("empty tin request..")
    sleep(1)
    vce = cv2.VideoCapture(pickingCam)
    vce.set(3, res[0])
    vce.set(4, res[1])
    iterator = 0
    while vce.isOpened():
        val, frame = vce.read()
        iterator += 1
        #process image
        if iterator > maxF: frame = undistortImage(pickingCam, frame)
        cv2.imwrite("logs/0-raw.jpg", frame) #log
        frame = frame[100:450, 300:550] # crop res: 350 x 250
        contour = getContour(frame)
        if contour is None: return p
        (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
        cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
        fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
        #log
        cv2.imwrite("logs/0-contours.jpg", fr)
        cv2.imshow("stream", fr)
        #prepare data
        xC = x*pxmm
        yC = y*pxmm
        angle = angle
        MA = MA*pxmm
        ma = ma*pxmm
        #relate robot base to work object (transform frames) an convert to metters
        x = (xR-yC)/1000
        y = (yR-xC)/1000
        z = (MA+30)/1000
        tinObj = {
            "x": x,
            "y": y,
            "angle": int(angle),
            "MA": int(MA),
            "ma": int(ma),
            }
        print(tinObj)
        log(str(str(x) +','+ str(y) +','+ str(int(angle)) +','+ str(int(MA)) +','+ str(int(ma))), "logs/cam_stabilization_data.txt")
        #close cam and return
        if iterator > maxF:
            if tinObj["ma"] < 20: return p
            log("tin data: " + str(tinObj), "logs/log.txt")
            vce.release()
            
            #
            rotationAngle = angle
            gripperOpening = int(MA+30)
            shortAxis = MA/1000
            #
            
            pose = [x, y, z, p["rx"], p["ry"], p["rz"]];
            return urlib.listToPose(pose);
            #return tinValList
        k=cv2.waitKey(1)
        if k==27: break
    
#seal validation / return: boolean
def requestSealValidation():
    print("seal validation request..")
    sleep(1)
    vcc = cv2.VideoCapture(sealCam)
    vcc.set(3, res[0])
    vcc.set(4, res[1])
    iterator = 20
    while vcc.isOpened():
        val, frame = vcc.read()
        iterator += 1
        sealValidation = False
        #process image
        if iterator > maxF: frame = undistortImage(sealCam, frame)
        cv2.imwrite("logs/2-raw.jpg", frame) #log
        frame = frame[100:450, 300:550] # crop res: 350 x 250
        contour = getContour(frame)
        if contour is None: return False
        (x,y),(MA,ma),angle = cv2.fitEllipse(contour) 
        cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
        fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
        if MA/ma > 0.975: sealValidation = True
        #log
        cv2.imwrite("logs/2-contours.jpg", frame)
        cv2.imshow("stream", fr)
        print(sealValidation)
        log(str(sealValidation), "logs/cam_stabilization_data.txt")
        #close cam and return
        if iterator > maxF:
            #if tinObj["ma"] < 10: return None
            log("seal: "+str(sealValidation), "logs/log.txt")
            vcc.release()
            return sealValidation
        k=cv2.waitKey(1)
        if k==27: break
    
#rfid validation / return boolean
def requestRFIDValidation():
    print("rfid validation request..")
    sleep(1)
    rfidValidation = reqRFIDValidation()         
    log("rfid: "+str(rfidValidation), "logs/log.txt")
    return rfidValidation

#update seal data / return - boolean
def updateTinData(sealVal):
    #reading in the card id 
    id, text = CardReader.read()
    CardReader.write(mineArea)
    print (id)
    print (text)
    datenow = datetime.now()
    datetimestamp = datenow.strftime('%Y-%m-%-d %H:%M:%S')
    con = sqlite3.connect('TinTrackingDB.db')
    cur = con.cursor()
    #tinfk= cur.lastrowid
    cur.execute("select Id from TinHistory where RFID=:rfid", {"rfid": id})
    tinfk= cur.lastrowid
    cur.execute("Update TinHistory(SealValidation) SET SealValidation=:SealVal where RFID=:rfid", {"SealVal": SealVal},{"rfid": id})
   #cur.execute("select Id from TinHistory where RFID=:rfid", {"rfid": id})
    tinfk=cur.fetchone()

#
def requestEmptyTinRotationAngle(): return rotationAngle
def requestEmptyTinGrippingWidth(): return gripperOpening
def requestEmptyTinShortAxis(p):
    z = shortAxis-gripperDown
    pose = [p["x"], ["y"], z, p["rx"], p["ry"], p["rz"]];
    return urlib.listToPose(pose);
#

def log(data, src):
    f = open(src, "a")
    f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), data))
    f.close()


    
    