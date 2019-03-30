import cv2
import os
import pickle
from os.path import join, exists
import tohand as th
import argparse
from tqdm import tqdm

hc = []


def convert(gesture_folder, target_folder):
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

        videos = os.listdir(os.getcwd())
        videos = [video for video in videos if(os.path.isfile(video))]

        for video in tqdm(videos, unit='videos', ascii=True):
            name = os.path.abspath(video)
            cap = cv2.VideoCapture(name)  # capturing input video
            frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            lastFrame = None

            os.chdir(gesture_frames_path)
            count = 0

            # assumption only first 200 frames are important
            while count < 201:
                ret, f = cap.read()  # extract frame
                if ret is False:
                    break
                fName = os.path.splitext(video)[0]
                fName = fName + "_frame_" + str(count) + ".jpeg"
                hc.append([join(gesture_frames_path, fName), gesture, frameCount])

                if not os.path.exists(fName):
                    f = th.handsegment(f)
                    f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                    lastFrame = f
                    cv2.imwrite(fName, f)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                count += 1

            # repeat last frame untill we get 200 frames
            while count < 51:
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
    parser.add_argument('gesture_folder', help='olders of videos of different gestures.')
    parser.add_argument('target_folder', help='folder where extracted frames should be kept.')
    args = parser.parse_args()
    convert(args.gesture_folder, args.target_folder)
