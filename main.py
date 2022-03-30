import cv2
import numpy as np
from cam import openCam
from empty_tin import getEmptyTin
from seal_validation import getSealValidation
from ur10_interface import sendEmptyTinData
from ur10_interface import sendSealValidation
from cam import closeCam
from image_processing import getOrientation
from image_processing import getContours
from math import atan2, cos, sin, sqrt, pi

#setup
res = [960, 1280]

def start():
    recycle = True
    while recycle:
        #empty tin
        emptyTin = None
        while emptyTin == None:
            emptyTin = getEmptyTin(openCam(0, res))
        sendEmptyTinData(emptyTin)
        
        #seal validation
        sealValid = None
        while sealValid == None:
            sealValid = getSealValidation(openCam(2, res))
        sendSealValidation(sealValid)
        
        #dev only - recycle
        print("== Re-cycle? y/n ==")
        opt = input("::")
        if opt == "n": recycle = False   

#start()
        
        
def dev():
    vc = cv2.VideoCapture(0)
    vc.set(3, res[0])
    vc.set(4, res[1])
    while vc.isOpened():
        val, frame = vc.read() 
        # sm tin: 131x69 # big tin:
        simET(frame)
        #simCT(frame)
        k = cv2.waitKey(1)
        if k==27: break
    closeCam(vc)

def simET(frame):
    #EMPTY TIN
    frame = frame[95:460, 290:555] # crop res: 365x265
    #get data
    contours = getContours(frame)
    #if contours is None: return
    (x,y),(MA,ma),angle = cv2.fitEllipse(contours[0])
    cntr, img, eigenvectors, eigenvalues = getOrientation(contours[0], frame)
    #log data
    print("x: " + str(int(x)))
    print("y: " + str(int(y)))
    print("angle: " + str(int(angle)))
    print("Major Axis: " + str(int(MA)))
    print("minor axis: " + str(int(ma)))
    print("")
    #visualise data
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    cv2.imshow("stream", visualiseTinPos(cntr, frame, eigenvectors, eigenvalues))

def simCT(frame):
    #CANNING TIN
    frame = frame[145:510, 240:505] # crop res: 365x265
    #get data
    contours = getContours(frame)
    if contours is None: return
    (x,y),(MA,ma),angle = cv2.fitEllipse(contours[0])
    cntr, img, eigenvectors, eigenvalues = getOrientation(contours[0], frame)
    #log data
    print("x: " + str(int(x)))
    print("y: " + str(int(y)))
    print("angle: " + str(int(angle)))
    print("Major Axis: " + str(int(MA)))
    print("minor axis: " + str(int(ma)))
    print("")
    #visualise data
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    cv2.imshow("stream", visualiseTinPos(cntr, frame, eigenvectors, eigenvalues))
    
#visualisation - axis
def drawAxis(img, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
  ## [visualization1]
  angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
  hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * cos(angle)
  q[1] = p[1] - scale * hypotenuse * sin(angle)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  # create the arrow hooks
  p[0] = q[0] + 9 * cos(angle + pi / 4)
  p[1] = q[1] + 9 * sin(angle + pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  p[0] = q[0] + 9 * cos(angle - pi / 4)
  p[1] = q[1] + 9 * sin(angle - pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  ## [visualization1]

#viz
def visualiseTinPos(cntr, img, eigenvectors, eigenvalues):
    ## [visualization]
    # Draw the principal components
    cv2.circle(img, cntr, 7, (255, 0, 255), 1)
    p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
    p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
    drawAxis(img, cntr, p1, (255, 255, 0), 2)
    drawAxis(img, cntr, p2, (0, 0, 255), 2)
    angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    ## [visualization]
    # Label with the rotation angle
    rotationAngle = str(-int(np.rad2deg(angle)) - 90)
    for alpha in np.arange(0, 1.1, 0.1)[::-1]:
      overlay = img.copy()
      output = img.copy()
    label = " " + str(rotationAngle)
    textbox = cv2.rectangle(overlay, (420, 205), (595, 385), (0, 0, 0), -1)
    cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    return img
  
dev() 