# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:22:14 2019

@author: stone
"""
import cv2
import numpy as np
from numba import autojit

numThd = 0.7

def match(img):
    res = []
    minnum = 1
    minindex = -1
    
    for i in range(10):
        filename = 'templ/templ_'+str(i)+'.png'
        templ = cv2.imread(filename)
        templ = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
        _, templ = cv2.threshold(templ, 210, 255, cv2.THRESH_BINARY)
        binary, templ_cnts, hierarchy = cv2.findContours(templ, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(templ_cnts[1])
        templ = templ[y:y+h, x:x+w]
        
        numFig = cv2.resize(img, (np.shape(templ)[1], np.shape(templ)[0]))
        resVal = np.mean(cv2.matchTemplate(numFig, templ, cv2.TM_SQDIFF_NORMED))
        res.append(resVal)
        
        #print('Num ', i, ': ', resVal)
    
    for i in range(10):
        if res[i] > numThd:
            res[i] = 1.0
        if res[i] < minnum:
            minnum = res[i]
            minindex = i
    return (minindex, minnum)
        
        
