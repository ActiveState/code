# Reaction-Diffusion Simulation Using Gray-Scott Model
# https://en.wikipedia.org/wiki/Reaction-diffusion_system
# FB - 20151016
import math
import random
from PIL import Image, ImageDraw
imgx = 256; imgy = 256 # image size
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
pixels = image.load()
steps = 1000
dA = 1.0 # Diffusion Rate A
dB = 0.5 # Diffusion Rate B
f = 0.0545
k = 0.062
h = 0.01 # time step size

# 3x3 Convolution Matrix
weights = [[0.05, 0.2, 0.05], [0.2, -1.0, 0.2], [0.05, 0.2, 0.05]]

##arA = [[[1.0 for x in range(imgx)] for y in range(imgy)] for z in range(2)]
##arB = [[[0.0 for x in range(imgx)] for y in range(imgy)] for z in range(2)]
##arB[0][(imgy - 1) / 2][(imgx - 1) / 2] = 1.0 # seed
arA = [[[random.random() for x in range(imgx)] for y in range(imgy)] for z in range(2)]
arB = [[[random.random() for x in range(imgx)] for y in range(imgy)] for z in range(2)]

# simulation
p = 0; print "%" + str(p).zfill(2)
z = 1
for i in range(steps):
    z = 1 - z
    for iy in range(imgy):
        for ix in range(imgx):
            lapA = 0.0
            lapB = 0.0
            for jy in range(3):
                for jx in range(3):
                    kx = ix + (jx - 1)
                    ky = iy + (jy - 1)
                    if kx < 0: kx = imgx - 1
                    if kx > imgx - 1: kx = 0
                    if ky < 0: ky = imgy - 1
                    if ky > imgy - 1: ky = 0
                    lapA += arA[z][ky][kx] * weights[jy][jx]
                    lapB += arB[z][ky][kx] * weights[jy][jx]
            a = arA[z][iy][ix]
            b = arB[z][iy][ix]
            abb = a * b * b
            an = a + (dA * lapA - abb + f * (1.0 - a)) * h
            bn = b + (dB * lapB + abb - (k + f) * b) * h
            # prevent negative chemical amounts
            if an < 0: an = 0.0
            if bn < 0: bn = 0.0
            arA[1 - z][iy][ix] = an
            arB[1 - z][iy][ix] = bn

    pn = 100 * (i + 1) / steps # percent completed
    if pn != p:
        p = pn
        print "%" + str(p).zfill(2)

# paint the final state
z = 1 - z
aMin = arA[z][0][0]; aMax = aMin
bMin = arB[z][0][0]; bMax = bMin
for iy in range(imgy):
    for ix in range(imgx):
        a = arA[z][iy][ix]
        b = arB[z][iy][ix]
        if a < aMin: aMin = a
        if a > aMax: aMax = a
        if b < bMin: bMin = b
        if b > bMax: bMax = b

if aMin != aMax:
    for iy in range(imgy):
        for ix in range(imgx):
            a = arA[z][iy][ix]
            cA = int(255 * (a - aMin) / (aMax - aMin))
            pixels[ix, iy] = (cA, cA, cA)
    # label = "f = " + str(f) + " k = " + str(k)
    # draw.text((0, 0), label, (0, 255, 0))
    image.save("ReactionDiffusionSim_A.png", "PNG")

if bMin != bMax:
    for iy in range(imgy):
        for ix in range(imgx):
            b = arB[z][iy][ix]
            cB = int(255 * (b - bMin) / (bMax - bMin))
            pixels[ix, iy] = (cB, cB, cB)
    # label = "f = " + str(f) + " k = " + str(k)
    # draw.text((0, 0), label, (0, 255, 0))
    image.save("ReactionDiffusionSim_B.png", "PNG")
