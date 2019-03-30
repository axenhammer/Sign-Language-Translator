import numpy as np
import cv2
boundary = [([0, 120, 0], [140, 255, 100]),([25, 0, 75], [180, 38, 255])]


def handsegment(frame):
    l, u = boundary[0]
    l = np.array(l, dtype="uint8")
    u = np.array(u, dtype="uint8")
    mask1 = cv2.inRange(frame, l, u)

    l, u = boundary[1]
    l = np.array(l, dtype="uint8")
    u= np.array(u, dtype="uint8")
    mask2 = cv2.inRange(frame, l, u)
    mask = cv2.bitwise_or(mask1, mask2)
    output = cv2.bitwise_and(frame, frame, mask=mask)
    return output

if __name__ == '__main__':
    frame = cv2.imread("test.jpeg")
    handsegment(frame)
0
