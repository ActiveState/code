# Random Surface Using Bilinear Interpolation
# http://en.wikipedia.org/wiki/Bilinear_interpolation
# FB36 - 20130222
import random
from PIL import Image, ImageDraw
imgx = 800; imgy = 600 # image size
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
n = random.randint(2, 10); m = random.randint(2, 10) # grid size
ar = [[random.random() for i in range(n)] for j in range(m)] # random grid
nx = imgx / (n - 1.0)
ny = imgy / (m - 1.0)
for ky in range(imgy):
    for kx in range(imgx):
        i = int(kx / nx); j = int(ky / ny)
        dx0 = kx - i * nx; dx1 = nx - dx0
        dy0 = ky - j * ny; dy1 = ny - dy0
        z = ar[j][i] * dx1 * dy1
        z += ar[j][i + 1] * dx0 * dy1
        z += ar[j + 1][i] * dx1 * dy0
        z += ar[j + 1][i + 1] * dx0 * dy0
        z /= nx * ny            
        c = int(z * 255)
        pixels[kx, ky] = (0, 0, c)

label = "N = " + str(n) + " M = " + str(m)
draw.text((0, 0), label, (0, 255, 0)) # write to top-left using green color
image.save("RandomSurface.png", "PNG")
