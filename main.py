import cv2
import numpy as np
from core import requestEmptyTin
from core import requestSealValidation
from core import requestRFIDValidation

print(requestEmptyTin())
print(requestSealValidation())
print(requestRFIDValidation())
