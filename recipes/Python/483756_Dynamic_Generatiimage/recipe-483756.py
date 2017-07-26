import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


# Fix this path to match your configuration
fontpath = "/usr/local/src/python/multimedia/Imaging-1.1.5/pilfonts"

def zope_txt2img(self, id, label, imgformat="PNG", **kw):
    """
    Copy this module to your Zope Instance Extensions directory,
    and after restarting Zope do create an External Method in ZMI
    following the example:

     Id - txt2img 
     Title - Convert text into image
     Module Name - txt2img.py
     Function Name - zope_txt2img

    """
    from OFS.Image import manage_addImage	
    imgfile = StringIO()
    img = txt2img(label, **kw)
    img.save(imgfile, imgformat)	
    manage_addImage(self, id, imgfile)

def txt2img(label, fontname="courB08.pil", imgformat="PNG",
            fgcolor=(0,0,0), bgcolor=(255,255,255),
            rotate_angle=0):
    """Render label as image."""
    font = ImageFont.load(os.path.join(fontpath,fontname))
    imgOut = Image.new("RGBA", (20,49), bgcolor)

    # calculate space needed to render text
    draw = ImageDraw.Draw(imgOut)
    sizex, sizey = draw.textsize(label, font=font)

    imgOut = imgOut.resize((sizex,sizey))

    # render label into image draw area
    draw = ImageDraw.Draw(imgOut)
    draw.text((0, 0), label, fill=fgcolor, font=font)

    if rotate_angle:
        imgOut = imgOut.rotate(rotate_angle)

    return imgOut



if __name__ == "__main__":
    img = txt2img("fulano@belex.com.br", "helvR10.pil")
    img.save('output.png')
