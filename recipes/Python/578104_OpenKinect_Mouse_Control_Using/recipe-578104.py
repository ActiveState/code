from freenect import sync_get_depth as get_depth #Uses freenect to get depth information from the Kinect
import numpy as np #Imports NumPy
import cv,cv2 #Uses both of cv and cv2
import pygame #Uses pygame

#The libaries below are used for mouse manipulation
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

constList = lambda length, val: [val for _ in range(length)] #Gives a list of size length filled with the variable val. length is a list and val is dynamic

"""
This class is a less extensive form of regionprops() developed by MATLAB. It finds properties of contours and sets them to fields
"""
class BlobAnalysis:
    def __init__(self,BW): #Constructor. BW is a binary image in the form of a numpy array
        self.BW = BW
        cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) #Finds the contours
        counter = 0
        """
        These are dynamic lists used to store variables
        """
        centroid = list()
        cHull = list()
        contours = list()
        cHullArea = list()
        contourArea = list()
        while cs: #Iterate through the CvSeq, cs.
            if abs(cv.ContourArea(cs)) > 2000: #Filters out contours smaller than 2000 pixels in area
                contourArea.append(cv.ContourArea(cs)) #Appends contourArea with newest contour area
                m = cv.Moments(cs) #Finds all of the moments of the filtered contour
                try:
                    m10 = int(cv.GetSpatialMoment(m,1,0)) #Spatial moment m10
                    m00 = int(cv.GetSpatialMoment(m,0,0)) #Spatial moment m00
                    m01 = int(cv.GetSpatialMoment(m,0,1)) #Spatial moment m01
                    centroid.append((int(m10/m00), int(m01/m00))) #Appends centroid list with newest coordinates of centroid of contour
                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) #Finds the convex hull of cs in type CvSeq
                    cHullArea.append(cv.ContourArea(convexHull)) #Adds the area of the convex hull to cHullArea list
                    cHull.append(list(convexHull)) #Adds the list form of the convex hull to cHull list
                    contours.append(list(cs)) #Adds the list form of the contour to contours list
                    counter += 1 #Adds to the counter to see how many blobs are there
                except:
                    pass
            cs = cs.h_next() #Goes to next contour in cs CvSeq
        """
        Below the variables are made into fields for referencing later
        """
        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea

d = display.Display() #Display reference for Xlib manipulation
def move_mouse(x,y):#Moves the mouse to (x,y). x and y are ints
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()
    
def click_down(button):#Simulates a down click. Button is an int
    Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
    d.sync()
    
def click_up(button): #Simulates a up click. Button is an int
    Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
    d.sync()

"""
The function below is a basic mean filter. It appends a cache list and takes the mean of it.
It is useful for filtering noisy data
cache is a list of floats or ints and val is either a float or an int
it returns the filtered mean
"""
def cacheAppendMean(cache, val):
    cache.append(val)
    del cache[0]
    return np.mean(cache)

"""
This is the GUI that displays the thresholded image with the convex hull and centroids. It uses pygame.
Mouse control is also dictated in this function because the mouse commands are updated as the frame is updated
"""
def hand_tracker():
    (depth,_) = get_depth()
    cHullAreaCache = constList(5,12000) #Blank cache list for convex hull area
    areaRatioCache = constList(5,1) #Blank cache list for the area ratio of contour area to convex hull area
    centroidList = list() #Initiate centroid list
    #RGB Color tuples
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (255,0,255)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    pygame.init() #Initiates pygame
    xSize,ySize = 640,480 #Sets size of window
    screen = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #creates main surface
    screenFlipped = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #creates surface that will be flipped (mirror display)
    screen.fill(BLACK) #Make the window black
    done = False #Iterator boolean --> Tells programw when to terminate
    dummy = False #Very important bool for mouse manipulation
    while not done:
        screen.fill(BLACK) #Make the window black
        (depth,_) = get_depth() #Get the depth from the kinect 
        depth = depth.astype(np.float32) #Convert the depth to a 32 bit float
        _,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV) #Threshold the depth for a binary image. Thresholded at 600 arbitary units
        _,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV) #Threshold the background in order to have an outlined background and segmented foreground
        blobData = BlobAnalysis(depthThresh) #Creates blobData object using BlobAnalysis class
        blobDataBack = BlobAnalysis(back) #Creates blobDataBack object using BlobAnalysis class
        
        for cont in blobDataBack.contours: #Iterates through contours in the background
            pygame.draw.lines(screen,YELLOW,True,cont,3) #Colors the binary boundaries of the background yellow
        for i in range(blobData.counter): #Iterate from 0 to the number of blobs minus 1
            pygame.draw.circle(screen,BLUE,blobData.centroid[i],10) #Draws a blue circle at each centroid
            centroidList.append(blobData.centroid[i]) #Adds the centroid tuple to the centroidList --> used for drawing
            pygame.draw.lines(screen,RED,True,blobData.cHull[i],3) #Draws the convex hull for each blob
            pygame.draw.lines(screen,GREEN,True,blobData.contours[i],3) #Draws the contour of each blob
            for tips in blobData.cHull[i]: #Iterates through the verticies of the convex hull for each blob
                pygame.draw.circle(screen,PURPLE,tips,5) #Draws the vertices purple
        
        """
        #Drawing Loop
        #This draws on the screen lines from the centroids
        #Possible exploration into gesture recognition :D
        for cent in centroidList:
            pygame.draw.circle(screen,BLUE,cent,10)
        """
        
        pygame.display.set_caption('Kinect Tracking') #Makes the caption of the pygame screen 'Kinect Tracking'
        del depth #Deletes depth --> opencv memory issue
        screenFlipped = pygame.transform.flip(screen,1,0) #Flips the screen so that it is a mirror display
        screen.blit(screenFlipped,(0,0)) #Updates the main screen --> screen
        pygame.display.flip() #Updates everything on the window
        
        #Mouse Try statement
        try:
            centroidX = blobData.centroid[0][0]
            centroidY = blobData.centroid[0][1]
            if dummy:
                mousePtr = display.Display().screen().root.query_pointer()._data #Gets current mouse attributes
                dX = centroidX - strX #Finds the change in X
                dY = strY - centroidY #Finds the change in Y
                if abs(dX) > 1: #If there was a change in X greater than 1...
                    mouseX = mousePtr["root_x"] - 2*dX #New X coordinate of mouse
                if abs(dY) > 1: #If there was a change in Y greater than 1...
                    mouseY = mousePtr["root_y"] - 2*dY #New Y coordinate of mouse
                move_mouse(mouseX,mouseY) #Moves mouse to new location
                strX = centroidX #Makes the new starting X of mouse to current X of newest centroid
                strY = centroidY #Makes the new starting Y of mouse to current Y of newest centroid
                cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0]) #Normalizes (gets rid of noise) in the convex hull area
                areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea) #Normalizes the ratio between the contour area and convex hull area
                if cArea < 10000 and areaRatio > 0.82: #Defines what a click down is. Area must be small and the hand must look like a binary circle (nearly)
                    click_down(1)
                else:
                    click_up(1)
            else:
                strX = centroidX #Initializes the starting X
                strY = centroidY #Initializes the starting Y
                dummy = True #Lets the function continue to the first part of the if statement
        except: #There may be no centroids and therefore blobData.centroid[0] will be out of range
            dummy = False #Waits for a new starting point
            
        for e in pygame.event.get(): #Itertates through current events
            if e.type is pygame.QUIT: #If the close button is pressed, the while loop ends
                done = True

try: #Kinect may not be plugged in --> weird erros
    hand_tracker()
except: #Lets the libfreenect errors be shown instead of python ones
    pass
