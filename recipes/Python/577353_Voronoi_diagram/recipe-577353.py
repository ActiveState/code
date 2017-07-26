# Voronoi diagram
# FB - 201008087
import random
import math
from PIL import Image
imgx = 800
imgy = 600
image = Image.new("RGB", (imgx, imgy))

n = random.randint(50, 100) # of cells
nx = []
ny = []
nr = []
ng = []
nb = []
for i in range(n):
    nx.append(random.randint(0, imgx - 1))
    ny.append(random.randint(0, imgy - 1))
    nr.append(random.randint(0, 255))
    ng.append(random.randint(0, 255))
    nb.append(random.randint(0, 255))

for y in range(imgy):
    for x in range(imgx):
        # find the closest cell center
        dmin = math.hypot(imgx - 1, imgy - 1)
        j = -1
        for i in range(n):
            d = math.hypot(nx[i] - x, ny[i] - y)
            if d < dmin:
                dmin = d
                j = i
        
        image.putpixel((x, y), (nr[j], ng[j], nb[j]))

# mark the cell centers
for i in range(n):
    image.putpixel((nx[i], ny[i]),(255 - nr[i], 255 - ng[i], 255 - nb[i]))

image.save("Voronoi.png", "PNG")
