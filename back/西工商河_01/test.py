# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:12:09 2019

@author: Ironprop
"""

def clearMem():
    for i in locals().keys():
        del locals()[i]
clearMem()

import gauge_detect as gd
import cv2

VIDEO_PATH = 'D:/C#_finial/water_gauge_pooling/西工商河-北园桥_2019070611355124AFD6A0_1562384151_1.mp4'
FRAME_TOTAL = 500
FRAME_STEP = 10

########______Main______########

video = cv2.VideoCapture()
video.open(VIDEO_PATH)

for i in range(FRAME_TOTAL):
    _, frame = video.read()
    
    '''
    if i == 120:
        flag, ans, wd = gd.gaugeRead(frame)
        break
    '''
    if i % FRAME_STEP == 0:
        flag, ans, wd = gd.gaugeRead(frame)
        if (flag):
            print('Frame: ', i, ' -- ', ans)
        else:
            print('Frame: ', i, ' -- ', wd)
