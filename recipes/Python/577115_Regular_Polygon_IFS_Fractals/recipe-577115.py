# Regular Polygon IFS Fractal
# FB - 201003151
from PIL import Image
import math
import random
# image size
imgx = 512
imgy = 512

for n in range(3, 8):
    image = Image.new("L", (imgx, imgy))
    m = n % 2
    p = (n - m + 2.0) / 4.0
    q = p + 1.0
    a = 2.0 * math.pi / n
    b = a / 2.0 * (1.0 - m)
    x = 0.0
    y = 0.0

    for i in range(imgx * imgy):
        k = random.randint(0, n - 1)
        c = k * a + b
        x = (x + math.sin(c)) / q
        y = (y + math.cos(c)) / q
        kx = int((x * p + 1.0) / 2.0 * (imgx - 1))            
        ky = int((y * p + 1.0) / 2.0 * (imgy - 1))            
        image.putpixel((kx, ky), 255)

    image.save("rpIFSfr_" + str(n) + ".png", "PNG")
