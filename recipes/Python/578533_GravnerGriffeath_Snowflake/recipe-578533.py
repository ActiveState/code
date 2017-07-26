# Gravner-Griffeath Snowflake Simulation
# http://psoup.math.wisc.edu/Snowfakes.htm
# "A typical simulated crystal reaches a final diameter of 400-600 cells
# over 10,000-100,000 updates (growth steps)..."
# FB36 - 20130526
import math; import random
from PIL import Image
imgx = 300; imgy = 300 # image size
imgx1 = imgx - 1; imgy1 = imgy - 1
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
ver = "deterministic" # random.choice(["deterministic", "randomized"])
print "Version: " + ver
maxIt = 3000 # 10000 - 100000 # of growth steps
p = 0.58 # random.random() * 0.6 + 0.3 # rho: homogeneous vapor density
k = random.random() * 0.05 # kappa
b = 2.0 # random.random() * 1.95 + 1.05 # beta
a = random.random() * 0.3 # alpha
t = random.random() * 0.5595 + 0.02 # theta
m = random.random() * 0.01 # mu
g = 0.0000515 # gamma
s = random.random() * -0.5 # sigma
print "Parameters:"
print "rho = ", p
print "kappa = ", k
print "beta = ", b
print "alpha = ", a
print "theta = ", t
print "mu = ", m
print "gamma = ", g
print "sigma = ", s
print

mx = imgx; my = imgy # width and height of 2DCA
dx = [-1, 0, -1, 1, 0, 1]; dy = [-1, -1, 0, 0, 1, 1] # 6 directions to grow
# set initial state
# ice cells belong to crystal
at = [[[0 for x in range(mx)] for y in range(my)] for z in range(2)]
# boundary masses of cells
bt = [[[0.0 for x in range(mx)] for y in range(my)] for z in range(2)]
# crystal masses of cells
ct = [[[0.0 for x in range(mx)] for y in range(my)] for z in range(2)]
# diffusive masses of cells
dt = [[[p for x in range(mx)] for y in range(my)] for z in range(2)]
# set ice seed
ox = (mx - 1) / 2; oy = (my - 1) / 2
at[0][oy][ox] = 1
ct[0][oy][ox] = 1.0
dt[0][oy][ox] = 0.0

def isBoundary(x, y):
    global dx, dy, at, za
    flag = False
    if at[za][y][x] == 0:
        for j in range(6): # neighbors
            jx = x + dx[j]; jy = y + dy[j]
            if jx >= 0 and jx < mx and jy >= 0 and jy < my:
                if at[za][jy][jx] == 1: flag = True; break
    return flag

def numIce(x, y): # of ice neighbors of boundary cell
    global dx, dy, at, za
    ni = 0
    if at[za][y][x] == 0:
        for j in range(6): # neighbors
            jx = x + dx[j]; jy = y + dy[j]
            if jx >= 0 and jx < mx and jy >= 0 and jy < my:
                if at[za][jy][jx] == 1: ni += 1
    return ni

# total diffusive mass
def difMass(x, y):
    global dx, dy, dt, zd
    wsum = dt[zd][y][x]
    for j in range(6): # neighbors
        jx = x + dx[j]; jy = y + dy[j]
        if jx >= 0 and jx < mx and jy >= 0 and jy < my:
            wsum += dt[zd][jy][jx]
    return wsum

za = 0; wa = 1
zb = 0; wb = 1
zc = 0; wc = 1
zd = 0; wd = 1

for i in range(maxIt): # growth steps
    print "Growth Step: " + str(i + 1) + " of " + str(maxIt)

    # step 1: diffusion
    for iy in range(my):
        for ix in range(mx):
            if not(at[za][iy][ix] == 1 or isBoundary(ix, iy)):
                dt[wd][iy][ix] = difMass(ix, iy) / 7.0
            elif isBoundary(ix, iy):
                wsum = dt[zd][iy][ix]
                for j in range(6): # neighbors
                    jx = ix + dx[j]; jy = iy + dy[j]
                    if jx >= 0 and jx < mx and jy >= 0 and jy < my:
                        if at[za][jy][jx] == 1:
                            wsum += dt[zd][iy][ix]
                        else:
                            wsum += dt[zd][jy][jx]                            
                dt[wd][iy][ix] = wsum / 7.0                
    zd = 1 - zd; wd = 1 - wd # switch planes

    # step 2: freezing
    for iy in range(my):
        for ix in range(mx):
            if isBoundary(ix, iy):
                bt[wb][iy][ix] = bt[zb][iy][ix] + (1.0 - k) * dt[zd][iy][ix]
                ct[wc][iy][ix] = ct[zc][iy][ix] + k * dt[zd][iy][ix]
                dt[wd][iy][ix] = 0.0    
    zb = 1 - zb; wb = 1 - wb # switch planes
    zc = 1 - zc; wc = 1 - wc # switch planes
    zd = 1 - zd; wd = 1 - wd # switch planes

    # step 3: attachment
    for iy in range(my):
        for ix in range(mx):
            nIce = numIce(ix, iy)
            if nIce > 0:
                if (nIce == 1 or nIce == 2) and bt[zb][iy][ix] >= b:
                    at[wa][iy][ix] = 1
                if nIce == 3:
                    if bt[zb][iy][ix] >= 1.0:
                        at[wa][iy][ix] = 1
                    elif bt[zb][iy][ix] >= a:
                        if difMass(ix, iy) < t: at[wa][iy][ix] = 1                        
                if nIce >= 4: at[wa][iy][ix] = 1
                if at[wa][iy][ix] == 1:
                    ct[wc][iy][ix] = bt[zb][iy][ix] + ct[zc][iy][ix];
                    bt[zb][iy][ix] = 0.0    
    za = 1 - za; wa = 1 - wa # switch planes
    zb = 1 - zb; wb = 1 - wb # switch planes
    zc = 1 - zc; wc = 1 - wc # switch planes

    # step 4: melting
    for iy in range(my):
        for ix in range(mx):
            if isBoundary(ix, iy):
                bt[wb][iy][ix] = bt[zb][iy][ix] * (1.0 - m)
                ct[wc][iy][ix] = ct[zc][iy][ix] * (1.0 - g)
                dt[wd][iy][ix] = dt[zd][iy][ix] + bt[zb][iy][ix] * m + ct[zc][iy][ix] * g    
    zb = 1 - zb; wb = 1 - wb # switch planes
    zc = 1 - zc; wc = 1 - wc # switch planes
    zd = 1 - zd; wd = 1 - wd # switch planes

    # step 5: noise
    if ver == "randomized":
        for iy in range(my):
            for ix in range(mx):
                if at[wa][iy][ix] == 0: # if not ice
                    dt[wd][iy][ix] = dt[zd][iy][ix] * (1.0 + s * random.choice([1, -1]))    
    zd = 1 - zd; wd = 1 - wd # switch planes

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
            c = at[wa][int((my - 1) * ty / imgy1)][int((mx - 1) * tx / imgx1)]
            pixels[kx, ky] = (c * 255, c * 255, c * 255)

image.save("Gravner-Griffeath_Snowfake_Simulation.png", "PNG")
