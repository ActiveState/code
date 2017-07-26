# Diffusion Limited Aggregation fractal
# FB - 201004036
from PIL import Image
import random
import math

imgx = 256
imgy = 256
image = Image.new("L", (imgx, imgy))

# neighbor pixel directions
nx = [-1, -1, 0, 1, 1, 1, 0, -1]
ny = [0, 1, 1, 1, 0, -1, -1, -1]

maxIt = 256

xc = (imgx - 1) / 2
yc = (imgy - 1) / 2
rmax = min(xc, yc) - 1
# seed
image.putpixel((xc, yc), 255) 

rm = 1.0
while rm < rmax:
    a = random.random() * math.pi * 2.0
    x = xc + rm * math.cos(a)
    y = yc + rm * math.sin(a)
    # random walk
    flag = False
    for i in range(maxIt):
        a = random.randint(0, 7)
        x = x + nx[a]
        y = y + ny[a]
        if x < 0 or x > (imgx - 1) or y < 0 or y > (imgy - 1):
            break
        if image.getpixel((x, y)) == 0:
            # check the neighbors
            for k in range(8):
                xn = x + nx[k]
                yn = y + ny[k]
                if image.getpixel((xn, yn)) > 0:
                    image.putpixel((x, y), 255)
                    r = math.sqrt((x - xc) ** 2.0 + (y - yc) ** 2.0)
                    if r > rm:
                        rm = r
                        print "%" + str(int(100 * rm / rmax))
                    flag = True
                    break
        if flag == True:
            break

image.save("DLA.png", "PNG")
