#!/usr/bin/env python3
# Universal Sign Language Translator
# Created by Team Axenhammer, https://github.com/Axenhammer
# Licensed as MIT

import numpy as np
import os
import cv2
import pickle

DATADIR="training_data/classes"
CATEGORIES = ["Everyone","Good_evening"]
training_data =[]
def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR,category)
        class_num =CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img),0)
                training_data.append([img_array ,class_num])
            except Exception as e:
                pass
create_training_data()

X = []
y = []
for features,label in training_data:
    X.append(features)
    y.append(label)

X=np.array(X).reshape(-1,1920,1080,1)


pickle_out=open("X.pickle","wb")
pickle.dump(X,pickle_out)
pickle_out.close()

pickle_out=open("y.pickle","wb")
pickle.dump(y,pickle_out)
pickle_out.close()
