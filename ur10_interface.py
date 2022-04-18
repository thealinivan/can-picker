import cv2
from time import sleep

#send empty tin data / args: array - empty tin data
def requestEmptyTinData(data):
    print("sending empty tin data..")
    print(data)
    
#send seal validation / args: boolean - validation
def requestSealValidation(validation):
    print("sending seal validation..")
    print(validation)
    
#send rfid validation / args: boolean - validation
def requestRFIDValidation(validation):
    print("sending rfid validation..")
    print(validation)
