# plasma.py
# plasma fractal
# FB - 201003147
from PIL import Image
import math
import random

# image size
w = 512
h = 512
global image
image = Image.new("L", (w, h))
roughness = random.randint(2, 5)

def adjust(xa, ya, x, y, xb, yb):
    global image
    if(image.getpixel((x,y)) == 0):
      d=math.fabs(xa-xb) + math.fabs(ya-yb)
      v=(image.getpixel((xa,ya)) + image.getpixel((xb,yb)))/2.0 \
         + (random.random()-0.5) * d * roughness
      c=int(math.fabs(v) % 256)
      image.putpixel((x,y), c)

def subdivide(x1, y1, x2, y2):
    global image
    if(not((x2-x1 < 2.0) and (y2-y1 < 2.0))):
        x=int((x1 + x2)/2.0)
        y=int((y1 + y2)/2.0)
        adjust(x1,y1,x,y1,x2,y1)
        adjust(x2,y1,x2,y,x2,y2)
        adjust(x1,y2,x,y2,x2,y2)
        adjust(x1,y1,x1,y,x1,y2)
        if(image.getpixel((x,y)) == 0):
            v=int((image.getpixel((x1,y1)) + image.getpixel((x2,y1)) \
               + image.getpixel((x2,y2)) + image.getpixel((x1,y2)))/4.0)
            image.putpixel((x,y),v)

        subdivide(x1,y1,x,y)
        subdivide(x,y1,x2,y)
        subdivide(x,y,x2,y2)
        subdivide(x1,y,x,y2)


image.putpixel((0,0),random.randint(0, 255))
image.putpixel((w-1,0),random.randint(0, 255))
image.putpixel((w-1,h-1),random.randint(0, 255))
image.putpixel((0,h-1),random.randint(0, 255))
subdivide(0,0,w-1,h-1)
image.save("plasma.png", "PNG")
