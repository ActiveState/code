"""aebovl -- overlay bracketed exposures to create a composite image

Usage:
  aebovl -l<val> [-d<val> -a<val> -m -h] <normal> <under> <over>
Where:
  -l <val>  light limit (0-255). Pixels lighter than this value are considered
     to be too light. Default: 127
  -d <val>  dark limit (0-255). Pixels darker than this values are considered
     to be too dark. Optional. If omitted, the dark limit is set to 
     255 - light limit.
  -a <val>  alpha. Adjusts level of blending between images. Optional, range
     1 - 255, default is 1. 1 means use all of the light or dark image, 255
     means use all of the normal image. Values in between give a blend.
  -f <val>  apply a filter. Optional. Default: no filter. Filters are:
     BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, 
     FIND_EDGES, SMOOTH, SMOOTH_MORE, and SHARPEN.
  -b Blur masks. Blur the light and dark masks to soften the overlays and help
     smooth transitions.
  -m Save mask image. A composite of the masks is saved for reference as 
     overlay-cm.jpg. Optional. The composite mask shows light areas
     as white, normal areas as gray and dark areas as black.
  -h Help 
  <normal>  Normally exposed image. Required.
  <under>   Under-exposed (dark) image. Required.         
  <over>    Over-exposed (light) image. Required.
Output:
  Results are saved as overlay*.JPG in the current directory
Notes:
  Generally it is easiest to focus on getting the largest uniform section of the
  image right (e.g. the sky), then fine tuning from there. Try using -l120 -m
  initially, and reduce -l by 10 until the sky is uniformaly darkened. Then set
  -d to 255-l, and continue to adjust -l independantly of -d until you are happy
  with the rest of the image. Try high and low values of -l. Finally add -b and
  see if this improves the effect.
Example work flow:
  Start: 
    aebovl -l120 -m normal.jpg under.jpg over.jpg
  Adjust in increments of 10 until sky looks good, perhaps something like:
    aebovl -l70 -m normal.jpg under.jpg over.jpg
  Fix -d at 255-70:
    aebovl -l80 -d185 -m normal.jpg under.jpg over.jpg
  Continue to adjust -l until main subject is how you want it:
    aebovl -l35 -d185 -m normal.jpg under.jpg over.jpg
  Now try -b, and see if it helps:
    aebovl -l35 -d185 -b normal.jpg under.jpg over.jpg 
"""  

import sys
import Image, ImageFilter
import getopt
from getopt import GetoptError

VALID_FILTERS = ["BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", 
    "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", "SMOOTH", 
    "SMOOTH_MORE", "SHARPEN"]

def abort(code, msg):
    sys.stderr.write(msg + '\n')
    sys.stderr.write('Run expovl -h for help\n') 
    sys.exit(code)

def main():
    # Get command line parameters
    getoptstring = 'bhml:d:a:f:'
    try:
        opts, args = getopt.getopt(sys.argv[1:], getoptstring)
    except GetoptError:
        abort(2, "Invalid or missing command line option")
    llimit = 127
    dlimit = None
    alpha = 1
    savemasks = False
    filter = None
    blurmasks = False
    help = False
    outfilename = "overlay.jpg"
    for opt, val in opts:
        if opt == "-l": llimit = int(val)    
        if opt == "-d": dlimit = int(val)
        if opt == "-m": savemasks = True    
        if opt == "-h": help = True
        if opt == "-a": alpha = int(val)
        if opt == "-b": blurmasks = True
        if opt == "-f": filter = val.upper()
    if help:
        print __doc__
        sys.exit(0)
    if dlimit is None: dlimit = 255 - llimit
    if len(args) != 3: 
        abort(1, "Three input image files required.")
    if filter is not None and filter not in VALID_FILTERS:
        abort(3, "Invalid filter specified")
    midimgfile, darkimgfile, lightimgfile = args
     
    print "Loading images ..."
    midimg = Image.open(midimgfile).convert("RGB")
    darkimg = Image.open(darkimgfile).convert("RGB")
    lightimg = Image.open(lightimgfile).convert("RGB")
    gsimg = midimg.convert("L")
    
    print "Processing images ..."
    lightmask = gsimg.point(lambda i: ((i < llimit) * alpha) or 255)
    darkmask = gsimg.point(lambda i: ((i > dlimit) * alpha) or 255)
    if blurmasks:
	    lightmask = lightmask.filter(ImageFilter.BLUR)
	    darkmask = darkmask.filter(ImageFilter.BLUR)
    resimg = Image.composite(midimg, lightimg, lightmask)
    resimg = Image.composite(resimg, darkimg, darkmask)
    
    if filter is not None:
        resimg = resimg.filter(getattr(ImageFilter, filter))
    
    print "Saving image file(s) ..."
    resimg.save("overlay.JPG")
    if savemasks:
    	# Recreate the masks without using the alpha factor, so the composite
    	# mask is composed of white, mid-gray and black, not shades in between
        lightmask = gsimg.point(lambda i: (i < llimit) or 255)
        darkmask = gsimg.point(lambda i: (i > dlimit) or 255)
        if blurmasks:
            lightmask = lightmask.filter(ImageFilter.BLUR)
            darkmask = darkmask.filter(ImageFilter.BLUR)
        gimg = Image.new("L", midimg.size, 128)
        wimg = Image.new("L", midimg.size, 0)
        bimg = Image.new("L", midimg.size, 255)
        compmask = Image.composite(gimg, wimg, lightmask)
        compmask = Image.composite(compmask, bimg, darkmask)
        compmask.save("overlay-cm.JPG")
    print "Results saved as overlay*.JPG"
    
main()
