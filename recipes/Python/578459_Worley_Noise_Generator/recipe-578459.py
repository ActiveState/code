# Worley Noise Generator
# http://en.wikipedia.org/wiki/Worley_noise
# FB36 - 20130216
import math
import random
from PIL import Image, ImageDraw
imgx = 500; imgy = 500 # image size
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
n = 100 # of seed points
m = 0 # random.randint(0, n - 1) # degree (?)
seedsX = [random.randint(0, imgx - 1) for i in range(n)]
seedsY = [random.randint(0, imgy - 1) for i in range(n)]

# find max distance
maxDist = 0.0
for ky in range(imgy):
    for kx in range(imgx):
        # create a sorted list of distances to all seed points
        dists = [math.hypot(seedsX[i] - kx, seedsY[i] - ky) for i in range(n)]
        dists.sort()
        if dists[m] > maxDist: maxDist = dists[m]

# paint
for ky in range(imgy):
    for kx in range(imgx):
        # create a sorted list of distances to all seed points
        dists = [math.hypot(seedsX[i] - kx, seedsY[i] - ky) for i in range(n)]
        dists.sort()
        c = int(round(255 * dists[m] / maxDist))
        pixels[kx, ky] = (0, 0, c) 

label = "N = " + str(n) + " M = " + str(m)
draw.text((0, 0), label, (0, 255, 0)) # write to top-left using green color
image.save("WorleyNoise.png", "PNG")
