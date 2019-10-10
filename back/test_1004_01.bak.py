# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:12:09 2019

@author: Ironprop
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = 'D:/C#_finial/water_gauge_pooling/西工商河-北园桥_2019070611355124AFD6A0_1562384151_1.mp4'
FRAME_INDEX = 100
Sobel_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
Robert_kernel = np.array([[-1, 0], [0, 1]])
my_kernel = np.array([[0,0.2,0],[0.2,0.2,0.2],[0,0.2,0]])

#get frame
def getPict(VIDEO_PATH, FRAME_INDEX):
    video = cv2.VideoCapture()
    video.open(VIDEO_PATH)
    for i in range(FRAME_INDEX):
        _, frame = video.read()
    return frame

def lineFm(x1, y1, x2, y2, x):
    return (x*1.0 - x2) / (x1-x2) * (y1-y2) + y2

def lineDetect(img):
    lines = cv2.HoughLinesP(img, 1.0, np.pi/180, 500, minLineLength = 500, maxLineGap = 5)
    if (lines.shape[0] == 1):
        return (True, lines[0][0])
    else:
        return (False, 0)

def edgeDetect(img):
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    binary, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for (i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        if (w > 500):
            return (True, contours[i])
    return (False, 0)

#get edge by Sobel kernel
frame = getPict(VIDEO_PATH, FRAME_INDEX)
img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img_line = cv2.filter2D(img_gray, -1, Sobel_kernel)
img_cont = cv2.filter2D(img_gray, -1, my_kernel)

rows, cols = img_gray.shape
M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), 90, 1)
img_line = cv2.warpAffine(img_line, M, (cols,rows))
img_cont = cv2.warpAffine(img_cont, M, (cols,rows))
frame = cv2.warpAffine(frame, M, (cols, rows))

line_flag, line = lineDetect(img_line)
if (line_flag):
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]
    print('Line: ', np.sqrt(np.power(x1-x2, 2) + np.power(y1-y2, 2)), ', k = '+str((y2-y1)/(x2-x1)))
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
else:
    print('No Line')

edge_flag, edge = edgeDetect(img_cont)
if (edge_flag):
    epsilon = 0.05*cv2.arcLength(edge, True)
    approx = cv2.approxPolyDP(edge, epsilon, True)
    for point in approx:
        x = point[0][0]
        y = point[0][1]
        cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)
else:
    print('No edge')

if (line_flag and edge_flag):
    for x in range(x2, 1536):
        y = int(lineFm(x1, y1, x2, y2, x))
        for point in edge:
            if (x == point[0][0] and y == point[0][1]):
                print('Point: ', x, y)
                cv2.circle(frame, (x, y), 10, (0, 255, 0), 4)
                break



'''

img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img_line = cv2.filter2D(img_gray, -1, Sobel_kernel)
img_cont = cv2.filter2D(img_gray, -1, my_kernel)

#Hough detection is not sensitive to vertical line
rows, cols = img_line.shape
M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), 90, 1)
img_line = cv2.warpAffine(img_line, M, (cols,rows))
img_cont = cv2.warpAffine(img_cont, M, (cols,rows))
frame = cv2.warpAffine(frame, M, (cols, rows))

#edge detection
_, img_cont = cv2.threshold(img_cont, 127, 255, cv2.THRESH_BINARY)
binary, contours, hierarchy = cv2.findContours(img_cont, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
locs = []
for (i, c) in enumerate(contours):
    (x, y, w, h) = cv2.boundingRect(c)
    if (w > 500):
        print((x,y,w,h))
        locs.append(contours[i])
#cv2.drawContours(frame,locs,-1,(0,0,255),3)

#draw lines
lines = cv2.HoughLinesP(img_line, 1.0, np.pi/180, 500, minLineLength = 500, maxLineGap = 5)
for line in lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[0][2]
    y2 = line[0][3]
    print(np.sqrt(np.power(x1-x2, 2) + np.power(y1-y2, 2)), ', k = '+str((y2-y1)/(x2-x1)))
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

#get intersection
for x in range(lines[0][0][2], 1536):
    x1 = lines[0][0][0]
    y1 = lines[0][0][1]
    x2 = lines[0][0][2]
    y2 = lines[0][0][3]
    y = int(lineFm(x1, y1, x2, y2, x))
    for point in locs[0]:
        if (x == point[0][0] and y == point[0][1]):
            print(x, y)
            cv2.circle(frame, (x, y), 10, (0, 255, 0), 4)
            break

epsilon = 0.05*cv2.arcLength(locs[0], True)
approx = cv2.approxPolyDP(locs[0], epsilon, True)

for point in approx:
    x = point[0][0]
    y = point[0][1]
    cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)

cv2.drawContours(frame, approx, -1, (0, 0, 255), 3)
'''

#output
M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), -90, 1)
frame = cv2.warpAffine(frame, M, (cols, rows))
cv2.imwrite('my.jpg', frame)
print('DONE!')


