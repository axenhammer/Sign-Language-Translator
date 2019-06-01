#!/usr/bin/env python3
# Universal Sign Language Translator
# Created by Team Axenhammer, https://github.com/Axenhammer
# Licensed as MIT

from matplotlib import pyplot as plt
import numpy as np
import cv2

debug = True

lower = np.array([0, 45, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return(edged)
    # return the edged image

def edgedetection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # apply Canny edge detection using a wide threshold, tight
    # threshold, and automatically determined threshold
    wide = cv2.Canny(blurred, 10, 200)
    tight = cv2.Canny(blurred, 225, 250)
    auto = auto_canny(blurred)
    if debug == True:
        cv2.imshow("Edges", wide)
    return wide

if __name__ == '__main__':
    path__ = "C:\\Users\\Krishna_Alagiri\\Projects\\sign-lang-trans\\Trainer\\target_folder_1\\Accept\\050_001_001_frame_31.jpeg"
    frame = cv2.imread(path__)
    test = edgedetection(frame)
    cv2.imshow("Edges", test)
    k = cv2.waitKey(10000)
