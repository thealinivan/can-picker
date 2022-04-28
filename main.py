import cv2
import numpy as np
from core import requestEmptyTin
from core import requestSealValidation
from core import requestRFIDValidation
from core import updateTinData
from core import requestEmptyTinGrippingWidth
from core import requestEmptyTinRotationAngle
from core import requestEmptyTinShortAxis

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

    server.register_function(requestEmptyTin, "requestEmptyTin")
    server.register_function(requestSealValidation, "requestSealValidation")
    server.register_function(requestRFIDValidation, "requestRFIDValidation")
    server.register_function(updateTinData, "updateTinData")
    
    #
    server.register_function(requestEmptyTinGrippingWidth, "requestEmptyTinGrippingWidth")
    server.register_function(requestEmptyTinRotationAngle, "requestEmptyTinRotationAngle")
    server.register_function(requestEmptyTinShortAxis, "requestEmptyTinShortAxis")
    #
    
    server.serve_forever()

runServer()

#print(requestEmptyTin())
#print(requestSealValidation())
#print(requestRFIDValidation())
