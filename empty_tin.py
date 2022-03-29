import cv2
from time import sleep
from image_processing import getContours
from image_processing import getAngle

#open Cam / args: int source, array - resolution / return: array - ???data
def getEmptyTin(frame):
    print("getting empty tin data..")
    sleep(2)
    
    #crop
    frame = frame[95:460, 290:555]
    contours = getContours(frame)
    angle = getAngle(frame, contours)
    
    emptyTin = [13, 45]
    
    return emptyTin
    

    

