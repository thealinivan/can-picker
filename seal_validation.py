import cv2
from time import sleep
from image_processing import getContours
from image_processing import getAngle

#get seal validation / args: numpy array - image / return: boolean - seal validation
def getSealValidation(frame):
    print("getting seal validation..")
    sleep(2)
    
    frame = frame[145:510, 240:505]
    frame = getContours(frame)
    
    sealValidation = True
    
    return sealValidation
    

    

