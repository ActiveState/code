# Knight's Tour using Warnsdorff's Rule
# http://en.wikipedia.org/wiki/Knight's_tour
# FB - 20121216
from heapq import heappush, heappop # for priority queue
import random
import string
cbx = 8; cby = 8 # width and height of the chessboard
cb = [[0 for x in range(cbx)] for y in range(cby)] # chessboard
# directions the Knight can move on the chessboard
dx = [-2, -1, 1, 2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]
# start the Knight from a random position
kx = random.randint(0, cbx - 1)
ky = random.randint(0, cby - 1)

for k in range(cbx * cby):
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

# print cb
for cy in range(cby):
    for cx in range(cbx):
        print string.rjust(str(cb[cy][cx]), 2),
    print
