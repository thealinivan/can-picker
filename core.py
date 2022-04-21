import cv2
import numpy as np
from time import sleep
from datetime import datetime
from image_processing import getOrientation
from image_processing import getContour
from math import atan2, cos, sin, sqrt, pi
from visualization import visualiseTinPos

#empty tin
def requestEmptyTin():
    print("empty tin request..")
    sleep(1)
    vce = cv2.VideoCapture(0)
    vce.set(3, 960)
    vce.set(4, 1280)
    iterator = 0
    while vce.isOpened():
        val, frame = vce.read()
        iterator += 1
        #process image
        cv2.imwrite("logs/0-raw.jpg", frame) #log
        frame = frame[95:460, 290:555] # crop res: 365x265
        #frame = undistortImage(src, frame[95:460, 290:555])
        contour = getContour(frame)
        if contour is None: return
        (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
        cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
        fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
        #log
        cv2.imwrite("logs/0-contours.jpg", fr)
        cv2.imshow("stream", fr)
        tinObj = {
            "x": int(x),
            "y":int(y),
            "angle": int(angle),
            "MA": int(MA),
            "ma": int(ma),
            }
        print(tinObj)
        #close cam and return
        if iterator > 50:
            log(tinObj, "logs/log.txt")
            vce.release()
            return tinObj
        k=cv2.waitKey(1)
        if k==27: break
    
#seal validation
def requestSealValidation():
    print("seal validation request..")
    sleep(1)
    vcc = cv2.VideoCapture(2)
    vcc.set(3, 960)
    vcc.set(4, 1280)
    iterator = 20
    while vcc.isOpened():
        val, frame = vcc.read()
        iterator += 1
        sealValidation = False
        #process image
        cv2.imwrite("logs/2-raw.jpg", frame) #log
        frame= frame[145:510, 240:505]
        #frame = undistortImage(src, frame[145:510, 240:505])
        contour = getContour(frame)
        if contour is None: return None
        (x,y),(MA,ma),angle = cv2.fitEllipse(contour) 
        cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
        fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
        if MA/ma > 0.975: sealValidation = True
        #log
        cv2.imwrite("logs/2-contours.jpg", frame)
        cv2.imshow("stream", fr)
        print(sealValidation)
        #close cam and return
        if iterator > 50:
            log("seal: "+str(sealValidation), "logs/log.txt")
            vcc.release()
            return sealValidation
        k=cv2.waitKey(1)
        if k==27: break
    
#rfid validation
def requestRFIDValidation():
    print("rfid validation request..")
    sleep(1)
    rfidValidation = False
    #change it to true if..
    log("rfid: "+str(rfidValidation), "logs/log.txt")
    return rfidValidation

def log(data, src):
    f = open(src, "a")
    f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), data))
    f.close()
