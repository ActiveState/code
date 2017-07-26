# 2D Fluid Simulation using FHP LGCA (Lattice Gas Cellular Automata)
# Simulates fluid flow in a circular channel.
# Particles go out from right side and enter back from left.
# Reference:
# Lattice Gas Cellular Automata and Lattice Boltzmann Models by Wolf-Gladrow
# FB - 20140818
import math
import random
from PIL import Image
imgx = 512; imgy = 512 # image size
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
# simulation parameters:
tilesX = 32
tilesY = 32
n = 8 # coarse graining tile size is n by n
timeSteps = 300

nodesX = tilesX * n
nodesY = tilesY * n
nodes = [[[0 for x in range(nodesX)] for y in range(nodesY)] for z in range(6)]
obstacle = [[0 for x in range(nodesX)] for y in range(nodesY)]

# insert a square obstacle in the middle
for y in range(nodesY / 4):
    for x in range(nodesX / 4):
        obstacle[y + nodesY / 2 - nodesY / 8][x + nodesX / 2 - nodesX / 8] = 1

# fill-up with fluid flowing towards right
for y in range(1, nodesY - 1): # do not include top/bottom walls
    for x in range(nodesX):
        if obstacle[y][x] != 1:               
            nodes[0][y][x] = 1

for t in range(timeSteps): # run the simulation

    # HANDLE COLLISIONS
    
    # collisions at non-boundary nodes
    for y in range(1, nodesY - 1): # do not include top/bottom walls
        for x in range(nodesX):
            if obstacle[y][x] != 1:
                cell = [nodes[z][y][x] for z in range(6)]
                numParticles = sum(cell)

                # only 2 or 3 symmetric particle collisions implemented here
                if numParticles == 3:
                    if cell[0] == cell[2] and cell[2] == cell[4]:
                        # invert the cell contents
                        for z in range(6):
                            nodes[z][y][x] = 1 - cell[z]
                elif numParticles == 2:
                    # find the cell of one of the particles
                    p = cell.index(1)
                    # its diametric opposite must occupied as well
                    if p > 2:
                        pass
                    elif cell[p + 3] == 0:
                        pass
                    else:
                        # randomly rotate the particle pair clockwise or
                        # counterclockwise
                        if random.randint(0, 1) == 0: # counterclockwise
                            nodes[0][y][x] = cell[5]
                            nodes[1][y][x] = cell[0]
                            nodes[2][y][x] = cell[1]
                            nodes[3][y][x] = cell[2]
                            nodes[4][y][x] = cell[3]
                            nodes[5][y][x] = cell[4]
                        else: # clockwise
                            nodes[0][y][x] = cell[1]
                            nodes[1][y][x] = cell[2]
                            nodes[2][y][x] = cell[3]
                            nodes[3][y][x] = cell[4]
                            nodes[4][y][x] = cell[5]
                            nodes[5][y][x] = cell[0]

    # collisions along top/bottom walls (no-slip)
    for x in range(nodesX):
        cell = [nodes[z][0][x] for z in range(6)]
        nodes[0][0][x] = cell[3]
        nodes[1][0][x] = cell[4]
        nodes[2][0][x] = cell[5]
        nodes[3][0][x] = cell[0]
        nodes[4][0][x] = cell[1]
        nodes[5][0][x] = cell[2]
        cell = [nodes[z][nodesY - 1][x] for z in range(6)]
        nodes[0][nodesY - 1][x] = cell[3]
        nodes[1][nodesY - 1][x] = cell[4]
        nodes[2][nodesY - 1][x] = cell[5]
        nodes[3][nodesY - 1][x] = cell[0]
        nodes[4][nodesY - 1][x] = cell[1]
        nodes[5][nodesY - 1][x] = cell[2]
            
    # collisions at obstacle points (no-slip)
    for y in range(nodesY):
        for x in range(nodesX):
            if obstacle[y][x] == 1:
                cell = [nodes[z][y][x] for z in range(6)]
                nodes[0][y][x] = cell[3]
                nodes[1][y][x] = cell[4]
                nodes[2][y][x] = cell[5]
                nodes[3][y][x] = cell[0]
                nodes[4][y][x] = cell[1]
                nodes[5][y][x] = cell[2]

    # HANDLE MOVEMENTS

    nodesNew = [[[0 for x in range(nodesX)] for y in range(nodesY)] for z in range(6)]

    for y in range(nodesY):
        for x in range(nodesX):
            cell = [nodes[z][y][x] for z in range(6)]

            # propagation in the 0-direction
            neighbor_y = y
            if x == nodesX - 1:
                neighbor_x = 0 
            else:
                neighbor_x = x + 1
            nodesNew[0][neighbor_y][neighbor_x] = cell[0]

            # propagation in the 1-direction
            if y != nodesY - 1:
                neighbor_y = y + 1
                if y % 2 == 1:
                    if x == nodesX - 1:
                        neighbor_x = 1
                    else:
                        neighbor_x = x + 1
                else:
                    neighbor_x = x
                nodesNew[1][neighbor_y][neighbor_x] = cell[1]

            # propagation in the 2-direction
            if y != nodesY - 1:
                neighbor_y = y + 1
                if y % 2 == 0:
                    if x == 0:
                        neighbor_x = nodesX - 1
                    else:
                        neighbor_x = x - 1
                else:
                    neighbor_x = x
                nodesNew[2][neighbor_y][neighbor_x] = cell[2]

            # propagation in the 3-direction
            neighbor_y = y
            if x == 0:
                neighbor_x = nodesX - 1
            else:
                neighbor_x = x - 1
            nodesNew[3][neighbor_y][neighbor_x] = cell[3]

            # propagation in the 4-direction
            if y != 0:
                neighbor_y = y - 1
                if y % 2 == 0:
                    if x == 0:
                        neighbor_x = nodesX - 1
                    else:
                        neighbor_x = x - 1
                else:
                    neighbor_x = x
                nodesNew[4][neighbor_y][neighbor_x] = cell[4]

            # propagation in the 5-direction
            if y != 0:
                neighbor_y = y - 1
                if y % 2 == 1:
                    if x == nodesX - 1:
                        neighbor_x = 0
                    else:
                        neighbor_x = x + 1
                else:
                    neighbor_x = x
                nodesNew[5][neighbor_y][neighbor_x] = cell[5]
    
    nodes = nodesNew
    
    print '%' + str(100 * t / timeSteps) # show progress

