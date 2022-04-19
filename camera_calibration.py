#!/usr/bin/env python
import cv2
import numpy as np
import cv2 as cv
import glob
from time import sleep

def calibrateCam(src):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('/home/pi/Desktop/can-picker/camera_calibration/'+ str(src)+'/*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7,10), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (7,6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(27)
    cv.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return [mtx, dist]
    
def undistortImage(src, img):
    mtx, dist = calibrateCam(src)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2getOptimalNewCameraMatrix()
    undst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    undst = dst[y:y+h, x:x+w]
    return undst
    
    
    

    