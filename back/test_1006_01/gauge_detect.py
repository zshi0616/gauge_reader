# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 21:01:04 2019

@author: stone
"""
import cv2
import numpy as np
import numba
import matplotlib.pyplot as plt
import matchTemp as Templ

Sobel_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
Robert_kernel = np.array([[-1, 0], [0, 1]])
mean_kernel = np.array([[0,0.2,0],[0.2,0.2,0.2],[0,0.2,0]])
#my_kernel = np.array([[0,0.2,0],[0.2,0.2,0.2],[0,0.2,0]])
sharp_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
erode_kernel = np.ones((3,3))

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

def getDist(PointA, PointB):
    return (np.sqrt(np.power(PointA[0]-PointB[0], 2) + np.power(PointA[1]-PointB[1], 2)))

def gaugeRead(frame):
    img_cont = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame_m, frame_n = np.shape(img_cont)
    #img_cont = cv2.filter2D(img_gray, -1, my_kernel)
    
    #提取水尺边沿
    edge_flag, edge = edgeDetect(img_cont)
    if (edge_flag):
        #获得近似四边形
        epsilon = 0.02*cv2.arcLength(edge, True)
        approx = cv2.approxPolyDP(edge, epsilon, True)
        x, y, w, h = cv2.boundingRect(approx)
        
        #自适应四个顶点
        if (np.shape(approx)[0] >= 4):
            mindis = getDist((x, y), (x+w, y+h))
            for point in approx:
                dis = getDist(point[0], (x+w-1, 0))
                if dis < mindis:
                    mindis = dis
                    ex1 = point[0][0]
                    ey1 = point[0][1]
            
            mindis = getDist((x, y), (x+w, y+h))
            for point in approx:
                dis = getDist(point[0], (x+w-1, y+h-1))
                if dis < mindis:
                    mindis = dis
                    ex2 = point[0][0]
                    ey2 = point[0][1]
            
            mindis = getDist((x, y), (x+w, y+h))
            for point in approx:
                dis = getDist(point[0], (0, y+h-1))
                if dis < mindis:
                    mindis = dis
                    ex3 = point[0][0]
                    ey3 = point[0][1]
            
            mindis = getDist((x, y), (x+w, y+h))
            for point in approx:
                dis = getDist(point[0], (0, 0))
                if dis < mindis:
                    mindis = dis
                    ex4 = point[0][0]
                    ey4 = point[0][1]
            
        else:
            return(False, 'NA', 'No edge') 
        
        #计算变换矩阵
        maxlength = int(max(np.sqrt(np.power(ex1-ex2, 2)+np.power(ey1-ey2, 2)), np.sqrt(np.power(ex3-ex4, 2)+np.power(ey3-ey4, 2))))
        maxwidth = int(max(np.sqrt(np.power(ex3-ex2, 2)+np.power(ey3-ey2, 2)), np.sqrt(np.power(ex1-ex4, 2)+np.power(ey1-ey4, 2))))
        dst = np.array([[maxwidth-1, 0], [maxwidth-1, maxlength-1], [0, maxlength-1], [0, 0]], dtype = "float32")
        rect = np.array([[ex1, ey1], [ex2, ey2], [ex3, ey3], [ex4, ey4]], dtype = "float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        #将水尺变换为矩形
        gauge = cv2.warpPerspective(frame, M, (maxwidth, maxlength))
        gauge_m, gauge_n, _ = np.shape(gauge)
        #二值化
        warped = cv2.cvtColor(gauge, cv2.COLOR_BGR2GRAY)
        warped = cv2.filter2D(warped, -1, sharp_kernel)
        _, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY_INV)
        #腐蚀膨胀
        warped = cv2.dilate(warped, erode_kernel, iterations = 1)
        mor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
        warped = cv2.morphologyEx(warped, cv2.MORPH_CLOSE, mor_kernel)
        warped = cv2.morphologyEx(warped, cv2.MORPH_OPEN, mor_kernel)
        _, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY_INV)
        #提取边沿
        binary, cnts, hierarchy = cv2.findContours(warped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #提取数字的边沿
        locs = []
        figIndex = 0
        for c in cnts:
            area = cv2.contourArea(c)
            if (area < 1500 and area > 500):
                figIndex = figIndex+1
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(gauge, (x,y), (x+w, y+h), (0, 255, 0), 2)
                numFig = warped[y:y+h, x:x+w]
                #设置关键点、最底点和识别结果
                keyPoint = (x+w/2, y+h/2)
                bottomPoint = y+h
                res, _ = Templ.match(numFig)
                #imgOut(numFig, str(figIndex)+'.jpg')
                #在约束范围内的数字储存在数组中
                if (res != -1 and keyPoint[0] > 50 and keyPoint[0] < gauge_n/2):
                    locs.append([keyPoint, bottomPoint, res])
        #imgOut(gauge, 'gauge.jpg')
        #生成比例尺
        dial = []
        for i in range(np.shape(locs)[0]):
            PointA = locs[i][0]
            for j in range(i+1, np.shape(locs)[0]):
                PointB = locs[j][0]
                dist = np.sqrt(np.power(PointA[0]-PointB[0], 2) + 10*np.power(PointA[1]-PointB[1], 2))
                #当距离小于最大距离
                if (dist < 80):
                    #print(dist)
                    if (PointA[0] > PointB[0]):
                        index_i = j
                        index_j = i
                    else:
                        index_i = i
                        index_j = j
                    num = locs[index_i][2] + 0.1*locs[index_j][2]
                    point = locs[index_i][1]
                    dial.append([point, num])
        #计算结果
        numA = 0
        numB = 0
        if (np.shape(dial)[0] >= 2):
            for i in range(np.shape(dial)[0]):
                if (dial[i][1] == 3.4 or dial[i][1] == 3.2 or dial[i][1] == 3.0 or dial[i][1] == 2.8):
                    if (numA == 0):
                        numA = dial[i][1]
                        potA = dial[i][0]
                        continue
                    if (numB == 0):
                        numB = dial[i][1]
                        potB = dial[i][0]
                        continue
                    break
            
            if (numA == 0 or numB == 0):
                return(False, 'NA', 'No Dial')

            ans = numA - 0.92*(gauge_m-potA)*(numA-numB)/(potB-potA)
            return(True, ans, dial)
        else:
            return(False, 'NA', 'No Dial')
    
                
        #cv2.drawContours(gauge, locs, -1, (0, 255, 0), 2)
        
        #imgOut(gauge, 'gauge.jpg')
        #imgOut(warped, 'warped.jpg')
        
    else:
        return(False, 'NA', 'No edge')
    

