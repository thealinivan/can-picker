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
from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio
from UpdateTin import updateTinData

import sys
import urlib

#cam src
pickingCam = 0
sealCam = 2
maxF = 50 #frames stabilization limit
res = [960, 1280] #frame resolution
pxmm = 1.08285 #px to mm conversiton rate
#pxmm = 0.92592
#robot work object coordinate in (mm)
xR = 1050
yR = 600
zR = 150
zOffset = 0

#default rotation
RX = 1.378
RY = 2.847
RZ = -0.007

#rfid scanner tollerance position
RFIDScannerTollerance = 0.043

#packing data
validPackingX = 0.95
notValidPackingX = 0.95
validPackingY = -0.381
notValidPackingY = -0.538
validTinCount = 0
notValidTinCount = 0
tinGap = 0.02
packingRX = 2.465
packingRY = -2.301
packingRZ = 2.439

#interfacing data
tinX = 0
tinY = 0
tinZ = 0
tinAngle = 0
tinMA = 0
tinma = 0
isTinPresent = False
sealValidation = False
gripperDown = 0.1
emptyTinPose = []
    
def runPickingCam():
    global emptyTinPose
    global tinX
    global tinY
    global tinZ
    global tinAngle
    global tinMA
    global tinma
    global isTinPresent
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
        if contour is None: return False
        (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
        cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
        cv2.ellipse(frame, (int(x), int(y)), (int(MA/2), int(ma/2)), int(angle), 0, 360, (0, 255, 0), 1)
        fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
        #log
        cv2.imwrite("logs/0-contours.jpg", fr)
        cv2.imshow("stream", fr)
        #coord conversion
        xC = x*pxmm
        yC = y*pxmm
        angle = angle
        MA = MA*pxmm
        ma = ma*pxmm
        #relate robot base to work object (transform frames) an convert to metters
        x = (xR-yC)/1000
        y = (yR-xC)/1000
        tinObj = {"x": x,"y": y,"angle": int(angle),"MA": int(MA),"ma": int(ma),}
        print(tinObj)
        log(str(str(x) +','+ str(y) +','+ str(int(angle)) +','+ str(int(MA)) +','+ str(int(ma))), "logs/cam_stabilization_data.txt")
        #write global interfacing data
        if iterator > maxF:
            tinX = x
            tinY = y
            tinZ = MA/1000
            tinAngle = int(angle)
            tinMA = MA/1000
            tinma = ma/1000
            log("tin data: " + str(tinObj), "logs/log.txt")
            vce.release()
            if tinObj["ma"] > 30: isTinPresent = True
            if tinObj["ma"] < 31: isTinPresent = False      
        k=cv2.waitKey(1)
        if k==27: break

def runCaningCam():
    global sealValidation
    sleep(1)
    vcc = cv2.VideoCapture(sealCam)
    vcc.set(3, res[0])
    vcc.set(4, res[1])
    iterator = 0
    while vcc.isOpened():
        val, frame = vcc.read()
        iterator += 1
        sealValidation = False
        #process image
        if iterator > maxF: frame = undistortImage(sealCam, frame)
        cv2.imwrite("logs/2-raw.jpg", frame) #log
        frame = frame[100:450, 300:550] # crop res: 350 x 250
        contour = getContour(frame)
        if contour is None: sealValidation = False
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
        #write global interfacing data
        if iterator > maxF:
            if tinma > 49: sealValidation = True
            if tinma < 50: sealValidation = False
            log("seal: "+str(sealValidation), "logs/log.txt")
            vcc.release()
            
        k=cv2.waitKey(1)
        if k==27: break

def requestIsEmptyTin():
    print("empty tin present..")
    runPickingCam()
    print(isTinPresent)
    return isTinPresent

def requestEmptyTinTopPose():
    print("empty tin top pose..")
    pose =  {"x":tinX, "y":tinY, "z":tinZ + 0.03, "rx":RX, "ry":RY, "rz":RZ}
    print(pose)
    return pose

def requestGripperRotationJointAngles(q, a):
    print("empty tin top pose..")
    jointAngles = [q[0], q[1], q[2], q[3], q[4], d2r(tinAngle + r2d(q[0]) + a)]
    print(jointAngles)
    return jointAngles

def requestEmptyTinScanPose(p):
    print("empty tin scan pose..")
    radius = tinMA/2
    scanZ = 0.2
    scanZ = (radius + (RFIDScannerTollerance - radius))
    pose = {"x":p["x"], "y":p["y"], "z":scanZ, "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose

def requestEmptyTinGrabPose(p):
    print("empty tin grab pose..")
    pose = {"x":p["x"], "y":p["y"], "z":(tinMA/2 - (tinMA/2*0.05)), "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose

def requestEmptyTinLeavePose(p):
    print("empty tin leave pose..")
    pose = {"x": p["x"], "y":p["y"], "z": 0.4, "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose

def requestCaningTopPose():
    print("canning top pose..")
    pose = {"x":0.88, "y":-0.014, "z":0.4 , "rx":2.465, "ry":-2.301, "rz":2.439}
    print(pose)
    return pose

def requestCaningScanPose(p):
    print("canning  scan pose...")
    radius = tinMA/2
    pose = {"x": ( p["x"] + (radius - RFIDScannerTollerance) ), "y":p["y"], "z": p["z"], "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose

def requestCaningGrabPose(p):
    print("canning grab pose..")
    pose = {"x": (p["x"]), "y":p["y"], "z": (tinma/2 - (tinMA*0.12)), "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose

def requestSealValidation():
    print("seal validation request..")
    runCaningCam()
    return sealValidation

def requestPackingValidTopNextPose():
    print("packing-valid top pose..")
    global validTinCount
    x = validPackingX - validTinCount*tinMA - validTinCount*tinGap
    validTinCount += 1
    pose = {"x": x, "y":validPackingY, "z": 0.4, "rx":packingRX, "ry":packingRY, "rz":packingRZ}
    print(pose)
    return pose
    
def requestPackingNotValidTopNextPose():
    print("packing-not-valid top pose..")
    global notValidTinCount
    x = notValidPackingX - notValidTinCount*tinMA - notValidTinCount*tinGap
    notValidTinCount += 1
    pose = {"x": x, "y":notValidPackingY, "z":0.4, "rx":packingRX, "ry":packingRY, "rz":packingRZ}
    print(pose)
    return pose

def requestPackingValidReleaseNextPose(p):
    print("packing-valid release pose..")
    pose = {"x": p["x"], "y":p["y"], "z":(tinma/2 - (tinma*0.12)), "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose
    
def requestPackingNotValidReleaseNextPose(p):
    print("packing-not-valid release pose..")
    pose = {"x": p["x"], "y":p["y"], "z":(tinma/2 - (tinma*0.12)), "rx":p["rx"], "ry":p["ry"], "rz":p["rz"]}
    print(pose)
    return pose
    

#rfid validation / return boolean
def requestRFIDValidation():
    print("rfid validation request..")
    rfidValidation = reqRFIDValidation()         
    log("rfid: "+str(rfidValidation), "logs/log.txt")
    return rfidValidation

#update seal data / return - boolean
def requestIsTinUpdated(sealVal):
    #reading in the card id
    print("update tin data..")
    tinUpdate = updateTinData(sealVal)         
    log("rfid: "+str(tinUpdate), "logs/log.txt")
    return tinUpdate

def log(data, src):
    f = open(src, "a")
    f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), data))
    f.close()
    
def d2r(d): return d*(pi/180)
def r2d(r): return r/(pi/180)


    
    