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

def edgeDetect(img, imgcolor):
    _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    
    #imgOut(img, 'bin.jpg')
    
    binary, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea)
    
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
    imgOut(frame, 'frame.jpg')
    #frame_m, frame_n = np.shape(img_cont)
    #img_cont = cv2.filter2D(img_cont, -1, sharp_kernel)
    #img_cont = cv2.Canny(img_cont, 50, 100)
    #imgOut(img_cont, 'cont.jpg')
    #提取水尺边沿
    edge_flag, edge = edgeDetect(img_cont, frame)
    if (edge_flag):
        #获得近似四边形
        epsilon = 0.02*cv2.arcLength(edge, True)
        approx = cv2.approxPolyDP(edge, epsilon, True)
        x, y, w, h = cv2.boundingRect(approx)
        
        #for p in approx:
        #    cv2.circle(frame, (p[0][0], p[0][1]), 10, (0, 0, 255), -1)
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
        #imgOut(frame, 'frame.jpg')
        
        #自适应四个顶点
        if (np.shape(approx)[0] >= 4):
            mindis = getDist((x, y), (x+w, y+h))
            
            #cv2.circle(frame, (x+w-1, y), 10, (0, 255, 0), -1)
            for point in approx:
                dis = getDist(point[0], (x+w-1, y))
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
                dis = getDist(point[0], (x, y+h-1))
                if dis < mindis:
                    mindis = dis
                    ex3 = point[0][0]
                    ey3 = point[0][1]
            
            mindis = getDist((x, y), (x+w, y+h))
            for point in approx:
                dis = getDist(point[0], (x, y))
                if dis < mindis:
                    mindis = dis
                    ex4 = point[0][0]
                    ey4 = point[0][1]
            
            #cv2.rectangle(frame, (ex4, ey4), (ex2, ey2), (0, 0, 255), 2)
            #imgOut(frame, 'frame.jpg')
            
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
        #warped = np.uint8(np.clip((1.2*warped - 50), 0, 255))
        warped = cv2.filter2D(warped, -1, mean_kernel)
        imgOut(warped, 'sharp.jpg')
        _, warped = cv2.threshold(warped, 210, 255, cv2.THRESH_BINARY_INV)
        #腐蚀膨胀
        #warped = cv2.dilate(warped, erode_kernel, iterations = 1)
        mor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        warped = cv2.morphologyEx(warped, cv2.MORPH_CLOSE, mor_kernel)
        warped = cv2.morphologyEx(warped, cv2.MORPH_OPEN, mor_kernel)
        _, warped = cv2.threshold(warped, 127, 255, cv2.THRESH_BINARY_INV)
        imgOut(warped, 'warped.jpg')
        #提取边沿
        binary, cnts, hierarchy = cv2.findContours(warped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #提取数字的边沿
        locs = []
        nums = []
        figIndex = 0
        for c in cnts:
            area = cv2.contourArea(c)
            
            if (area < 1500 and area > 500):
                figIndex = figIndex+1
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(gauge, (x,y), (x+w, y+h), (0, 255, 0), 2)
                numFig = warped[y:y+h, x:x+w]
                imgOut(numFig, str(figIndex)+'.jpg')
                #设置关键点、最底点和识别结果
                keyPoint = (x+w/2, y+h/2)
                bottomPoint = y+h
                res, _ = Templ.match(numFig)
                #imgOut(numFig, str(figIndex)+'.jpg')
                #在约束范围内的数字储存在数组中
                if (res != -1 and keyPoint[0] > 110 and keyPoint[0] < gauge_n/2):
                    nums.append([keyPoint, bottomPoint, res])
                    #print(figIndex, res, _, keyPoint)
                locs.append([keyPoint, bottomPoint, res])
        #print(locs)
        imgOut(gauge, 'gauge.jpg')
        #生成比例尺
        
        if (np.shape(nums)[0] <= 0):
            return(False, 'NA', 'No Dial')
        
        dial = []
        numId = nums[0]
        minDis = gauge_m
        minIndex = -1
        for i in range(np.shape(locs)[0]):
            PointA = locs[i]
            if (numId[1] - PointA[1] > 0 and numId[1] - PointA[1] < minDis):
                minIndex = i
                minDis = numId[1] - PointA[1]
        dial.append([numId[1], 2+0.1*numId[2]])
        dial.append([locs[minIndex][1], 2+0.1*numId[2]+0.1])
        
        #print(dial)
        #计算结果
        potA = dial[0][0]
        numA = dial[0][1]
        potB = dial[1][0]
        numB = dial[1][1]
        if (potB-potA != 0):
            ans = numA - 0.92*(gauge_m-potA)*(numA-numB)/(potB-potA)
            return(True, ans, dial)
        else:
            return(False, 'NA', 'No Dial')
    
                
        #cv2.drawContours(gauge, locs, -1, (0, 255, 0), 2)
        
        #imgOut(gauge, 'gauge.jpg')
        #imgOut(warped, 'warped.jpg')
        
    else:
        return(False, 'NA', 'No edge')
    

