# Tetration Fractal
# http://en.wikipedia.org/wiki/Tetration
# FB - 201110237
import math
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
# drawing area (xa < xb & ya < yb)
xa = -1.5
xb = -0.75
ya = 0.0
yb = 0.75
maxIt = 256 # max number of iterations allowed
for ky in range(imgy):
    for kx in range(imgx):
        x = xa + (xb - xa) * kx / (imgx - 1)
        y = ya + (yb - ya) * ky / (imgy - 1)
        for i in range(maxIt):
            try:
                e = math.exp(-0.5 * math.pi * y)
                p = math.pi * x / 2
                x = e * math.cos(p)
                y = e * math.sin(p)
            except:
                break
            if math.hypot(x, y) > 1000000:
                break
        image.putpixel((kx, ky), (i % 4 * 64, i % 8 * 32, i % 16 * 16))
image.save("TetrationFractal.png", "PNG")
