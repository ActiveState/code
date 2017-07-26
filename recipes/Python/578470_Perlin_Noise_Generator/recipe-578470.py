# Perlin Noise Generator
# http://en.wikipedia.org/wiki/Perlin_noise
# http://en.wikipedia.org/wiki/Bilinear_interpolation
# FB36 - 20130222
import random
import math
from PIL import Image, ImageDraw
imgx = 800; imgy = 600 # image size
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
octaves = int(math.log(max(imgx, imgy), 2.0))
persistence = random.random()
imgAr = [[0.0 for i in range(imgx)] for j in range(imgy)] # image array
totAmp = 0.0
for k in range(octaves):
    freq = 2 ** k
    amp = persistence ** k
    totAmp += amp
    # create an image from n by m grid of random numbers (w/ amplitude)
    # using Bilinear Interpolation
    n = freq + 1; m = freq + 1 # grid size
    ar = [[random.random() * amp for i in range(n)] for j in range(m)]
    nx = imgx / (n - 1.0); ny = imgy / (m - 1.0)
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
            imgAr[ky][kx] += z # add image layers together

# paint image
for ky in range(imgy):
    for kx in range(imgx):
        c = int(imgAr[ky][kx] / totAmp * 255)
        pixels[kx, ky] = (c, c, c)

label = "Persistence = " + str(persistence)
draw.text((0, 0), label, (0, 255, 0)) # write to top-left using green color
image.save("PerlinNoise.png", "PNG")
