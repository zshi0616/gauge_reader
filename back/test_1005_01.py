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
import matchTemp as Templ

VIDEO_PATH = 'D:/C#_finial/water_gauge_pooling/西工商河-北园桥_2019070611355124AFD6A0_1562384151_1.mp4'
OUTFILE_PATH = 'my.jpg'
FRAME_INDEX = 20

Sobel_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
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
    
    maxlength = int(max(np.sqrt(np.power(ex1-ex2, 2)+np.power(ey1-ey2, 2)), np.sqrt(np.power(ex3-ex4, 2)+np.power(ey3-ey4, 2))))
    maxwidth = int(max(np.sqrt(np.power(ex3-ex2, 2)+np.power(ey3-ey2, 2)), np.sqrt(np.power(ex1-ex4, 2)+np.power(ey1-ey4, 2))))
    
    dst = np.array([[maxwidth-1, 0], [maxwidth-1, maxlength-1], [0, maxlength-1], [0, 0]], dtype = "float32")
    rect = np.array([[ex1, ey1], [ex2, ey2], [ex3, ey3], [ex4, ey4]], dtype = "float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    gauge = cv2.warpPerspective(frame, M, (maxwidth, maxlength))
    gauge_m, gauge_n, _ = np.shape(gauge)
    
    warped = cv2.cvtColor(gauge, cv2.COLOR_BGR2GRAY)
    warped = cv2.filter2D(warped, -1, sharp_kernel)
    _, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY_INV)
    
    warped = cv2.dilate(warped, erode_kernel, iterations = 1)
    mor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    warped = cv2.morphologyEx(warped, cv2.MORPH_CLOSE, mor_kernel)
    warped = cv2.morphologyEx(warped, cv2.MORPH_OPEN, mor_kernel)
    _, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY_INV)
    binary, cnts, hierarchy = cv2.findContours(warped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    templ = cv2.imread('templ/templ_0.png')
    templ = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
    _, templ = cv2.threshold(templ, 210, 255, cv2.THRESH_BINARY)
    binary, templ_cnts, hierarchy = cv2.findContours(templ, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(templ_cnts[1])
    templ = templ[y:y+h, x:x+w]
    imgOut(templ, 'templ.jpg')
    
    locs = []
    figIndex = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if (area < 1500 and area > 500):
            figIndex = figIndex+1
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(gauge, (x,y), (x+w, y+h), (0, 255, 0), 2)
            numFig = warped[y:y+h, x:x+w]
            
            keyPoint = (x+w/2, y+h/2)
            bottomPoint = y+h
            res = Templ.match(numFig)
            if (res != -1):
                #print('Times ', figIndex, ': ', res)
                imgOut(numFig, str(figIndex)+'.jpg')
                locs.append([keyPoint, bottomPoint, res])
    
    dial = []
    for i in range(np.shape(locs)[0]):
        PointA = locs[i][0]
        if PointA[0] > gauge_n/2:
            continue
        for j in range(i+1, np.shape(locs)[0]):
            PointB = locs[j][0]
            dist = np.sqrt(np.power(PointA[0]-PointB[0], 2) + 1.5*np.power(PointA[1]-PointB[1], 2))
            if (dist < 100):
                if (PointA[0] > PointB[0]):
                    index_i = j
                    index_j = i
                else:
                    index_i = i
                    index_j = j
                num = locs[index_i][2] + 0.1*locs[index_j][2]
                point = locs[index_i][1]
                dial.append([point, num])
    
    if (np.shape(dial)[0] >= 2):
        numA = dial[0][1]
        numB = dial[1][1]
        potA = dial[0][0]
        potB = dial[1][0]
        
        ans = numA - 0.92*(gauge_m-potA)*(numA-numB)/(potB-potA)
        print(ans)
    else:
        print('No Dial')

            
    #cv2.drawContours(gauge, locs, -1, (0, 255, 0), 2)
    
    
    imgOut(gauge, 'gauge.jpg')
    imgOut(warped, 'warped.jpg')
    
    '''
    #warped = cv2.filter2D(gauge, -1, sharp_kernel)
    warped = cv2.cvtColor(gauge, cv2.COLOR_BGR2GRAY)
    warped = cv2.filter2D(warped, -1, Sobel_kernel)
    _, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY)
    #warped = cv2.erode(warped, erode_kernel, iterations = 2)
    
    lines = cv2.HoughLinesP(warped, 1.0, np.pi/180, 100, minLineLength = int(maxwidth/4), maxLineGap = 5)
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if (np.sqrt(np.power(x1-x2,2)+np.power(y1-y2,2)) < maxwidth/2):
            cv2.line(gauge, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 255, 0), 2)
    
    imgOut(gauge, 'gauge.jpg')
    imgOut(warped, 'warped.jpg')
    '''
    
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


