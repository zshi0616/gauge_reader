# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:12:09 2019

@author: Ironprop
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = 'D:/C#_finial/water_gauge_pooling/全福河经一路南_2019070611430524AFD6A0_1562384585_1.mp4'
FRAME_INDEX = 100
Sobel_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
Robert_kernel = np.array([[-1, 0], [0, 1]])
my_kernel = np.array([[-1, 1], [-1, 1]])

#get frame
def getPict(VIDEO_PATH, FRAME_INDEX):
    video = cv2.VideoCapture()
    video.open(VIDEO_PATH)
    for i in range(FRAME_INDEX):
        _, frame = video.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#get edge by Sobel kernel
frame = getPict(VIDEO_PATH, FRAME_INDEX)
img = cv2.filter2D(frame, -1, Sobel_kernel)
#img = cv2.Canny(frame, 50, 150, 3)

#Hough detection is not sensitive to vertical line
rows, cols = img.shape
M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), 90, 1)
img = cv2.warpAffine(img, M, (cols,rows))
frame = cv2.warpAffine(frame, M, (cols, rows))

#draw lines
lines = cv2.HoughLinesP(img, 1.0, np.pi/180, 500, minLineLength = 500, maxLineGap = 5)
for line in lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[0][2]
    y2 = line[0][3]
    print(np.sqrt(np.power(x1-x2, 2) + np.power(y1-y2, 2)), ', k = '+str((y2-y1)/(x2-x1)))
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),-90,1)
frame = cv2.warpAffine(frame,M,(cols,rows))
cv2.imwrite('my.jpg', frame)
print('DONE!')

