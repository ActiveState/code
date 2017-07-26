# clock.py  By Anton Vredegoor (anton.vredegoor@gmail.com) 
# last edit: july 2009,
# license: GPL
# enjoy!

"""
A very simple  clock.

The program transforms worldcoordinates into screencoordinates 
and vice versa according to an algorithm found in: "Programming 
principles in computer graphics" by Leendert Ammeraal.

"""

from Tkinter import *
from time import localtime
from datetime import timedelta,datetime
from math import sin, cos, pi
import sys, types, os

_inidle = type(sys.stdin) == types.InstanceType and \
	  sys.stdin.__class__.__name__ == 'PyShell'

class transformer:

    def __init__(self, world, viewport):
        self.world = world 
        self.viewport = viewport

    def point(self, x, y):
        x_min, y_min, x_max, y_max = self.world
        X_min, Y_min, X_max, Y_max = self.viewport
        f_x = float(X_max-X_min) /float(x_max-x_min) 
        f_y = float(Y_max-Y_min) / float(y_max-y_min) 
        f = min(f_x,f_y)
        x_c = 0.5 * (x_min + x_max)
        y_c = 0.5 * (y_min + y_max)
        X_c = 0.5 * (X_min + X_max)
        Y_c = 0.5 * (Y_min + Y_max)
        c_1 = X_c - f * x_c
        c_2 = Y_c - f * y_c
        X = f * x + c_1
        Y = f * y + c_2
        return X , Y

    def twopoints(self,x1,y1,x2,y2):
        return self.point(x1,y1),self.point(x2,y2)

class clock:

    def __init__(self,root,deltahours = 0):
        self.world       = [-1,-1,1,1]
        self.bgcolor     = '#000000'
        self.circlecolor = '#808080'
        self.timecolor   = '#ffffff'
        self.circlesize  = 0.09
        self._ALL        = 'all'
        self.pad         = 25
        self.root        = root
        WIDTH, HEIGHT = 400, 400
        root.bind("<Escape>", lambda _ : root.destroy())
        self.delta = timedelta(hours = deltahours)  
        self.canvas = Canvas(root, 
                width       = WIDTH,
                height      = HEIGHT,
                background  = self.bgcolor)
        viewport = (self.pad,self.pad,WIDTH-self.pad,HEIGHT-self.pad)
        self.T = transformer(self.world,viewport)
        self.root.title('Clock')
        self.canvas.bind("<Configure>",self.configure())
        self.canvas.pack(fill=BOTH, expand=YES)
        self.poll()
 
    def configure(self):
        self.redraw()
    
    def redraw(self):
        sc = self.canvas
        sc.delete(self._ALL)
        width = sc.winfo_width()
        height =sc.winfo_height()
        sc.create_rectangle([[0,0],[width,height]],
                fill = self.bgcolor, tag = self._ALL)
        viewport = (self.pad,self.pad,width-self.pad,height-self.pad)
        self.T = transformer(self.world,viewport)
        self.paintgrafics()

    def paintgrafics(self):
        start = -pi/2
        step = pi/6
        for i in range(12):
            angle =  start+i*step
            x, y = cos(angle),sin(angle)
            self.paintcircle(x,y)
        self.painthms()
        self.paintcircle(0,0)
    
    def painthms(self):
        T = datetime.timetuple(datetime.utcnow()-self.delta)
        x,x,x,h,m,s,x,x,x = T
        self.root.title('%02i:%02i:%02i' %(h,m,s))
        angle = -pi/2 + (pi/6)*h + (pi/6)*(m/60.0)
        x, y = cos(angle)*.60,sin(angle)*.60   
        scl = self.canvas.create_line
        scl(apply(self.T.twopoints,[0,0,x,y]), fill = self.timecolor, 
                    tag =self._ALL, width = 6)
        angle = -pi/2 + (pi/30)*m + (pi/30)*(s/60.0)
        x, y = cos(angle)*.80,sin(angle)*.80   
        scl(apply(self.T.twopoints,[0,0,x,y]), fill = self.timecolor, 
                    tag =self._ALL, width = 3)
        angle = -pi/2 + (pi/30)*s
        x, y = cos(angle)*.95,sin(angle)*.95   
        scl(apply(self.T.twopoints, [0,0,x,y]), fill = self.timecolor,
                    tag =self._ALL, arrow = 'last')
    
    def paintcircle(self,x,y):
        ss = self.circlesize / 2.0
        mybbox = [-ss+x,-ss+y,ss+x,ss+y]
        sco = self.canvas.create_oval
        sco(apply(self.T.twopoints,mybbox), fill = self.circlecolor,
                    tag =self._ALL)
   
    def poll(self):
        self.configure()
        self.root.after(200,self.poll)

def main():
    root= Tk()
    # deltahours: how far are you from utc?
    # someone should automatize that, but I sometimes want to display
    # time as if I am in another timezone ...
    clock(root,deltahours = -2)
    if not _inidle:
        root.mainloop()

if __name__=='__main__':
  main()
