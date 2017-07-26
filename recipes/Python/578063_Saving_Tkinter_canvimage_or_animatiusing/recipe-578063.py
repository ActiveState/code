from Tkinter import *
from PIL import ImageGrab
from numpy import array
import os

class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.overrideredirect(1) # FRAMELESS CANVAS WINDOW

        self.width = 900
        self.height = 640
        self.initialize()

    def initialize(self):
        self.c = Canvas(self, width=self.width, height=self.height, background='white')
        self.c.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.update() # DISPLAY THE CANVAS

        self.run_anim() # RUN ANIMATION METHOD
        self.destroy() # CLOSE THE FRAMELESS CANVAS WHEN COMPLETED

    def run_anim(self):
        print os.getcwd() # REMINDER OF THE CURRENT SAVE LOCATION
        c = self.c
        polyo = array([34,60,226,15,419,60,359,151,91,151])
        polyd = array([205,253,296,187,388,253,353,360,239,360])
        trantime = 20 # NUMBER OF FRAMES TO WRITE (TRANSITION TIME)
        for i in xrange(trantime):
            c.delete('pol')
            ptrans = (float(i)/trantime)*polyd+(trantime-float(i))/trantime*polyo
            c.create_polygon(list(ptrans), outline='black', fill='red', tags='pol')

            self.update() # UPDATE THE CANVAS DISPLAY
            savename = 'im_{0:0>6}'.format(i)
            ImageGrab.grab((0,0,self.width,self.height)).save(savename + '.jpg')

app = App(None)
app.mainloop()
