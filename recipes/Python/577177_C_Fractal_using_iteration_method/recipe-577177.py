# C Fractal using iteration method
# FB - 201004036
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
maxIt = 256 # max iterations allowed

for ky in range(imgy):
    for kx in range(imgx):
        x = float(kx) / (imgx - 1) * 2.0 + 0.5
        y = float(ky) / (imgy - 1) * 2.0 - 0.5
        for i in range(maxIt):
            if not (x < -0.5 or x > 1.5):
                t = x + y
                y = - x + y + 1.0
                x = t
            elif not (y < -0.25 or y > 1.0):
                t = x - y
                y = x + y - 2.0
                x = t
            else:
                break
        image.putpixel((kx, ky), (i % 8 * 32, 255 - i % 16 * 16, i % 16 * 16))

image.save("cFr.png", "PNG")
