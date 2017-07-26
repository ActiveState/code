#!/usr/bin/env python
"""
Kinect Demo using minimum values from the depth image. 
@Author   = Alex Wallar
@Date     = 17 March, 2012
@Version  = 1.1
@Filename = KinectJoystickMin.py
"""
from freenect import sync_get_depth as get_depth, sync_get_video as get_video, init, close_device, open_device, set_led
import cv  
import numpy as np
import pygame
from math import *
from numpy import mean

def doloop():
    
    #Series of commands to do pointer operations on the kinect (motor, led, accelerometer)
    ctx = init() #Initiates device
    mdev = open_device(ctx, 0) #Opens the device for commands
    set_led(mdev, 1) #Sets LED to green
    close_device(mdev #Closes device. Device must be closed immediately after usage
    
    #Mean filter caches
    yList = [0,0,0,0,0,0]
    xList = [0,0,0,0,0,0]
    
    #Sets color tuples
    RED = (255,0,0)
    BLUE = (0,0,255)
    TEAL = (0,200,100)
    BLACK = (0,0,0)
    
    #Sets the size of the screen
    xSize = 640
    ySize = 480
    
    done = False #Main while loop bool counter
    pygame.init() #Initiates pygame
    screen = pygame.display.set_mode((xSize, ySize), pygame.RESIZABLE) #Creates the pygame window
    screen.fill(BLACK) #Fills the window black
    
    #Initiates the xTempPos and yTempPos values so that the point will remain stationary
    #if the minimum value is larger than 600
    xTempPos = xSize/2
    yTempPos = ySize/2
    
    global depth, rgb #Makes the depth and rgb variables global
    
    while not done:
        screen.fill(BLACK) #Makes the pygame window black after each iteration
        
        # Get a fresh frame
        (depth,_) = get_depth()
        (rgb, _) = get_video()
        
        minVal = np.min(depth) #This is the minimum value from the depth image
        minPos = np.argmin(depth) #This is the raw index of the minimum value above
        xPos = np.mod(minPos, xSize) #This is the x component of the raw index
        yPos = minPos//xSize #This is the y component of the raw index
        
        #This is the mean filter process
        """
        A mean filter works by collecting values in a cache list and taking the mean of them
        to determine the final value. It works in this case to decrease the amount of
        volatility the minimum position experiences to get a smoother display with a more
        consistent value. My computer works smoothly with a 5 bit cache where as a faster
        computer may need a larger cache and a slower computer may need a smaller cache
        """
        xList.append(xPos)
        del xList[0]
        xPos = int(mean(xList))
        yList.append(yPos)
        del yList[0]
        yPos = int(mean(yList))
        
        """
        This if statement says that if the minimum value is below 600 to store the minimum 
        positions in xTempPos and yTempPos and to make the dot color red. Also if the minimum
        value is larger than 600, xPos and yPos become the last stored minimum and maximum
        positions. It also changes the color to purple
        """
        if minVal < 600:
            xTempPos = xPos
            yTempPos = yPos
            COLOR = cv.RGB(255,0,0)
        else:
            xPos = xTempPos
            yPos = yTempPos
            COLOR = cv.RGB(100,0,100)
            
        cv.Circle(rgb, (xPos, yPos), 2, COLOR, 40) #draws a circle of a certain color at minimum position
    
        cv.ShowImage('Image',rgb) #Shows the image
        cv.WaitKey(5) #Keyboard interupt
        
        """
        The if statement below sets up the virtual joystick by basically breaking the pygame
        window into four parts. A dot representing the minimum position is drawn on the window
        and the corresponding button based on the position is "pressed". The quarter of the
        window in which the button "pressed" corresponds to turns teal after being "pressed"
        
        Top Right   : A
        Bottom Right: B
        Bottom Left : Y
        Top Right   : X
        """        
        if xPos <= xSize/2 and yPos <= ySize/2:
            command = 'A'
            rect1 = pygame.Rect((xSize/2,0),(xSize/2,ySize/2))
            pygame.draw.rect(screen,TEAL,rect1)
        elif xPos <= xSize/2 and yPos > ySize/2:
            command = 'B'
            rect1 = pygame.Rect((xSize/2,ySize/2),(xSize/2,ySize/2))
            pygame.draw.rect(screen,TEAL,rect1)
        elif xPos > xSize/2 and yPos <= ySize/2:
            command = 'X'
            rect1 = pygame.Rect((0,0),(xSize/2,ySize/2))
            pygame.draw.rect(screen,TEAL,rect1)
        else: 
            command = 'Y'
            rect1 = pygame.Rect((0,ySize/2),(xSize/2,ySize/2))
            pygame.draw.rect(screen,TEAL,rect1)
        pygame.draw.line(screen, BLUE, (xSize/2, ySize/2), (xSize - xPos,yPos)) #Draws a line from the middle to the minimum position
        pygame.draw.circle(screen, RED, (xSize - xPos,yPos), 10) #Draws the circle on pygame window
        pygame.display.flip() #Displays the processed pygame window
        print command, minVal #Prints the "pressed" button and the minimum value
        for e in pygame.event.get(): #Itertates through current events
            if e.type is pygame.QUIT: #If the close button is pressed, the while loop ends
                done = True
        
doloop()
