import cv2
import numpy as np
from core import requestRFIDValidation
from core import updateTinData
from core import requestIsEmptyTin
from core import requestEmptyTinTopPose
from core import requestGripperRotationJointAngles
from core import requestEmptyTinGrabPose
from core import requestCaningTopPose
from core import requestCaningGrabPose
from core import requestSealValidation
from core import requestPackingValidTopNextPose
from core import requestPackingValidReleaseNextPose  
from core import requestPackingNotValidTopNextPose
from core import requestPackingNotValidReleaseNextPose
from core import requestEmptyTinLeavePose

import sys
import urlib

is_py2 = sys.version[0] == '2'
if is_py2: from SimpleXMLRPCServer import SimpleXMLRPCServer
if not is_py2: from xmlrpc.server import SimpleXMLRPCServer

PORT = 50001
HOST = ""   

def runServer():
    server = SimpleXMLRPCServer((HOST, PORT))
    server.RequestHandlerClass.protocol_version = "HTTP/1.1"
    print("Listening on port " + str(PORT) + "...")
    
    server.register_function(requestRFIDValidation, "requestRFIDValidation")
    server.register_function(updateTinData, "updateTinData")
    server.register_function(requestIsEmptyTin, "requestIsEmptyTin")
    server.register_function(requestEmptyTinTopPose, "requestEmptyTinTopPose")
    server.register_function(requestGripperRotationJointAngles, "requestGripperRotationJointAngles")
    server.register_function(requestEmptyTinGrabPose, "requestEmptyTinGrabPose")
    server.register_function(requestCaningTopPose, "requestCaningTopPose")
    server.register_function(requestCaningGrabPose, "requestCaningGrabPose")
    server.register_function(requestSealValidation, "requestSealValidation")
    server.register_function(requestPackingValidTopNextPose, "requestPackingValidTopNextPose")
    server.register_function(requestPackingValidReleaseNextPose, "requestPackingValidReleaseNextPose")
    server.register_function(requestPackingNotValidTopNextPose, "requestPackingNotValidTopNextPose")
    server.register_function(requestPackingNotValidReleaseNextPose, "requestPackingNotValidReleaseNextPose")
    server.register_function(requestEmptyTinLeavePose, "requestEmptyTinLeavePose")
    
    server.serve_forever()

runServer()
