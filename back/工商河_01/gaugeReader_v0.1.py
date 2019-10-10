# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:12:09 2019

@author: Ironprop
"""

def clearMem():
    for i in locals().keys():
        del locals()[i]
clearMem()

import detecter as gd
import cv2

VIDEO_PATH_1 = 'D:/C#_finial/water_gauge_pooling/西工商河-北园桥_2019070611355124AFD6A0_1562384151_1.mp4'
VIDEO_PATH_2 = 'D:/C#_finial/water_gauge_pooling/东工商河-北园桥_2019070611372824AFD6A0_1562384248_1 00_00_20-00_00_50.mp4'

FRAME_TOTAL = 500
FRAME_STEP = 10
OUTPUT_PATH = 'gaugeReader.log'

########______Main______########

mode_str = input()
mode = -1
if (mode_str == '01'):
    VIDEO_PATH = VIDEO_PATH_1
    mode = 1
if (mode_str == '02'):
    VIDEO_PATH = VIDEO_PATH_2
    mode = 2

video = cv2.VideoCapture()
video.open(VIDEO_PATH)

doc = open(OUTPUT_PATH, 'w')
for i in range(FRAME_TOTAL):
    _, frame = video.read()
    
    '''
    if i == 120:
        flag, ans, wd = gd.gaugeRead(frame)
        break
    '''
    if i % FRAME_STEP == 0:
        flag, ans = gd.gaugeRead(frame, mode)
        print(ans, file = doc)
print('done')
doc.close()
