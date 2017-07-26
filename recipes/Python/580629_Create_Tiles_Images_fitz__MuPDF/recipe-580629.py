#!/usr/bin/python
# -*- coding: utf-8 -*-
import fitz                    # this is PyMuPDF

'''
Created on Fri Jan 08 17:00:00 2016

@author: Jorj X. McKie

===============================================================================
PyMuPDF demo program - updated to PyMuPDF 1.9
---------------------------------------------
Demonstrates some of MuPDF's non-PDF graphic capabilities.

Read an image and create a new one consisting of 3 * 4 tiles of it.
===============================================================================
'''
# create a pixel map from any supported image file: BMP, JPEG, PNG, GIF, TIFF, JXR
pix0 = fitz.Pixmap("supported_img.xxx")          # create a pixel map from file

# calculate target pixmap colorspace and dimensions, then create it
tar_csp    = pix0.getColorspace()                     # copy input's colorspace
tar_width  = pix0.width * 3                           # 3 columns
tar_height = pix0.height * 4                          # 4 rows
tar_irect  = fitz.IRect(0, 0, tar_width, tar_height)  # we need to define a target rectangle
tar_pix    = fitz.Pixmap(tar_csp, tar_irect)          # now create target pixel map
tar_pix.clearWith(90)        # clear pixmap with a lively gray: (R, G, B) = (90, 90, 90)

# now fill target with 3 * 4 tiles of input picture
for i in list(range(4)):
    pix0.y = i * pix0.height                          # modify input's y coord
    for j in list(range(3)):
        pix0.x = j * pix0.width                       # modify input's x coord
        tar_pix.copyPixmap(pix0, pix0.getIRect())     # copy input to new loc
        # save intermediate images too, to display what is happening
        fn = "target-" + str(i) + str(j) + ".png"
        tar_pix.writePNG(fn)
