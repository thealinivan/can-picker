import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi

#get  orientation / args: numpy array - contour, numpy array - image
def getOrientation(pts, img):
  ## [pca]
  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]
  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
  # Store the center of the object
  cntr = (int(mean[0,0]), int(mean[0,1]))
  return [cntr, img, eigenvectors, eigenvalues]
    
#get contours / args: numpy array - image / return numpy array - contours
def getContours(frame):
    cont = None
    mono = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(mono, (5, 5))
    val, th = cv2.threshold(blur, 110, 255, cv2.THRESH_BINARY)
    #th = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2. THRESH_BINARY,11, 2)
    kernel = np.ones((5, 5), np.uint8)
    close = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    canny = cv2.Canny(close, 100, 200)
    cont, h = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if len(cont) < 1: cont = None
    return cont

