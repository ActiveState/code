# Spiral IFS Fractals
# FB36 - 20130914
from PIL import Image
import math
import random
imgx = 1024; imgy = 1024
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
n = random.randint(2, 9)  # number of spiral arms
m = random.randint(5, 12) # number of spirals in each arm
a = 2.0 * math.pi / n     # angle between arms
b = 2.0 * math.pi * random.random() # max rotation (bending) angle for each arm
rmax = 0.1 * random.random() + 0.1 # max spiral radius on each arm
x = 0.0; y = 0.0
i = 0; p = 0
while True:
    k = random.randint(0, n - 1) # select an arm
    j = random.randint(0, m - 1) # select an spiral on the arm
    c = k * a + b * (j + 1.0) / m # angle of the spiral in the arm
    d = (j + 1.0) / m # distance of the spiral to the center
    r = d * rmax # radius of the spiral in the arm
    x = x * r + math.sin(c) * d
    y = y * r + math.cos(c) * d
    kx = int((x + 1.5) / 3.0 * (imgx - 1))            
    ky = int((y + 1.5) / 3.0 * (imgy - 1))
    if pixels[kx, ky] == (0, 0, 0):
        pixels[kx, ky] = (255, 255, 255)
        p += 1
    i += 1
    if 100 * p / i < 20: break
image.save("SpiralIFSFractal_" + str(n) + "_" + str(m) + ".png", "PNG")
