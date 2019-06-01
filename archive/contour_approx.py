#!/usr/bin/env python3
# Universal Sign Language Translator
# Created by Team Axenhammer, https://github.com/Axenhammer
# Licensed as MIT

from matplotlib import pyplot as plt
import cv2
import numpy as np
import argparse
import glob

path = "C:\\Users\\Krishna_Alagiri\\Projects\\sign-lang-trans\\target_folder\\kk-best\\kk_frame_0.jpeg"
img = cv2.imread(path)
grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

(ret, thresh) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
edge = cv2.Canny(thresh, 100, 200)
(cnts, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


total = 0
for c in cnts:
    epsilon = 0.08 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    cv2.drawContours(img, [approx], -1, (0, 255, 0), 4)
    total += 1

print ("I found {0} RET in that image".format(total))
cv2.imshow("Output", img)
cv2.waitKey(0)
exit()
