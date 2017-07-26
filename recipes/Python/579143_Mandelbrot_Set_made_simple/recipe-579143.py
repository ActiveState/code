"""
recipe_mandelbrot.py

A mini-framework for exploring the Mandelbrot set. 

The Mandelbrot Set is the set of points which when iterated over by a
particular math procedure repeatedly, the cumulative value does not go  
to infinity. There are more complete explanations elsewhere.

Suffice it to say that the output of calc_mandelbrot_set() returns
an array of values for how quickly the point escaped to infinity, which 
has been proven equivalent to the absolute value of the cumulative value > 2.

If the point does not escape, its escape value equals the maximum number
of iterations. The higher the number of iterations, the more accurate
the output of calc_mandelbrot_values().

Strictly speaking the Mandelbrot Set, as calculated here, is only the 
points whose escape values equal the maximum number of iterations. 
Rendering those points as black presents the standard bug-shaped image.

The spectacular colored Mandelbrot images are created by mapping all the 
escape values to various colors. There any number of color mapping schemes.
The art of exploring the Mandelbrot Set visually is choosing or creating
a mapping which works with the region of the Set one has calculated.
(The smaller the region, the higher the number of iterations should be
used.)

In this recipe escapevals_to_color() provides one such mapping. Change
that function to change the color mapping.

Since it is time-consuming to calculate the Mandelbrot escape values,
it's convenient to cache the calculations to disk, then use the cached
values as one experiments with color mappings.

This recipe contains a disk caching mechanism which saves the calculations
from one run to a file. The parameters of those calculations are encoded
in the filename, so the next time those particular calculations are
required, the recipe will find those calculations automatically.

The recipe outputs to a PNG file and to a Tkinter window. The PNG file 
output requires installation of the Pillow version of the Python Imaging 
Library. 

Suggestions:

* Run the recipe as is to see the output in Tkinter.
* Experiment by varying the number of iterations (MAX_ITERS).
* Experiment by varying the graph rectangle (X_MIN, X_MAX, Y_MIN, Y_MAX).
* Experiment by changing the color mapping function (escapeval_to_color).
"""
__author__ = "Jack Trainor"
__date__ = "2015-12-28"

import sys
import re
import os.path
import time
import array

########################################################################
""" 
Customize these constants 

IMG_WD/IMG_HT should be set roughly equal to (X_MAX-XMIN)/(Y_MAX-Y_MIN).
"""
MAX_ITERS = 250
IMG_WD = 400
IMG_HT = 400
X_MIN = -2.125
X_MAX = 0.875
Y_MIN = -1.5
Y_MAX = 1.5
OUTPUT_DIR = "C:/"
DISK_CACHING = True

