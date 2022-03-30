import cv2
from time import sleep
from image_processing import getContours

#get seal validation / args: numpy array - image / return: boolean - seal validation
def getSealValidation(frame):
    print("getting seal validation..")
    sleep(2)
    frame = frame[145:510, 240:505]
    contours = getContours(frame)
    if len(contours) < 1: return None
    (x,y),(MA,ma),angle = cv2.fitEllipse(contours[0])
    
    sealValidation = True
    
    return sealValidation
    

    

