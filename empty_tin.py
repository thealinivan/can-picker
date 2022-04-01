import cv2
from time import sleep
from image_processing import getContour
from visualization import visualiseTinPos
from image_processing import getOrientation

#open Cam / args: int source, array - resolution / return: array - ???data
def getEmptyTin(frame):
    print("getting empty tin data..")
    frame = frame[95:460, 290:555]
    contour = getContour(frame)
    if contour is None: return None
    (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
    tinArray= [int(x), int(y), int(angle), int(MA), int(ma)]
    tinObj = {
        "x": int(x),
        "y":int(y),
        "angle": int(angle),
        "MA": int(MA),
        "ma": int(ma),
        }
    #log
    cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
    cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
    fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
    cv2.imwrite("/home/pi/Desktop/can-picker/cam_logs/0-contours.jpg", fr)
    return tinObj
    

    

