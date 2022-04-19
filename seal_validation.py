import cv2
from time import sleep
from image_processing import getContour
from image_processing import getOrientation
from visualization import visualiseTinPos
from camera_calibration import undistortImage

#get seal validation / args: numpy array - image / return: boolean - seal validation
def getSealValidation(src, frame):
    print("getting seal validation..")
    #frame = undistortImage(src, frame[145:510, 240:505])
    frame= frame[145:510, 240:505]
    contour = getContour(frame)
    if contour is None: return None
    (x,y),(MA,ma),angle = cv2.fitEllipse(contour) 
    sealValidation = False
    axisRatio = MA/ma
    if axisRatio > 0.975: sealValidation = True
    #log
    cntr, img, eigenvectors, eigenvalues = getOrientation(contour, frame)
    cv2.drawContours(frame, contour, -1, (0, 255, 0), 1)
    fr = visualiseTinPos(angle, cntr, frame, eigenvectors, eigenvalues)
    cv2.imwrite("/home/pi/Desktop/can-picker/cam_logs/2-contours.jpg", fr)
    return sealValidation
    

    

