# SuperHelix
# FB - 201007213
import math
from PIL import Image
imgx = 800
imgy = 800
image = Image.new("RGB", (imgx, imgy))

r0 = float(300) # radius of the 1. helix
r1 = float(30)  # radius of the 2. helix
r2 = float(10)  # radius of the 3. helix

ctr = 0
while True:
    ctr += 1
    
    # 1. helix point
    a0 = float(ctr) / r0 / 10
    x0 = r0 * math.cos(a0)
    y0 = r0 * math.sin(a0)
    z0 = float(ctr) * 0.01

    # plot the 1. helix point
    if z0 > imgy - 1: break
    image.putpixel((x0 + imgx / 2, z0), (255, 0, 0))
    
    # 2. helix point (superhelix)
    a1 = float(ctr) / r1 / 2
    x1 = x0 + r1 * math.cos(a1) * math.cos(a0)
    y1 = y0 + r1 * math.cos(a1) * math.sin(a0)
    z1 = z0 + r1 * math.sin(a1)

    # plot the 2. helix point
    if z1 < 0: z1 = 0
    if z1 > imgy - 1: break
    image.putpixel((x1 + imgx / 2, z1), (0, 0, 255))

    # 3. helix point (hyperhelix?)
    a2 = float(ctr) / r2
    x2 = x1 + r2 * math.cos(a2) * math.cos(a1)
    y2 = y1 + r2 * math.cos(a2) * math.sin(a1)
    z2 = z1 + r2 * math.sin(a2)

    # plot the 3. helix point
    if z2 < 0: z2 = 0
    if z2 > imgy - 1: break

    image.putpixel((x2 + imgx / 2, z2), (0, 255, 0))

image.save("SuperHelix.png", "PNG")
