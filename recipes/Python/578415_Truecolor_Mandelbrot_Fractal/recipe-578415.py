# True-color Mandelbrot Fractal
# FB36 - 20130113
import math
from PIL import Image
imgx = 800; imgy = 800
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
xa = -2.0; xb = 1.0
ya = -1.5; yb = 1.5
maxIt = 256 # of iterations

# find max values for |x|, |y|, |z|
maxAbsX = 0.0; maxAbsY = 0.0; maxAbsZ = 0.0
for ky in range(imgy):
    b = ky * (yb - ya) / (imgy - 1)  + ya
    for kx in range(imgx):
        a = kx * (xb - xa) / (imgx - 1)  + xa
        c = complex(a, b); z = c
        for i in range(maxIt):
            z = z * z + c
            if abs(z) > 2.0: break
        if abs(z.real) > maxAbsX: maxAbsX = abs(z.real)
        if abs(z.imag) > maxAbsY: maxAbsY = abs(z.imag)
        if abs(z) > maxAbsZ: maxAbsZ = abs(z)

# paint
for ky in range(imgy):
    b = ky * (yb - ya) / (imgy - 1)  + ya
    for kx in range(imgx):
        a = kx * (xb - xa) / (imgx - 1)  + xa
        c = complex(a, b); z = c
        for i in range(maxIt):
            z = z * z + c
            if abs(z) > 2.0: break
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
image.save("MandelbrotFractal.png", "PNG")
