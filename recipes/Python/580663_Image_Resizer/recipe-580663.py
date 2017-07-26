# Image Resizer/Converter [Batch Mode]
# Supported Formats:
# http://effbot.org/imagingbook/formats.htm
# FB36 - 20160521
from PIL import Image, ImageFilter 
import sys, os, glob
output = False
n = len(sys.argv)
if n < 3 or n > 7:
    usage = "USAGE:\n"
    usage += "[python] ImageResizer.py"
    usage += " [Path]ImageFileName [Format=...]"
    usage += " [Width=...] [Height=...] [Method=...] [Filter=...]\n"
    usage += "[]: optional argument!\n"
    usage += "Format: JPG/PNG/..."
    usage += "Method: NEAREST(Default)/BILINEAR/BICUBIC/ANTIALIAS\n"
    usage += "Filter: BLUR/CONTOUR/DETAIL/EDGE_ENHANCE/EDGE_ENHANCE_MORE"
    usage += "/EMBOSS/FIND_EDGES/SMOOTH/SMOOTH_MORE/SHARPEN\n"
    usage += "Use quotes if file paths/names contain spaces!\n"
    usage += "ImageFileName can contain wildcards (*/?)!"
    print usage
    os._exit(1) # sys.exit()
imageFilePath = sys.argv[1]
imgFormat = ""
width = 0
height = 0
method = ""
imgFilter = ""
for i in range(n - 2):
    args = sys.argv[i + 2].split("=")
    if args[0] == "Format":
        imgFormat = args[1].upper()
        ext = imgFormat
        if imgFormat == "JPG": imgFormat = "JPEG"
        if imgFormat == "TIF": imgFormat = "TIFF"
    if args[0] == "Width":
        width = int(args[1]) # in pixels
    if args[0] == "Height":
        height = int(args[1]) # in pixels
    if args[0] == "Method":
        method = args[1].upper()
    if args[0] == "Filter":
        imgFilter = args[1].upper()

fileList = glob.glob(imageFilePath)
for filePath in fileList:
    if output:
        print filePath
    image = Image.open(filePath)
    (imgWidth, imgHeight) = image.size
    if width == 0 and height == 0:
        imWidth = imgWidth
        imHeight = imgHeight
    elif width > 0 and height > 0:
        imWidth = width
        imHeight = height
    # preserve aspect ratio
    elif width > 0 and height == 0:
        imWidth = width
        imHeight = int(imgHeight * width / imgWidth)
    elif width == 0 and height > 0:
        imWidth = int(imgWidth * height / imgHeight)
        imHeight = height

    if method == "NEAREST":
        image = image.resize((imWidth, imHeight), Image.NEAREST)
    elif method == "BILINEAR":
        image = image.resize((imWidth, imHeight), Image.BILINEAR)
    elif method == "BICUBIC":
        image = image.resize((imWidth, imHeight), Image.BICUBIC)
    elif method == "ANTIALIAS":
        image = image.resize((imWidth, imHeight), Image.ANTIALIAS)
    else:
        image = image.resize((imWidth, imHeight))

    if imgFilter == "BLUR":
        image = image.filter(ImageFilter.BLUR)
    if imgFilter == "CONTOUR":
        image = image.filter(ImageFilter.CONTOUR)
    if imgFilter == "DETAIL":
        image = image.filter(ImageFilter.DETAIL)
    if imgFilter == "EDGE_ENHANCE":
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    if imgFilter == "EDGE_ENHANCE_MORE":
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if imgFilter == "EMBOSS":
        image = image.filter(ImageFilter.EMBOSS)
    if imgFilter == "FIND_EDGES":
        image = image.filter(ImageFilter.FIND_EDGES)
    if imgFilter == "SMOOTH":
        image = image.filter(ImageFilter.SMOOTH)
    if imgFilter == "SMOOTH_MORE":
        image = image.filter(ImageFilter.SMOOTH_MORE)
    if imgFilter == "SHARPEN":
        image = image.filter(ImageFilter.SHARPEN)

    if imgFormat != "":
        filePathStr = os.path.normpath(os.path.splitext(filePath)[0] + "." + ext)
        image.save(filePathStr, imgFormat)
    else:
        image.save(filePath)
