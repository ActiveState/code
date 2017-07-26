#!/usr/bin/env python
"""
Use the Kinect to control your mouse

@Author   = Alexander James Wallar
@Date     = March 19, 2012
@Version  = 1.0
@Filename = Mouse.py
"""
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest
from freenect import sync_get_depth as get_depth
import numpy as np

zeros = lambda length: [0 for _ in range(length)]

global depth #Makes the depth global

#Sets the size of the screen
xSize = 640
ySize = 480

#Mean filter caches
yList = zeros(35)
xList = zeros(35)

d = display.Display()

def mouse_move(x,y):
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()

def mouse_click_down(button): 
    Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
    d.sync()
    
def mouse_click_up(button):
    Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
    d.sync()

def get_min_pos_kinect():
    
    (depth,_) = get_depth()
        
    minVal = np.min(depth) #This is the minimum value from the depth image
    minPos = np.argmin(depth) #This is the raw index of the minimum value above
    xPos = np.mod(minPos, xSize) #This is the x component of the raw index
    yPos = minPos//xSize #This is the y component of the raw index
        
    xList.append(xPos)
    del xList[0]
    xPos = int(np.mean(xList))
    yList.append(yPos)
    del yList[0]
    yPos = int(np.mean(yList))
        
    return (xSize - xPos-10, yPos, minVal)
    
def main_mouse(screen_x = 1280, screen_y = 800):
    timer = 0
    while timer < 10000:
        x_min, y_min, min_val = get_min_pos_kinect()
        print min_val
        x_min = int((screen_x/630)*x_min)
        y_min = int(2*(screen_y/479)*y_min)
        mouse_move(x_min, y_min)
        if min_val < 600:
            mouse_click_down(1)
        else:
            mouse_click_up(1)
        timer +=1
        
