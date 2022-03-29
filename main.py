import cv2
import numpy as np
from cam import openCam
from empty_tin import getEmptyTin
from seal_validation import getSealValidation
from ur10_interface import sendEmptyTinData
from ur10_interface import sendSealValidation
from cam import closeCam
from image_processing import getAngle

from math import atan2, cos, sin, sqrt, pi


#init cam
recycle = True
res = [960, 1280]

def start():
    while recycle == True:
        #empty tin
        emptyTin = None
        while emptyTin == None:
            emptyTin = getEmptyTin(openCam(2, res))
        sendEmptyTinData(emptyTin)
        
        #seal validation
        sealValid = None
        while sealValid == None:
            sealValid = getSealValidation(openCam(4, res))
        sendSealValidation(sealValid)
        
        #dev only - recycle
        print("== Re-cycle? y/n ==")
        opt = input("::")
        if opt == "n": recycle = False   

#start()
        


    
def dev():
    vc = cv2.VideoCapture(2)
    vc.set(3, res[0])
    vc.set(4, res[1])
    while vc.isOpened():
        val, frame = vc.read()
        
        
        ##crop
        frame = frame[95:460, 290:555]
        
        ##contours
        from image_processing import getContours
        contours = getContours(frame)
        
        #orientation
        angles = getAngle(frame, contours)
        print(angles)        

        cv2.imshow("stream", frame)
        k = cv2.waitKey(1)
        if k==27: break
    closeCam(vc)
    
    
    
def parked():
    #mono + threshold
    img = frame[95:460, 290:555]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img,5)
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    #contours
    mono = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(mono, (5, 5))
    val, th = cv2.threshold(blur, 110, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    close = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    canny = cv2.Canny(close, 100, 200)
    cont, h = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, cont, -1, (0, 255, 0), 1)
dev()
    



    

    






