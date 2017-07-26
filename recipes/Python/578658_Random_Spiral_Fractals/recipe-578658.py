# Random Spiral Fractals
# FB36 - 20130929
import math
import random
from collections import deque
from PIL import Image
imgx = 512; imgy = 512
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
xa = -1.5; xb = 1.5; ya = -1.5; yb = 1.5 # view
n = random.randint(2, 9) # of spiral arms
a = 2.0 * math.pi / n # angle between arms
t = 2.0 * math.pi * random.random() # rotation angle of central copy
r1 = 0.1 * random.random() + 0.1 # scale factor of outmost copies of the spiral arms
r0 = 1.0 - r1 # scale factor of central copy
ts = math.sin(t) * r0; tc = math.cos(t) * r0
maxIt = 64 # max number of iterations allowed
for ky in range(imgy):
    print str(100 * ky / (imgy - 1)).zfill(3) + "%"
    for kx in range(imgx):
        x = float(kx) / (imgx - 1) * (xb - xa) + xa
        y = float(ky) / (imgy - 1) * (yb - ya) + ya
        queue = deque([])
        queue.append((x, y, 0))
        while len(queue) > 0: # iterate points until none left
            (x, y, i) = queue.popleft()
            # apply all (inverse) IFS transformations
            for k in range(n + 1): # n outmost copies + central copy
                if k == n: # central copy
                    # inverse rotation and scaling
                    xnew = (y + x * tc / ts) / (ts + tc * tc / ts)
                    ynew = (y - x / tc * ts) / (tc + ts / tc * ts)
                else: # outmost copies on the spiral arms
                    c = k * a # angle
                    # inverse scaling and translation
                    xnew = (x - math.cos(c)) / r1
                    ynew = (y - math.sin(c)) / r1
                if xnew >= xa and xnew <= xb and ynew >= ya and ynew <= yb:
                    if i + 1 == maxIt: break
                    queue.append((xnew, ynew, i + 1))
        pixels[kx, ky] = (i % 16 * 16 , i % 8 * 32, i % 4 * 64)
image.save("RandomSpiralFractal_" + str(n) + ".png", "PNG")
