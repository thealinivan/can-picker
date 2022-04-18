import cv2
from time import sleep

#close cam / args: VideoCapture - video capture
def closeCam(vc):
    vc.release()
res = [960, 1280]
#open Cam / args: int source, array - resolution / return: numpy array - image
def openCam(src, res):
    vc = cv2.VideoCapture(src)
    vc.set(3, res[0])
    vc.set(4, res[1])
    while vc.isOpened():
        for i in range (0, 17):
            sleep(2)
            val, frame = vc.read()
            if src==0: frame = frame[95:460, 290:555]
            if src==2: frame = frame[145:510, 240:505]
            #if i>5: cv2.imwrite("/home/pi/Desktop/can-picker/camera_calibration/"+str(src)+"/"+ str(i-6) +".jpg", frame)
            print("Screnshot "+ str(i))
            sleep(1)
            print("Get ready..")
        closeCam(vc)
        
openCam(2 , res)
  

    

    

