import cv2
import numpy as np
from cam import openCam
from empty_tin import getEmptyTin
from seal_validation import getSealValidation
from rfid_validation import getRFIDValidation
from ur10_interface import requestEmptyTinData
from ur10_interface import requestSealValidation
from ur10_interface import requestRFIDValidation

#setup
res = [960, 1280]

def start():
    while True:
        print("")
        #empty tin
        emptyTin = None
        while emptyTin == None:
            emptyTin = getEmptyTin(0, openCam(0, res))
        requestEmptyTinData(emptyTin)
        
        #RFID validation
        RFIDValid = None
        while RFIDValid == None:
            RFIDValid = getRFIDValidation()
        requestRFIDValidation(RFIDValid)
        
        #seal validation
        sealValid = None
        while sealValid == None:
            sealValid = getSealValidation(2, openCam(2, res))
        requestSealValidation(sealValid)
        
        #RFID validation
        RFIDValid = None
        while RFIDValid == None:
            RFIDValid = getRFIDValidation()
        requestRFIDValidation(RFIDValid)
        
start()
   