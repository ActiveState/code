# Regular Polygon Fractals using iteration method
# FB - 201003206
from PIL import Image
import math
imgx = 512
imgy = 512
maxIt = 16 # max iterations allowed

for n in range(3, 9):
    image = Image.new("RGB", (imgx, imgy))
    m = n % 2
    p = float(n - m - 2.0) / 4.0 + 2.0
    q = p - 1.0
    af = 2.0 * math.pi / n
        
    for ky in range(imgy):
        for kx in range(imgx):
            x = kx * 2.0 / (imgx-1.0) - 1.0
            y = ky * 2.0 / (imgy-1.0) - 1.0
            for i in range(maxIt):      
                a = math.atan2(y, x)
                if a < 0:
                    a = 2.0 * math.pi - math.fabs(a)
                k = int(a / af) % n                
                x = x * p - math.cos(k * af + af / 2.0) * q
                y = y * p - math.sin(k * af + af / 2.0) * q
                if math.hypot(x, y) > 1.0:    
                    break

            r = i % 4 * 64
            g = i % 8 * 32
            b = i % 16 * 16
            image.putpixel((kx, ky), b * 65536 + g * 256 + r)

    image.save("rpItfr_" + str(n) + ".png", "PNG")
