# Riemann Zeta Function Graph
# http://en.wikipedia.org/wiki/Riemann_zeta_function
# FB - 20130721
import math
from PIL import Image, ImageDraw
imgx = 512; imgy = 512
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
maxIt = 256
xa = -40.0; xb = 40.0
ya = -40.0; yb = 40.0

def f(z):
    t = 0.0
    for i in range(1, maxIt):
        t += 1.0 / i ** z
    return t

print "Finding max values of x, y, z..."
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

print "Drawing..."
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

st = str(xa) + " <= x <= " + str(xb) + " and " + str(ya) + " <= y <= " + str(yb)
draw.text((0, 0), st, (255, 0, 0))
image.save("RiemannZetaFunctionGraph.png", "PNG")
