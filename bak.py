# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:12:09 2019

@author: Ironprop
"""
def clearMem():
    for i in locals().keys():
        del locals()[i]
clearMem()

import cv2
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = 'D:/C#_finial/water_gauge_pooling/西工商河-北园桥_2019070611355124AFD6A0_1562384151_1.mp4'
OUTFILE_PATH = 'my.jpg'
FRAME_INDEX = 100

Sobel_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
Robert_kernel = np.array([[-1, 0], [0, 1]])
mean_kernel = np.array([[0,0.2,0],[0.2,0.2,0.2],[0,0.2,0]])
my_kernel = np.array([[0,0.2,0],[0.2,0.2,0.2],[0,0.2,0]])
sharp_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
erode_kernel = np.ones((3,3))

#get frame
def getPict(VIDEO_PATH, FRAME_INDEX):
    video = cv2.VideoCapture()
    video.open(VIDEO_PATH)
    for i in range(FRAME_INDEX):
        _, frame = video.read()
    print('-------------------')
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
        if (h > 500):
            return (True, contours[i])
    return (False, 0)

def imgOut(img, OUTFILE_PATH):
    cv2.imwrite(OUTFILE_PATH, img)
    return 'DONE!'

#get edge by Sobel kernel
frame = getPict(VIDEO_PATH, FRAME_INDEX)
img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img_line = cv2.filter2D(img_gray, -1, Sobel_kernel)
img_cont = cv2.filter2D(img_gray, -1, my_kernel)

edge_flag, edge = edgeDetect(img_cont)
if (edge_flag):
    epsilon = 0.02*cv2.arcLength(edge, True)
    approx = cv2.approxPolyDP(edge, epsilon, True)
    
    ex1 = approx[3][0][0]
    ey1 = approx[3][0][1]
    ex2 = approx[2][0][0]
    ey2 = approx[2][0][1]
    ex3 = approx[1][0][0]
    ey3 = approx[1][0][1]
    ex4 = approx[0][0][0]
    ey4 = approx[0][0][1]
    
    #cv2.circle(frame, (ex1, ey1), 10, (0, 0, 255), 5)
    #cv2.circle(frame, (ex2, ey2), 10, (0, 0, 255), 5)
    cv2.circle(frame, (ex3, ey3), 10, (0, 0, 255), 5)
    #cv2.circle(frame, (ex4, ey4), 10, (0, 0, 255), 5)

    imgOut(frame, 'frame.jpg')
    
    maxlength = int(max(np.sqrt(np.power(ex1-ex2, 2)+np.power(ey1-ey2, 2)), np.sqrt(np.power(ex3-ex4, 2)+np.power(ey3-ey4, 2))))
    maxwidth = int(max(np.sqrt(np.power(ex3-ex2, 2)+np.power(ey3-ey2, 2)), np.sqrt(np.power(ex1-ex4, 2)+np.power(ey1-ey4, 2))))
    
    dst = np.array([[maxwidth-1, 0], [maxwidth-1, maxlength-1], [0, maxlength-1], [0, 0]], dtype = "float32")
    rect = np.array([[ex1, ey1], [ex2, ey2], [ex3, ey3], [ex4, ey4]], dtype = "float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(frame, M, (maxwidth, maxlength))
    gauge = warped
    
    warped = cv2.filter2D(warped, -1, sharp_kernel)
    #warped = warped[:, x1:x2, :]
    
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    #warped = cv2.filter2D(warped, -1, mean_kernel)
    #_, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY)
    
    #warped = cv2.erode(warped, erode_kernel, iterations = 2)
    
    warped = cv2.GaussianBlur(warped, (5, 5), 0)
    warped = cv2.Canny(warped, 50, 200, 255)
    
    
    _, cnts, _ = cv2.findContours(warped.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    numLocs = []
    num = 5
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if num == 0:
            break
        if len(approx) == 4:
            num = num - 1
            numLocs.append(approx)
    
    for loc in numLocs:
        ex1 = loc[0][0][0]
        ey1 = loc[0][0][1]
        ex2 = loc[1][0][0]
        ey2 = loc[1][0][1]
        ex3 = loc[2][0][0]
        ey3 = loc[2][0][1]
        ex4 = loc[3][0][0]
        ey4 = loc[3][0][1]

        cv2.circle(gauge, (ex1, ey1), 10, (0, 0, 255), 5)
        cv2.circle(gauge, (ex2, ey2), 10, (0, 0, 255), 5)
        cv2.circle(gauge, (ex3, ey3), 10, (0, 0, 255), 5)
        cv2.circle(gauge, (ex4, ey4), 10, (0, 0, 255), 5)
    
    
    imgOut(gauge, 'warped.jpg')
    
    
    '''
    for point in approx:
        x = point[0][0]
        y = point[0][1]
        cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)
    for i in range(approx.shape[0]):
        if (i == approx.shape[0] - 1):
            cv2.line(frame, (approx[i][0][0], approx[i][0][1]), (approx[0][0][0], approx[0][0][1]), (0, 0, 255), 2)
        else:
            cv2.line(frame, (approx[i][0][0], approx[i][0][1]), (approx[i+1][0][0], approx[i+1][0][1]), (0, 0, 255), 2)
    '''
        
else:
    print('No edge')

'''
if (line_flag and edge_flag):
    for x in range(x, 1536):
        y = int(lineFm(x1, y1, x2, y2, x))
        for point in edge:
            if (x == point[0][0] and y == point[0][1]):
                print('Point: ', x, y)
                cv2.circle(frame, (x, y), 10, (0, 255, 0), 4)
                break
'''

#output
print(imgOut(frame, OUTFILE_PATH))


