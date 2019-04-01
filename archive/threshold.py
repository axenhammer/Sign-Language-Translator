import cv2
import numpy as np
import copy
import math

# Open Camera
camera = cv2.VideoCapture(0)
camera.set(10, 200)

while camera.isOpened():
    #Main Camera
    ret, frame = camera.read()
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
    frame = cv2.flip(frame, 1)  #Horizontal Flip
    cv2.imshow('original', frame)


    #Background Removal
    bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
    fgmask = bgModel.apply(frame)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    img = cv2.bitwise_and(frame, frame, mask=fgmask)

    # Skin detect and thresholding
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skinMask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('Threshold Hands', skinMask)

    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
