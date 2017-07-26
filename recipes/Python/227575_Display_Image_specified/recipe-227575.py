#HelloImage - display an image file
# Simon Peverett - October 2003
# uses the PIL module: http://www.pythonware.com/products/pil/
# developed using ActivePython 2.2: http://www.activestate.com

from Tkinter import *
import Image            #PIL
import ImageTk          #PIL
import sys
import getopt

try:
    if len(sys.argv) == 1:
        raise ValueError, "No image filename specified"

    #will raise file IO error if no file found
    im = Image.open(sys.argv[1]) 

    #print im.size, im.mode, im.format
    #print im.size[0]

    root = Tk()

    # add 20 to account for border defined in create_image
    canvas = Canvas(root, height=im.size[1]+20, width=im.size[0]+20)
    canvas.pack(side=LEFT,fill=BOTH,expand=1)

    photo = ImageTk.PhotoImage(im)
    item = canvas.create_image(10,10,anchor=NW, image=photo)
    mainloop()

except Exception, e:
    print >>sys.stderr, e
    print "USAGE: HelloImage <image filename>"
    sys.exit(1)
