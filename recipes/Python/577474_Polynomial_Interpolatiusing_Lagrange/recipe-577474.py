# Polynomial Interpolation (Curve-fitting) using Lagrange Polynomial
# http://en.wikipedia.org/wiki/Lagrange_polynomial
# FB - 201011276
import random
from PIL import Image, ImageDraw
imgx = 800
imgy = 600
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)

n = random.randint(3, 5) # of points for the curve to pass-thru
xList = []
yList = []
for i in range(n):
    x = random.random() * (imgx - 1)
    y = random.random() * (imgy - 1)
    xList.append(x)
    yList.append(y)

# calculate the Lagrange polynomial for each x
m = 100000 # of steps
for p in range(m):
    x = (imgx - 1) * p / (m - 1)
    y = 0.0
    for j in range(n):
        Lx = 1.0
        for k in range(n):
            if k != j:
                Lx = Lx * (x - xList[k]) / (xList[j] - xList[k])
        y = y + yList[j] * Lx
    if y >= 0 and y <= imgy - 1:
        image.putpixel((int(x), int(y)), (255, 255, 255))

# show the points used
cr = 5 # circle radius
for i in range(n):
    cx = int(xList[i])
    cy = int(yList[i])
    draw.ellipse((cx - cr, cy - cr, cx + cr, cy + cr))
    
image.save("Polynomial_Interpolation.png", "PNG")
