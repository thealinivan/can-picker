import cv2
import numpy as np
from core import requestEmptyTin
from core import requestSealValidation
from core import requestRFIDValidation

import sys
import urlib

is_py2 = sys.version[0] == '2'
if is_py2: from SimpleXMLRPCServer import SimpleXMLRPCServer
if not is_py2: from xmlrpc.server import SimpleXMLRPCServer

def get_next_pose(p):
    assert type(p) is dict
    pose = urlib.poseToList(p)
    print("Received pose: " + str(pose))
    pose = [-0.18, -0.61, 0.23, 0, 3.12, 0.04];
    return urlib.listToPose(pose);
    #return "Walabila!"    
    
server = SimpleXMLRPCServer(("localhost", 50000))
server.RequestHandlerClass.protocol_version = "HTTP/1.1"
print("Listening on port 50000...")

server.register_function(get_next_pose, "get_next_pose")
server.register_function(requestEmptyTin, "requestEmptyTin")
server.register_function(requestSealValidation, "requestSealValidation")
server.register_function(requestRFIDValidation, "requestRFIDValidation")

server.serve_forever()


#print(requestEmptyTin())
#print(requestSealValidation())
#print(requestRFIDValidation())
