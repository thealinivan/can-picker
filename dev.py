import cv2
import numpy as np
from cam import openCam
from empty_tin import getEmptyTin
from seal_validation import getSealValidation
from cam import closeCam
from image_processing import getOrientation
from image_processing import getContour
from math import atan2, cos, sin, sqrt, pi
from ur10_interface import requestEmptyTinData
from ur10_interface import requestSealValidation
from rfid_validation import getRFIDValidation
from ur10_interface import requestRFIDValidation
from visualization import visualiseTinPos
import sys

res = [960, 1280]
src = int(sys.argv[1])

def dev(src):
    vc = cv2.VideoCapture(src)
    vc.set(3, res[0])
    vc.set(4, res[1])
    while vc.isOpened():
        val, frame = vc.read()
        if src==0: simET(frame)
        if src==2: simCT(frame)
        k=cv2.waitKey(1)
        if k==27: break
    closeCam(vc)
    
def simET(frame):
    frame = frame[95:460, 290:555] # crop res: 365x265
    contour = getContour(frame)
    if contour is None: return
    (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
    cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
    prinData()
    cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
    fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
    cv2.imshow("stream", fr)

def simCT(frame):
    frame = frame[145:510, 240:505] # crop res: 365x265
    contour = getContour(frame)
    if contour is None: return
    (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
    cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
    printData(x, y, angle, MA, ma)
    cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
    fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
    cv2.imshow("stream", fr)
    
def printData(x, y, angle, MA, ma):
    print("x: " + str(int(x)))
    print("y: " + str(int(y)))
    print("angle: " + str(int(angle)))
    print("Major Axis: " + str(int(MA)))
    print("minor axis: " + str(int(ma)))
    print("")
    
dev(src)
