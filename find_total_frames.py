#!/usr/bin/env python3
# Find total number of frames in a video (overrides default value)

import cv2

def find_frames(path):
    cap = cv2.VideoCapture(path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return(length)

if __name__ == '__main__':
    # Test case "ASL Lesson 1.mp4" has 12906 Frames
    test_location = ("in\\ASL Lesson 1.mp4");
    print(test_location, "has", find_frames(test_location),"frames.")
