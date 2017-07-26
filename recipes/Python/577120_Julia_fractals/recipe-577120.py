# Julia fractals
# FB - 201003254
from PIL import Image
import random
# image size
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))

# drawing area
xa = -2.0
xb = 2.0
ya = -1.5
yb = 1.5
maxIt = 255 # max iterations allowed

# find a good Julia set point using the Mandelbrot set
while True:
    cx = random.random() * (xb - xa) + xa
    cy = random.random() * (yb - ya) + ya
    c = cx + cy * 1j
    z = c
    for i in range(maxIt):
        if abs(z) > 2.0:
            break 
        z = z * z + c
    if i > 10 and i < 100:
        break

# draw the Julia set
for y in range(imgy):
    zy = y * (yb - ya) / (imgy - 1)  + ya
    for x in range(imgx):
        zx = x * (xb - xa) / (imgx - 1)  + xa
        z = zx + zy * 1j
        for i in range(maxIt):
            if abs(z) > 2.0:
                break 
            z = z * z + c
        image.putpixel((x, y), (i % 8 * 32, i % 16 * 16, i % 32 * 8))

image.save("juliaFr.png", "PNG")