########################################################################
def calc_mandelbrot_vals(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    escapevals = []
    xwd = xmax - xmin
    yht = ymax - ymin
    for y in range(imght):
        for x in range(imgwd):
            z  = 0
            r = xmin + xwd * x / imgwd
            i = ymin + yht * y / imght
            c = complex(r, i)  
            for n in range(maxiters + 1):
                z = z*z + c
                if abs(z) > 2.0:  # escape radius
                    break
            escapevals.append(n)
    return escapevals

########################################################################
def escapeval_to_color(n, maxiters):
    """ 
    http://www.fractalforums.com/index.php?topic=643.msg3522#msg3522
    """
    v = float(n) / float(maxiters)
    n = int(v * 4096.0)
    
    r = g = b = 0
    if (n == maxiters):
        pass
    elif (n < 64):
        r = n * 2
    elif (n < 128):
        r = (((n - 64) * 128) / 126) + 128
    elif (n < 256):
        r = (((n - 128) * 62) / 127) + 193
    elif (n < 512):
        r = 255
        g = (((n - 256) * 62) / 255) + 1
    elif (n < 1024):
        r = 255
        g = (((n - 512) * 63) / 511) + 64
    elif (n < 2048):
        r = 255
        g = (((n - 1024) * 63) / 1023) + 128
    elif (n < 4096):
        r = 255
        g = (((n - 2048) * 63) / 2047) + 192
    
    return (int(r), int(g), int(b))

########################################################################
def get_mb_corename(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    return "mb_%d_wd_%d_ht_%d_xa_%f_xb_%f_ya_%f_yb_%f_" % (maxiters, imgwd, imght, xmin, xmax, ymin, ymax)

def extract_mb_filename(filename):
    maxiters = xmin = xmax = ymin = ymax = imgwd = imght = ""
    filename_re = re.compile("mb_(.+)_wd_(.+)_ht_(.+)_xa_(.+)_xb_(.+)_ya_(.+)_yb_(.+)_.*")
    match = filename_re.match(filename)
    if match:
        maxiters = int(match.group(1))
        imgwd = int(match.group(2))
        imght = int(match.group(3))
        xmin = float(match.group(4))
        xmax = float(match.group(5))
        ymin = float(match.group(6))
        ymax = float(match.group(7))
    return maxiters, xmin, xmax, ymin, ymax, imgwd, imght
    
########################################################################
def write_mb(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    escapevals = calc_mandelbrot_vals(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
    path = get_mb_path(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
    write_array_file(path, escapevals, 'i')
    
def read_mb(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    path = get_mb_path(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
    array_ = read_array_file(path, 'i', imght*imgwd)
    return array_

def get_mb_path(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    corename = get_mb_corename(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
    path = os.path.join(OUTPUT_DIR, corename+".data")
    return path
    
########################################################################  
def write_array_file(path, list_, typecode):
    array_ = array.array(typecode, list_)
    f = open(path, "wb")
    array_.tofile(f)
    f.close()    
    
def read_array_file(path, typecode, count):
    f = open(path, 'rb')
    array_ = array.array(typecode)
    array_.fromfile(f, count)
    return array_

########################################################################  
def get_mandelbrot(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    if DISK_CACHING:
        path = get_mb_path(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
        if not os.path.exists(path):
            write_mb(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
        return read_mb(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
    else:
        return calc_mandelbrot_vals(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)

########################################################################
def mb_to_png(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    try:
        from PIL import Image
        from PIL import ImageDraw
        array_ = get_mandelbrot(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
        img = Image.new("RGB", (imgwd, imght))
        d = ImageDraw.Draw(img)
     
        i = 0
        for y in range(imght):
            for x in range(imgwd):
                n = array_[i]
                color = escapeval_to_color(n, maxiters)
                d.point((x, y), fill=color)
                i += 1
          
        del d
        corename = get_mb_corename(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
        path = os.path.join(OUTPUT_DIR, corename+".png")
        img.save(path)
    except ImportError:
        println("mb_to_png failed: Pillow not installed.")
  
########################################################################
def mb_to_tkinter(maxiters, xmin, xmax, ymin, ymax, imgwd, imght):
    try:
        import tkinter as tk
    except ImportError:
        import Tkinter as tk
    
    array_ = get_mandelbrot(maxiters, xmin, xmax, ymin, ymax, imgwd, imght)
    window = tk.Tk()
    canvas = tk.Canvas(window, width=imgwd, height=imght, bg="#000000")
    img = tk.PhotoImage(width=imgwd, height=imght)
    canvas.create_image((0, 0), image=img, state="normal", anchor=tk.NW)

    i = 0
    for y in range(imght):
        for x in range(imgwd):
            n = array_[i]
            color = escapeval_to_color(n, maxiters)
            r = hex(color[0])[2:].zfill(2)
            g = hex(color[1])[2:].zfill(2)
            b = hex(color[2])[2:].zfill(2)
            img.put("#" + r + g + b, (x, y))     
            i += 1
            
    println("mb_to_tkinter %s" % time.asctime())
    canvas.pack()
    tk.mainloop()
  
########################################################################
def main():
    println("Start         %s" % time.asctime())
    mb_to_png(MAX_ITERS, X_MIN, X_MAX, Y_MIN, Y_MAX, IMG_WD, IMG_HT)
    println("mb_to_png     %s" % time.asctime())
    mb_to_tkinter(MAX_ITERS, X_MIN, X_MAX, Y_MIN, Y_MAX, IMG_WD, IMG_HT)
    
########################################################################
def println(text):
    sys.stdout.write(text + "\n")

if __name__ == "__main__":
    main()
