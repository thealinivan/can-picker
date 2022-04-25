import cv2
import numpy as np
from core import requestEmptyTin
from core import requestSealValidation
from core import requestRFIDValidation
from core import updateTinData

import sys
import urlib

is_py2 = sys.version[0] == '2'
if is_py2: from SimpleXMLRPCServer import SimpleXMLRPCServer
if not is_py2: from xmlrpc.server import SimpleXMLRPCServer

PORT = 50001
HOST = ""

#test function
def get_next_pose(p):
    assert type(p) is dict
    pose = urlib.poseToList(p)
    print("Received pose: " + str(pose))
    pose = [-0.18, -0.61, 0.23, 0, 3.12, 0.04];
    return urlib.listToPose(pose);    

def runServer():
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

print(requestEmptyTin())
print(requestSealValidation())
print(requestRFIDValidation())
