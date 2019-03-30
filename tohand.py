import numpy as np
import cv2

"""
# Red and Green based on the dataset
boundary = [
            ([0, 120, 0], [140, 255, 100]),
            ([25, 0, 75], [180, 38, 255])
           ]

# Skin colour (maha)
boundary =  [
            ([115,67,49], [237,206,187]),
            ([180,157,139], [210,202,189])
            ]

# Skin colour (KK)
boundary =  [
            ([0,0,0],[147,120,120]),
            ([180,157,139], [210,202,189])
            ]
# Skin colour (Ajay)
boundary =  [
            ([129,117,104],[200,160,125]),
            ([0,0,0], [140,90,73])
            ]
"""
lower = np.array([0, 45, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

def handsegment(frame):
    #l, u = boundary[1]
    l = lower
    u = upper
    mask1 = cv2.inRange(frame, l, u)
    """
    l, u = boundary[1]
    l = np.array(l, dtype="uint8")
    u= np.array(u, dtype="uint8")
    mask2 = cv2.inRange(frame, l, u)
    mask = cv2.bitwise_or(mask1, mask2)
    """
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask=skinMask)
    return output

if __name__ == '__main__':
    frame = cv2.imread("test.jpeg")
    handsegment(frame)
