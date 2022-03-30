import cv2
from time import sleep
from image_processing import getContours

#open Cam / args: int source, array - resolution / return: array - ???data
def getEmptyTin(frame):
    print("getting empty tin data..")
    sleep(2)
    frame = frame[95:460, 290:555]
    contours = getContours(frame)
    if contours is None: return None
    (x,y),(MA,ma),angle = cv2.fitEllipse(contours[0])
    emptyTin = [int(x), int(y), int(angle), int(MA), int(ma)]
    tin = {
        "x": int(x),
        "y":int(y),
        "angle": int(angle),
        "MA": int(MA),
        "ma": int(ma),
        }  
    return emptyTin
    

    

