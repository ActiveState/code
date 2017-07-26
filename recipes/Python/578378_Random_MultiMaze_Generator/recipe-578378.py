# Multi-Maze Generator using Depth-first Search
# Multi-Maze: Maze w/ multiple paths to solve
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# FB - 20121214
import random
from PIL import Image
imgx = 600; imgy = 600
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
m = random.randint(1, 10) # of maze paths
mx = 60; my = 60 # width and height of the maze
maze = [[0 for x in range(mx)] for y in range(my)]
dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
stack = [] # array of stacks
color = [(0, 0, 0)] # RGB colors maze paths
for i in range(m):
    while True:
        kx = random.randint(0, mx - 1); ky = random.randint(0, my - 1)
        if maze[ky][kx] == 0: break
    stack.append([(kx, ky)])
    maze[ky][kx] = i + 1
    color.append((random.randint(0, 255),
                  random.randint(0, 255),
                  random.randint(0, 255)))

cont = True # continue
while cont:
    cont = False
    for p in range(m):
        if len(stack[p]) > 0:
            cont = True # continue as long as there is a non-empty stack
            (cx, cy) = stack[p][-1]
            # find a new cell to add
            nlst = [] # list of available neighbors
            for i in range(4):
                nx = cx + dx[i]; ny = cy + dy[i]
                if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                    if maze[ny][nx] == 0:
                        # of occupied neighbors must be 1
                        ctr = 0
                        for j in range(4):
                            ex = nx + dx[j]; ey = ny + dy[j]
                            if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                                if maze[ey][ex] == p + 1: ctr += 1
                        if ctr == 1: nlst.append(i)
            # if 1 or more neighbors available then randomly select one and add
            if len(nlst) > 0:
                ir = nlst[random.randint(0, len(nlst) - 1)]
                cx += dx[ir]; cy += dy[ir]
                maze[cy][cx] = p + 1
                stack[p].append((cx, cy))
            else: stack[p].pop()

for ky in range(imgy):
    for kx in range(imgx):
        pixels[kx, ky] = color[maze[my * ky / imgy][mx * kx / imgx]]
image.save(str(m) + "Maze_" + str(mx) + "x" + str(my) + ".png", "PNG")
