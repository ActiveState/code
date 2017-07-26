# Snowflake Simulation Using Reiter Cellular Automata
# Source: "A Local Cellular Model for Snow Crystal Growth" by Cliff Reiter
# FB36 - 20130107
import math
import random
from PIL import Image, ImageDraw
imgx = 500; imgy = 500 # image size
imgx1 = imgx - 1; imgy1 = imgy - 1
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
maxIt = 1000 # of growth steps
# snowflake will differ depending on values of these parameters:
alpha = random.random() * 1.5 + 0.5
beta = random.random() * 0.3 + 0.3
gamma = random.random() * 0.01
mx = 250; my = 250 # width and height of 2DCA
ca = [[beta for x in range(mx)] for y in range(my)]
caRep = [[beta for x in range(mx)] for y in range(my)] # receptive cells
caNRep = [[beta for x in range(mx)] for y in range(my)] # non-receptive cells
dx = [-1, 0, -1, 1, 0, 1]; dy = [-1, -1, 0, 0, 1, 1] # 6 directions to grow
# these are for coloring the image
while True:
    mr0 = 2 ** random.randint(3, 6); mr1 = 256 / mr0
    mg0 = 2 ** random.randint(3, 6); mg1 = 256 / mg0
    mb0 = 2 ** random.randint(3, 6); mb1 = 256 / mb0
    if mr0 != mg0 and mr0 != mb0 and mg0 != mb0: break

ca[(my - 1) / 2][(mx - 1) / 2] = 1.0 # ice seed
for i in range(maxIt): # growth steps
    print "Growth Step: " + str(i + 1) + " of " + str(maxIt)
    # separate the array into receptive and non-receptive arrays
    for iy in range(my):
        for ix in range(mx):
            receptive = False
            if ca[iy][ix] >= 1.0: # ice
                receptive = True
            else: # check neighbors
                for j in range(6):
                    jx = ix + dx[j]; jy = iy + dy[j]
                    if jx >= 0 and jx < mx and jy >= 0 and jy < my:
                        if ca[jy][jx] >= 1.0: # ice
                            receptive = True
                            break
            if receptive:
                caRep[iy][ix] = ca[iy][ix] + gamma
                caNRep[iy][ix] = 0.0
            else:
                caRep[iy][ix] = 0.0
                caNRep[iy][ix] = ca[iy][ix]

    # new array: weighed averages of the non-receptive array + receptive array
    for iy in range(my):
        for ix in range(mx):
            wsum = caNRep[iy][ix] * (1.0 - alpha * 6.0 / 12.0)
            for j in range(6): # neighbors
                jx = ix + dx[j]; jy = iy + dy[j]
                if jx >= 0 and jx < mx and jy >= 0 and jy < my:
                    wsum += caNRep[jy][jx] * alpha / 12.0
            ca[iy][ix] = caRep[iy][ix] + wsum

# paint final state of the snowflake
an45 = - math.pi / 4.0
sn45 = math.sin(an45); cs45 = math.cos(an45)
scale = math.sqrt(3.0); ox = imgx1 / 2.0; oy = imgy1 / 2.0
for ky in range(imgy):
    for kx in range(imgx):
        # apply geometric transformation (scaling and rotation)
        tx = kx - ox; ty = (ky - oy) * scale
        tx0 = tx * cs45 - ty * sn45 + ox
        ty = tx * sn45 + ty * cs45 + oy; tx = tx0
        if tx >= 0 and tx <= imgx1 and ty >= 0 and ty <= imgy1:
            c = ca[int((my - 1) * ty / imgy1)][int((mx - 1) * tx / imgx1)]
            if c >= 1.0: # ice
                c = int((c - 1.0) * 255)
                pixels[kx, ky] = (c % mr0 * mr1, c % mg0 * mg1, c % mb0 * mb1)
label = "alpha = " + str(alpha) + " beta = " + str(beta) + " gamma = " + str(gamma)
draw.text((0, 0), label, (0, 255, 0)) # write to top-left using green color
image.save("Snowflake.png", "PNG")
