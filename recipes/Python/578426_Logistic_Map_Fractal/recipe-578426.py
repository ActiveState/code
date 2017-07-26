# Logistic Map Fractal
# http://en.wikipedia.org/wiki/Logistic_map
# FB - 20130118
import random
import math
from PIL import Image, ImageDraw
imgx = 800; imgy = 800
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
maxIt = 256
xa = -0.5; xb = 1.5
ya = -1.0; yb = 1.0
zEsc = 1000
r = random.random() + 3.0
def f(z):
    for i in range(maxIt):
        z = r * z * (1.0 - z)
        if abs(z) > zEsc: break
    return z

maxAbsX = 0.0; maxAbsY = 0.0; maxAbsZ = 0.0
percent = 0
for ky in range(imgy):
    pc = 100 * ky / (imgy - 1)
    if pc > percent: percent = pc; print '%' + str(percent)
    y0 = ya + (yb - ya) * ky / (imgy - 1)
    for kx in range(imgx):
        x0 = xa + (xb - xa) * kx / (imgx - 1)
        z = f(complex(x0, y0))
        if abs(z.real) > maxAbsX: maxAbsX = abs(z.real)
        if abs(z.imag) > maxAbsY: maxAbsY = abs(z.imag)
        if abs(z) > maxAbsZ: maxAbsZ = abs(z)

percent = 0
for ky in range(imgy):
    pc = 100 * ky / (imgy - 1)
    if pc > percent: percent = pc; print '%' + str(percent)
    y0 = ya + (yb - ya) * ky / (imgy - 1)
    for kx in range(imgx):
        x0 = xa + (xb - xa) * kx / (imgx - 1)
        z = f(complex(x0, y0))
        v0 = int(255 * abs(z.real) / maxAbsX)
        v1 = int(255 * abs(z.imag) / maxAbsY)
        v2 = int(255 * abs(z) / maxAbsZ)
        v3 = int(255 * abs(math.atan2(z.imag, z.real)) / math.pi)
        v = v3 * 256 ** 3 + v2 * 256 ** 2 + v1 * 256 + v0
        colorRGB = int(16777215 * v / 256 ** 4)
        red = int(colorRGB / 65536)
        grn = int(colorRGB / 256) % 256
        blu = colorRGB % 256        
        pixels[kx, ky] = (red, grn, blu)    
draw.text((0, 0), "r = " + str(r), (0, 255, 0))
image.save("LogisticMapFractal.png", "PNG")
