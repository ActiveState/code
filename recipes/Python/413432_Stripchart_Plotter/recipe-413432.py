#!/usr/bin/env python
"""
Author: Flavio Codeco Coelho
License: GPL
Stripchart module for vpython
Features:
-user defined number of channels

"""
import psyco
import time
from visual import *
from visual.text import *
from RandomArray import random
from psyco.classes import *
psyco.full()

class Strip:
    """
    Stripchart object.
    """
    def __init__(self, nch=1, xlabel='t(s)',ylabel='V'):
        self.scene = display(title="Stripchart Recorder",width=600,height=400, uniform=0, ambient=1,autoscale=1)
        #create the curves
        self.channels = self.addch(nch)
        self.gridon = True
        self.grid = frame() #collection of horizontal grid lines
        self.ticklabels=frame()#collection of labels
        self.xlabel = label(frame=self.grid,pos=(9,-9,0),text=xlabel,color=color.orange,box=0, line=0)
        self.ylabel = label(frame=self.grid,pos=(-9,9,0),text=ylabel,color=color.orange,box=0,line=0)
        self.drawGrid()
        self.drawTickLabels(range(-10,10),range(-10,10))
        

    def addch(self, nch=1):
        """
        Creates a channel object (curve)
        nch is the number of channels.
        """
        col = [color.white,color.blue,color.red,color.green,color.yellow,color.cyan,color.magenta, color.orange]
        tplch = tuple([curve(radius=0, color=col[n%len(col)])for n in xrange(nch)])

        return tplch

    def toggleGrid(self):
        """
        Toggle visibility of gridlines
        """
        r = len(self.grid.objects)
        if self.gridon:
            for i in range(r):
                self.grid.objects[0].visible = 0
            self.gridon = False
        else:
            self.drawGrid()
            self.gridon = True
            
        pass
    def drawGrid(self):
        """
        draw grid lines
        """
        hrng = int(self.scene.range[1])
        vrng = int(self.scene.range[0])
        
        [curve(frame=self.grid,pos=[(-vrng,i),(vrng,i)],color=color.white) for i in  xrange(-hrng, hrng, hrng*2/10)]
        
        [curve(frame=self.grid,pos=[(j,-hrng),(j,hrng)],color=color.white) for j in  xrange(-vrng, vrng, vrng*2/10)]
        
        
        
    def drawTickLabels(self,xticks,yticks):
        """
        Draw x and y tick labels
        """
        xticks2 = array([round(i,2) for i in xticks])
        yticks2 = array([round(i,2) for i in yticks])
        labidx = range(0,len(xticks2),len(xticks2)/10) #indices to the labels to be plotted
        Pos = range(-10,10,2) #position of the ticklabels within the frame coordinates
        
        #List comprehensions to draw ticklabels. [(xticks,yticks) for i in xrange(len(Pos))]
        # Not as clear as a regular "for" but much faster...
        [label(frame=self.ticklabels,pos=(Pos[i],-8,0),text=str(xticks2[labidx[i]]),color=color.orange,box=0,line=0) for i in xrange(len(Pos))] #x ticklables
        
        [label(frame=self.ticklabels,pos=(-8,Pos[i],0),text=str(yticks2[labidx[i]]),color=color.orange,box=0,line=0) for i in xrange(len(Pos))] #y ticklabels
       
    def updateTicks(self,xticks,yticks):
        """
        Update tick labels  values
        """
        xticks2 = array([round(i,2) for i in xticks])
        yticks2 = array([round(i,2) for i in yticks])
        labidx = range(0,len(xticks2),len(xticks2)/10) #indices to the labels to be plotted
        Pos = range(-10,10,2) #position of the ticklabels within the frame coordinates
        i = j = 0
        for l in self.ticklabels.objects:
            if self.ticklabels.objects.index(l) < 10: #update x axis
                l.text = str(xticks2[labidx[i]])
                i += 1
            else:                       #update y axis
                l.text = str(yticks2[labidx[j]])
                j += 1
        
        
    def plot(self,ch,point):
        """
        Appends a point to the channel(curve) object ch.
        Fills the scene and after it is full,
        shifts the curve one step left, for each new point.
        If its the first point it creates the plot.
        """
        #Adjust the scene and frames vertically to folow data
        if point[1] > self.scene.range[1]:
            self.scene.center[1] = point[1]-9
            self.grid.y = point[1]-9
            self.ticklabels.y = point[1]-9
        elif  point[1] < -self.scene.range[1]:
            self.scene.center[1] = point[1]+9
            self.grid.y = point[1]+9
            self.ticklabels.y = point[1]+9
        #=========================================    
        if self.scene.kb.keys:#key trap
            s = self.scene.kb.getkey() # obtain keyboard information
            if s == 'g' or s == 'G':
                self.toggleGrid()
        # Scroll scene center right to follow data        
        if len(ch.x) > 0 and ch.x[-1] > 10:
            # scroll center of the scene with x
            new_x_center = (ch.x[0]+ch.x[-1])/2.
            self.scene.center = (new_x_center,0,0)
            self.updateTicks(ch.x,ch.y)
            self.grid.x = new_x_center
            self.ticklabels.x = new_x_center
            
            # shift curve and append
            
            ch.pos[:-1] = ch.pos[1:]
            ch.pos[-1] = point
        else:
            ch.append(pos=point)

if __name__=='__main__':
    st = Strip(2)
    ch1 = st.channels[0]
    ch2 = st.channels[1]
    start = time.clock()
    for i in arange(-10,200,.1):
        st.plot(ch1,(i,10*sin(i),0))
        st.plot(ch2,(i,10*cos(i)+random(),0))
        #rate(50)#set maximum frame rate

    print "frame rate: ", 1/((time.clock()-start)/210.)
