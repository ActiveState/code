# by Antoni Gual Via 4/2015

from tkinter import Tk, Canvas, PhotoImage,NW,mainloop 
from time import clock

def mandel_pixel(c):
  """ calculates the color index of the mandelbrot plane point passed in the arguments """
  maxIt = 256
  z =  c   
  for i in range(maxIt):
      a = z * z
      z=a + c
      if a.real  >= 4.:
         return i
  return 256

def mandelbrot(xa,xb,ya,yb,x,y):
    """ returns a mandelbrot in a string for Tk PhotoImage"""
    #color string table in Photoimage format #RRGGBB 
    clr=[ ' #%02x%02x%02x' % (int(255*((i/255)**.25)),0,0) for i in range(256)]
    clr.append(' #000000')  #append the color of the centre as index 256
    #calculate mandelbrot x,y coordinates for each screen pixel
    xm=[xa + (xb - xa) * kx /x  for kx in range(x)]
    ym=[ya + (yb - ya) * ky /y  for ky in range(y)]
    #build the Photoimage string by calling mandel_pixel to index in the color table
    return" ".join((("{"+" ".join(clr[mandel_pixel(complex(i,j))] for i in xm))+"}" for j in ym))



#window size
x=640
y=480
#corners of  the mandelbrot plan to display  
xa = -2.0; xb = 1.0
ya = -1.27; yb = 1.27

#Tkinter window
window = Tk()
canvas = Canvas(window, width = x, height = y, bg = "#000000");canvas.pack()
img = PhotoImage(width = x, height = y)
canvas.create_image((0, 0), image = img, state = "normal", anchor = NW)

#do the mandelbrot 
t1=clock()
img.put(mandelbrot(xa,xb,ya,yb,x,y))
print(clock()-t1, ' seconds')

mainloop()
