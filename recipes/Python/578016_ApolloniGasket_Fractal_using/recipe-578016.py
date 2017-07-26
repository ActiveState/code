# Apollonian Gasket Fractal using IFS
# FB - 20120114
import math
import random
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
maxIt = 100000 # of iterations

s = math.sqrt(3.0)
def f(z):
    return 3.0 / (1.0 + s - z) - (1.0 + s) / (2.0 + s)
ifs = ["f(z)", "f(z) * complex(-1.0, s) / 2.0", "f(z) * complex(-1.0, -s) / 2.0"]

xa = -0.6
xb = 0.9
ya = -0.75
yb = 0.75

z = complex(0.0, 0.0)
for i in range(maxIt):
    z = eval(ifs[random.randint(0, 2)]) 
    kx = int((z.real - xa) / (xb - xa) * (imgx - 1))
    ky = int((z.imag - ya) / (yb - ya) * (imgy - 1))
    if kx >=0 and kx < imgx and ky >= 0 and ky < imgy:
        image.putpixel((kx, ky), (255, 255, 255))

image.save("ApollonianGasket.png", "PNG")
