# Circle Inversion Fractals (Apollonian Gasket)
# FB36 - 20131029
import math
import random
from PIL import Image
imgx = 512; imgy = 512
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
n = random.randint(3, 6) # of main circles
a = math.pi * 2.0 / n
r = math.sin(a) / math.sin((math.pi - a) / 2.0) / 2.0 # r of main circles
h = math.sqrt(1.0 - r * r)
xa = -h; xb = h; ya = -h; yb = h # viewing area
cx = [0.0]; cy = [0.0]; cr = [1.0 - r] # center circle
for i in range(n): # add main circles
    cx.append(math.cos(a * i))
    cy.append(math.sin(a * i))
    cr.append(r)
maxIt = 100000 # of iterations
x = -2.0; y = -2.0 # initial point (outside of the circles)
for i in range(maxIt):
    k = random.randint(0, n) # selected circle for inversion
    dx = x - cx[k]; dy = y - cy[k]
    d = math.hypot(dx, dy)
    dx = dx / d; dy = dy / d
    dnew = cr[k] ** 2.0 / d
    x = dnew * dx + cx[k]
    y = dnew * dy + cy[k]
    kx = int((imgx - 1) * (x - xa) / (xb - xa))
    ky = int((imgy - 1) * (y - ya) / (yb - ya))
    try: pixels[kx, ky] = (255, 255, 255)
    except: pass
image.save("CircleInversionFractal_" + str(n) + ".png", "PNG")
