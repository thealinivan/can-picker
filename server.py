import cv2
import numpy as np
#from core import requestEmptyTin
#from core import requestSealValidation
#from core import requestRFIDValidation
#from core import updateTinData

import sys
import urlib

is_py2 = sys.version[0] == '2'
if is_py2: from SimpleXMLRPCServer import SimpleXMLRPCServer
if not is_py2: from xmlrpc.server import SimpleXMLRPCServer

PORT = 50001
HOST = ""
#robot work object coordinate in (mm)
xR = 1035
yR = 609

#test function
def get_next_pose(p):
    assert type(p) is dict
    pose = urlib.poseToList(p)
    print("Received pose: " + str(pose))
    pose = [-0.18, -0.61, 0.23, 0, 3.12, 0.04];
    return urlib.listToPose(pose);

def requestEmptyTin(p):
    xC = 153
    yC = 205
    x = (xR-yC)/1000
    y = (yR-xC)/1000
    #covert mm to meter as the UR10 manual prescribes
    assert type(p) is dict
    pose = urlib.poseToList(p)
    print("Received pose: " + str(pose))
    pose = [x, y, 0.14017, 1.37, 2.83, 0.022];
    return urlib.listToPose(pose);

    
def requestRFIDValidation():
    rFID = True
    return rFID;
    
def updateTinData():
    tinData = True
    return tinData;
    
def requestSealValidation():
    sealVal= True
    return sealVal;


server = SimpleXMLRPCServer((HOST, PORT))
server.RequestHandlerClass.protocol_version = "HTTP/1.1"
print("Listening on port " + str(PORT) + "...")

server.register_function(get_next_pose, "get_next_pose")
server.register_function(requestEmptyTin, "requestEmptyTin")
server.register_function(requestSealValidation, "requestSealValidation")
server.register_function(requestRFIDValidation, "requestRFIDValidation")
server.register_function(updateTinData, "updateTinData")
server.serve_forever()

#runServer()