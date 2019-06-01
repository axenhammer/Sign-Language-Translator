#!/usr/bin/env python3
# Universal Sign Language Translator
# Created by Team Axenhammer, https://github.com/Axenhammer
# Licensed as MIT

import numpy as np
import argparse
import glob
import sys
import cv2
# from PIL import Image

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return(edged)
    # return the edged image

def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True, help="path to input dataset of images")
    args = vars(ap.parse_args())
    # loop over the images
    for imagePath in glob.glob(args["images"] + "/*.jpeg"):
        # load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        # apply Canny edge detection using a wide threshold, tight
        # threshold, and automatically determined threshold
        wide = cv2.Canny(blurred, 10, 200)
        tight = cv2.Canny(blurred, 225, 250)
        auto = auto_canny(blurred)
        # show the images
        fName = imagePath.replace("target_folder_1","canny_edge")
        print("Storing: ", fName)
        # cv2.imwrite(fName , wid2e)
        cv2.imshow("Original", image)
        cv2.imshow("Edges", np.hstack([wide, tight, auto]))

        if cv2.waitKey(50) & 0xFF == ord("q"):
            break

if __name__ == '__main__':
    main()
