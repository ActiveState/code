# Dragon Fractal using IFS method
# FB - 20120106
import random
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
maxIt = 100000 # max iterations allowed

n = 6 # coloring level
color = [0] * n
red = []
grn = []
blu = []
for j in range(2):
    red.append(random.randint(0, 255))
    grn.append(random.randint(0, 255))
    blu.append(random.randint(0, 255))

xa = -1.0 / 3
xb = 7.0 / 6
ya = -1.0 / 3
yb = 2.0 / 3

x = 0.0
y = 0.0
for i in range(maxIt):
    k = random.randint(0, 1)
    for m in range(n - 1):
        color[m] = color[m + 1]
    color[n - 1] = k
    if k == 0:
        x0 = (x - y) / 2.0
        y = (x + y) / 2.0
        x = x0
    else:
        x0 = 1.0 - (x + y) / 2.0
        y = (x - y) / 2.0
        x = x0
    kx = int((x - xa) / (xb - xa) * (imgx - 1))
    ky = int((y - ya) / (yb - ya) * (imgy - 1))
    if kx >=0 and kx < imgx and ky >= 0 and ky <= imgy:
        image.putpixel((kx, ky), (red[color[0]], grn[color[0]], blu[color[0]]))

image.save("DragonFractal_IFS.png", "PNG")
