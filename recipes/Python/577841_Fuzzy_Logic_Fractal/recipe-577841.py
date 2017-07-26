# Fuzzy Logic Fractal
# See: Scientific American Magazine, February 1993, "A Partly True Story"
# http://en.wikipedia.org/wiki/Fuzzy_logic
# FB - 201108147
import math
from PIL import Image
# drawing area
xa = -1.2
xb = 1.2
ya = -1.2
yb = 1.2
maxIt = 255 # max iterations allowed
# image size
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
for ky in range(imgy):
    for kx in range(imgx):
        x = kx * (xb - xa) / (imgx - 1)  + xa
        y = ky * (yb - ya) / (imgy - 1)  + ya
        for i in range(maxIt):
            if math.hypot(x, y) > 1.1: break
            x0 = 1 - math.fabs(x - y)
            y = 1 - math.fabs(y - (1 - x))
            x = x0
        image.putpixel((kx, ky), (i % 8 * 32, i % 4 * 64, i % 16 * 16))
image.save("FuzzyLogicFractal.png", "PNG")