# Create an image from the final state
# Calculate average velocity vectors for tiles
aveVelocityVectorMag = [[0.0 for x in range(tilesX)] for y in range(tilesY)]
aveVelocityVectorAng = [[0.0 for x in range(tilesX)] for y in range(tilesY)]
pi2 = math.pi * 2.0
dx = [math.cos(i * pi2 / 6.0) for i in range(6)]
dy = [math.sin(i * pi2 / 6.0) for i in range(6)]    
for ty in range(tilesY):
    for tx in range(tilesX):
        vx = 0.0
        vy = 0.0
        for cy in range(n):
            for cx in range(n):
                for z in range(6):
                    if nodes[z][ty * n + cy][tx * n + cx] == 1 \
                       and obstacle[ty * n + cy][tx * n + cx] == 0:
                        vx += dx[z]
                        vy += dy[z]
        aveVelocityVectorMag[ty][tx] = math.hypot(vx, vy) / n ** 2.0
        aveVelocityVectorAng[ty][tx] = (math.atan2(vy, vx) + pi2) % pi2

for ky in range(imgy):
    iy = nodesY * ky / imgy
    jy = tilesY * ky / imgy
    for kx in range(imgx):
        ix = nodesX * kx / imgx
        jx = tilesX * kx / imgx
        if obstacle[iy][ix] == 1: # paint the obstacle(s)
            red = 0
            grn = 0
            blu = 255
        else: # use vector magnitude and angle for coloring
            aveVelVecMag = aveVelocityVectorMag[jy][jx]
            aveVelVecAng = aveVelocityVectorAng[jy][jx]
            red = int(aveVelVecMag * 255)
            grn = int(aveVelVecAng / pi2 * 255)
            blu = 0
        pixels[kx, ky] = (red, grn, blu)
image.save("FHP_LGCA_2DFluidSim.png", "PNG")
