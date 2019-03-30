#!/usr/bin/python3
import cv2
import numpy as np
import copy
import math

# Environment:
# OS    : Win32
# python: 3
# opencv: 3.4.0


def calculateFingers(res, drawing):
    #  convexity defect
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if defects is not None:
            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            if cnt > 0:
                return True, cnt+1
            else:
                return True, 0
    return False, 0


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

    # Getting the contours and convex hull
    skinMask1 = copy.deepcopy(skinMask)
    _,contours, hierarchy = cv2.findContours(skinMask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    maxArea = -1
    if length > 0:
        for i in range(length):
            temp = contours[i]
            area = cv2.contourArea(temp)
            if area > maxArea:
                maxArea = area
                ci = i

        res = contours[ci]
        hull = cv2.convexHull(res)
        drawing = np.zeros(img.shape, np.uint8)
        cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

        isFinishCal, cnt = calculateFingers(res, drawing)
        print ("Fingers", cnt)
        cv2.imshow('output', drawing)

    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
