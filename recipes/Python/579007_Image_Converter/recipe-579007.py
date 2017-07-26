# Image Converter
# Supported Formats:
# http://effbot.org/imagingbook/formats.htm
from PIL import Image
import sys, os
if len(sys.argv) != 3:
    print "USAGE:"
    print "[python] ImageConverter.py InputImageFilePath OutputImageFilePath"
    print "Use quotes if file paths/names contain spaces!"
    os._exit(1) # sys.exit()
InputImageFilePath = sys.argv[1]
OutputImageFilePath = sys.argv[2]
imageFormat = ((os.path.splitext(OutputImageFilePath)[1])[1 : ]).upper()
if imageFormat == "JPG": imageFormat = "JPEG"
if imageFormat == "TIF": imageFormat = "TIFF"
image = Image.open(InputImageFilePath)
image.save(OutputImageFilePath, imageFormat)
