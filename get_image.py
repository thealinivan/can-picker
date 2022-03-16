import picamera
from time import sleep
import numpy as np
import math as m

def getNormRes(res):
    normRes = {"x": 32, "y": 16}
    i = 16
    targetX = 0
    targetY = 0
    while targetX < res["x"]: targetX += i*2
    while targetY < res["y"]: targetY += i
    lowX = int(targetX/(i*2)) * (i*2)
    highX = int((targetX/(i*2) + 1)) * (i*2)
    lowY = int(targetY/i) * i
    highY = int((targetY/i + 1)) * i
    if targetX < (lowX+highX)/2:
        if lowX < 64: lowX = 64
        normRes["x"] = lowX
    else:normRes["x"] = highX
    if targetY < int((lowY+highY)/2):
        if lowY < 64: lowY = 64
        normRes["y"] = lowY
    else:normRes["y"] = highY
    return normRes
    
       
def getImage(inputRes):
    res = getNormRes(inputRes)
    with picamera.PiCamera() as cam:
        cam.resolution = (res["x"], res["y"])
        cam.framerate = 24
        output = np.empty((res["x"], res["y"], 3), dtype=np.uint8)
        cam.capture(output, 'rgb')
        output = output[:inputRes["x"], :inputRes["y"], :]
    return output
