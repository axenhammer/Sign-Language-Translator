#!/usr/bin/env python3
# Universal Sign Language Translator
# Created by Team Axenhammer, https://github.com/Axenhammer
# Licensed as MIT

import os
from os.path import join, exists
from tqdm import tqdm
import tohand as th
import find_total_frames as ftf
import numpy as np
import cv2
import pickle
import argparse

hc = []
# assumption only first @default_fps frames are important
default_fps = fps = 183 # most test cases fall under 183 frames
full_load = False # Process only upto @default_fps frames in a video
# Uncomment the below line if you want to process every frame (Might cause huge runtimes)
# full_load = True # Process every frame in a video

# Perform Auto Canny in automatic mode
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return(edged)
    # return the edged image


# Extract Edges from Hand Frames
def convertToEdge(gesture_folder, target_folder, swap_):
    rP = os.getcwd()
    mData = os.path.abspath(target_folder)
    if not exists(mData):
        os.makedirs(mData)
    gesture_folder = os.path.abspath(gesture_folder)
    os.chdir(gesture_folder)
    gestures = os.listdir(os.getcwd())
    print("Source Directory containing gestures: %s" % (gesture_folder))
    print("Destination Directory containing frames: %s\n" % (mData))
    for gesture in tqdm(gestures, unit='actions', ascii=True):
        gesture_path = os.path.join(gesture_folder, gesture)
        os.chdir(gesture_path)
        gesture_frames_path = os.path.join(mData, gesture)
        if not os.path.exists(gesture_frames_path):
            os.makedirs(gesture_frames_path)
        framedir = os.listdir(os.getcwd())
        for imagePath in framedir:
            if(imagePath.endswith(".jpeg") or imagePath.endswith(".jpg")):
                fName = (os.getcwd()+ "\\" +imagePath)
                fName = fName.replace(swap_,target_folder)
                print("Extracting edges in ",fName)
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
                # fName = mData + "\\" + imagePath
                # print("Storing: ", fName)
                cv2.imwrite(fName , wide)
                #cv2.imshow("Original", image)
                #cv2.imshow("Edges", np.hstack([wide, tight, auto]))


# Extract Hands from Frames
def convertToHand(gesture_folder, target_folder):
    rP = os.getcwd()
    mData = os.path.abspath(target_folder)
    if not exists(mData):
        os.makedirs(mData)
    gesture_folder = os.path.abspath(gesture_folder)
    os.chdir(gesture_folder)
    gestures = os.listdir(os.getcwd())
    print("Source Directory containing gestures: %s" % (gesture_folder))
    print("Destination Directory containing frames: %s\n" % (mData))
    for gesture in tqdm(gestures, unit='actions', ascii=True):
        #gesture_path = os.path.join(gesture_folder, gesture)
        gesture_path = gesture_folder
        #print(gesture_folder)
        os.chdir(gesture_path)
        gesture_frames_path = os.path.join(mData, gesture)
        if not os.path.exists(gesture_frames_path):
            os.makedirs(gesture_frames_path)
        videos = os.listdir(os.getcwd())
        videos = [video for video in videos if(os.path.isfile(video))]
        for video in tqdm(videos, unit='videos', ascii=True):
            name = os.path.abspath(video)
            cap = cv2.VideoCapture(name)  # capturing input video
            frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            lastFrame = None
            os.chdir(gesture_frames_path)
            count = 0
            if full_load:
                fps = default_fps
                fps = ftf.find_frames(name)
            # assumption only first @fps frames are important
            while count < fps:
                ret, f = cap.read()  # extract frame
                if ret is False:
                    break
                fName = os.path.splitext(video)[0]
                fName = fName + "_frame_" + str(count) + ".jpeg"
                hc.append([join(gesture_frames_path, fName), gesture, frameCount])

                if not os.path.exists(fName):
                    f = th.handsegment(f)
                    lastFrame = f
                    cv2.imwrite(fName, f)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                count += 1
            # repeat last frame untill we @fps value is reached (Exception/ if full_load = False)
            while count < fps:
                fName = os.path.splitext(video)[0]
                fName = fName + "_frame_" + str(count) + ".jpeg"
                hc.append([join(gesture_frames_path, fName), gesture, frameCount])
                if not os.path.exists(fName):
                    cv2.imwrite(fName, lastFrame)
                count += 1
            os.chdir(gesture_path)
            cap.release()
            cv2.destroyAllWindows()
    os.chdir(rP)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Individual Frames from gesture videos.')
    parser.add_argument('gesture_folder', help='folders of videos of different gestures.')
    parser.add_argument('target_folder', help='folder where extracted frames should be kept.')
    parser.add_argument('final_folder', help='folder where the final edge frames should be kept.')
    #parser.add_argument('sum_folder', help='folder where the summated frames should be kept.')

    args = parser.parse_args()
    convertToHand(args.gesture_folder, args.target_folder)
    convertToEdge(args.target_folder, args.final_folder, args.target_folder)
    #summateEdge(args.final_folder, args.sum_folder, args.target_folder)
