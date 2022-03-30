import cv2
from time import sleep

#close cam / args: VideoCapture - video capture
def closeCam(vc):
    cv2.destroyWindow("stream")
    vc.release()

#open Cam / args: int source, array - resolution / return: numpy array - image
def openCam(src, res):
    if src==0: print("picking cam active..")
    if src==2: print("caning cam active..")
    #sleep(2)
    vc = cv2.VideoCapture(src)
    vc.set(3, res[0])
    vc.set(4, res[1])
    val, frame = vc.read()
    cv2.imshow("stream", frame)
    sleep(2)
    closeCam(vc)
    return frame
        
        
  

    

    

