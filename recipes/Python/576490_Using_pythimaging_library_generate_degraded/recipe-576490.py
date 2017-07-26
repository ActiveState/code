"""This contains routines to generate degraded letter stimuli"""

import Image #The PIL
import ImageDraw
import ImageFont

import numpy

def generate_letter(contrast_energy = .01, #michelson contrast energy
                   noise = 30.,
                   bg_luminance = 128.,
                   letter = "a",
                   letter_size = 400):
 N = 300 #size of image in pixels

 #first figure out what is the ink-area of the letter

 font = ImageFont.truetype("Data/arial.ttf", letter_size)
 #we copy the .ttf file to the local directory to avoid problems

 im_temp = Image.new("1", (1,1), 0)
 draw = ImageDraw.Draw(im_temp)
 #now we can draw on this

 sz = draw.textsize(letter, font=font)
 #this tells us the size of the letter

 im_temp = Image.new("1", sz, 0)
 #this is a temporary binary image created solely for the purpose of computing
 #the ink-area of the letter
 draw = ImageDraw.Draw(im_temp)
 #now we can draw on this
 draw.text((0,0), letter, font=font, fill=1)
 pix = im_temp.load()
 #pix is now an addressable array of pixel values
 area_in_pixels = 0.
 for row in xrange(sz[0]):
   for col in xrange(sz[1]):
     area_in_pixels += pix[row,col]

 #since contrast_energy = contrast^2 * pixel_area
 contrast = (contrast_energy/area_in_pixels)**0.5
 fg_luminance = bg_luminance*(1+contrast)/(1-contrast)
 print area_in_pixels
 print contrast
 print fg_luminance


 im = Image.new("L", (N,N), bg_luminance)
 #im is now a NxN luminance image with luminance set to bg_luminance

 draw = ImageDraw.Draw(im)
 #now we can draw on this

 draw.text(((N-sz[0])/2, (N-sz[1])/2), letter, font=font, fill=fg_luminance)
 #this centers the letter

 if noise > 0:
   pix = im.load()
   #pix is now an addressable array of pixel values
  
   rd = numpy.random.normal(scale=noise, size=(N,N))
   for row in xrange(N):
     for col in xrange(N):
       pix[row,col] += rd[row,col]

 im.show()
