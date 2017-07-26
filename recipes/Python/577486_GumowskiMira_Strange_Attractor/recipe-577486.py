# Gumowski-Mira Strange Attractor
# http://en.wikipedia.org/wiki/Attractor
# FB - 201012072
import random
from PIL import Image
imgx = 800
imgy = 600

maxIt = 50000 # number of pixels to draw
# drawing area (xa < xb and ya < yb)
xa = -20.0
xb = 20.0
ya = -20.0
yb = 20.0

def f(x):
    return a * x + 2.0 * (1.0 - a) * x * x / (1.0 + x * x)

def gm(x, y):
    xnew = b * y + f(x)
    y = -x + f(xnew)
    x = xnew
    return (x, y)

while True:    
    image = Image.new("L", (imgx, imgy)) # clear the image
    a = random.random() * 1.5 - 1.0
    b = random.random() * 0.1 + 0.9
    x = random.random() * (xb - xa) + xa
    y = random.random() * (yb - ya) + ya
    pixelCtr = 0
    for i in range(maxIt):
        (x, y) = gm(x, y)
        xi = int((imgx - 1) * (x - xa) / (xb - xa))
        yi = int((imgy - 1) * (y - ya) / (yb - ya))
        if xi >=0 and xi < imgx and yi >= 0 and yi < imgy:
            if image.getpixel((xi, yi)) == 0:
                image.putpixel((xi, yi), 255)
                pixelCtr += 1
    if 100 * pixelCtr / maxIt > 10: # retry until a good attractor is found
        break
    
image.save("strange_attractor.png", "PNG")
