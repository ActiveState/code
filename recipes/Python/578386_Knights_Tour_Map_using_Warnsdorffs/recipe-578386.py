# Knight's Tour Map using Warnsdorff's Rule
# http://en.wikipedia.org/wiki/Knight's_tour
# FB - 20121217
from heapq import heappush, heappop # for priority queue
import random
import time
from PIL import Image
imgx = 500; imgy = 500 # width and height of the image
cbx = 100; cby = 100 # width and height of the chessboard
maxItPercent = 10 # %100 => calculate the full tours
maxIt = cbx * cby * maxItPercent / 100
image = Image.new("RGB", (cbx, cby))
pixels = image.load()
while True:
    mr0 = 2 ** random.randint(3, 6); mr1 = 256 / mr0
    mg0 = 2 ** random.randint(3, 6); mg1 = 256 / mg0
    mb0 = 2 ** random.randint(3, 6); mb1 = 256 / mb0
    if mr0 != mg0 and mr0 != mb0 and mg0 != mb0: break
# directions the Knight can move on the chessboard
dx = [-2, -1, 1, 2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]
t = time.time()
for cy in range(cby):
    pc = 100.0 * cy / (cby - 1) # percent completed
    tp = time.time() - t # time passed in seconds
    print "%" + str(int(pc)), "in " + str(int(time.time() - t)) + "s.",
    if pc > 0:
        print str(int(100.0 * tp / pc - tp)) + "s remains..."
    else: print
    for cx in range(cbx):
        cb = [[0 for x in range(cbx)] for y in range(cby)] # chessboard
        kx = cx; ky = cy # initial position of the knight
        for k in range(maxIt):
            cb[ky][kx] = k + 1
            pq = [] # priority queue of available neighbors
            for i in range(8):
                nx = kx + dx[i]; ny = ky + dy[i]
                if nx >= 0 and nx < cbx and ny >= 0 and ny < cby:
                    if cb[ny][nx] == 0:
                        # count the available neighbors of the neighbor
                        ctr = 0
                        for j in range(8):
                            ex = nx + dx[j]; ey = ny + dy[j]
                            if ex >= 0 and ex < cbx and ey >= 0 and ey < cby:
                                if cb[ey][ex] == 0: ctr += 1
                        heappush(pq, (ctr, i))
            # move to the neighbor that has min number of available neighbors
            if len(pq) > 0:
                (p, m) = heappop(pq)
                kx += dx[m]; ky += dy[m]
            else: break
        # color the initial position according to final position
        # (its absolute/relative coordinates/distance/direction maybe used)
        c = 256 * (cbx * ky + kx) / (cbx * cby - 1)
        pixels[cx, cy] = (c % mr0 * mr1, c % mg0 * mg1, c % mb0 * mb1)
image = image.resize((imgx, imgy))
image.save("KnightsTourMap.png", "PNG")
