#!/usr/bin/env python3
# Universal Sign Language Translator
# Created by Team Axenhammer, https://github.com/Axenhammer
# Licensed as MIT

import numpy as np
import os
import cv2

def sequence_creator(user_path, final_path)
	path = user_path
	x=[]
	for i in os.listdir(path):
	    x.append(cv2.imread(path+i,0))
	p = x[0]
	k=1
	for i in x:
	    p[np.where(i> 190)]=0 + (255/60)*k
	    p += i
	    k += 1
	cv2.imshow("hello",p)
	cv2.waitKey(0)
	path ='training_data/everybody/'
	print(path+'everyone_1')
	cv2.imwrite( path+'everyone_1.jpg' ,p)
