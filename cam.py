import cv2
from time import sleep

#close cam / args: VideoCapture - video capture
def closeCam(vc):
    vc.release()

#open Cam / args: int source, array - resolution / return: numpy array - image
def openCam(src, res):
    if src==0: print("picking cam active..")
    if src==2: print("caning cam active..")
    vc = cv2.VideoCapture(src)
    vc.set(3, res[0])
    vc.set(4, res[1])
    frames = []
    for i in range(0, 10):
        val, frame = vc.read()
        frames.append(frame)
    #log
    if src==0: cv2.imwrite("/home/pi/Desktop/can-picker/cam_logs/0-raw.jpg", frames[9])
    if src==2: cv2.imwrite("/home/pi/Desktop/can-picker/cam_logs/2-raw.jpg", frames[9])
    closeCam(vc)
    return frames[9]
        
        
  

    

    

