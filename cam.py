import cv2
from time import sleep
    
def openCam(src, h, w):
    #setup
    vc = cv2.VideoCapture(src)
    vc.set(3, h)
    vc.set(4, w)
    while vc.isOpened():
        #refresh rate
        sleep(1/100)
        #read and display frame
        rval, frame = vc.read()
        cv2.imshow("stream", frame) 
        #exit
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyWindow("stream")
    vc.release()
    

