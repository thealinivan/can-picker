import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi

#axis
def drawAxis(img, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
  ## [visualization1]
  angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
  hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * cos(angle)
  q[1] = p[1] - scale * hypotenuse * sin(angle)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  # create the arrow hooks
  p[0] = q[0] + 9 * cos(angle + pi / 4)
  p[1] = q[1] + 9 * sin(angle + pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  p[0] = q[0] + 9 * cos(angle - pi / 4)
  p[1] = q[1] + 9 * sin(angle - pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  ## [visualization1]

#get  orientation / args: int - points, numpy array - image
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
  ## [pca]
  ## [visualization]
  # Draw the principal components
  cv2.circle(img, cntr, 3, (255, 0, 255), 2)
  p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
  p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
  drawAxis(img, cntr, p1, (255, 255, 0), 1)
  drawAxis(img, cntr, p2, (0, 0, 255), 5)
  angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
  ## [visualization]
  # Label with the rotation angle
  rotationAngle = str(-int(np.rad2deg(angle)) - 90)
  label = " " + str(rotationAngle)
  textbox = cv2.rectangle(img, (cntr[0], cntr[1]-25), (cntr[0] + 50, cntr[1] + 10), (255,255,255), -1)
  cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
  return rotationAngle
    
#get contours / args: numpy array - image / return numpy array - contours
def getContours(frame):
    mono = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(mono, (5, 5))
    val, th = cv2.threshold(blur, 110, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    close = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    canny = cv2.Canny(close, 100, 200)
    cont, h = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame, cont, -1, (0, 255, 0), 1)
    return cont

#get angle / aergs: numpy array - frame, numpy array - contours / return: array - angles
def getAngle(frame, contours):
    angles = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 4000 or 90000 < area: continue
        cv2.drawContours(frame, contours, i, (0, 255, 0), 2)
        angles.append(getOrientation(c, frame))
    return angles
