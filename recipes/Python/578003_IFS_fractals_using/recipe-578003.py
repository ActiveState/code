# IFS fractals using iteration method
# FB - 20120107
import random
from collections import deque
from PIL import Image
# image size
imgx = 512
imgy = 512 # will be auto-re-adjusted according to aspect ratio of the fractal

# Fractint IFS Fern
mat=[[0.0,0.0,0.0,0.16,0.0,0.0,0.01],
     [0.85,0.04,-0.04,0.85,0.0,1.6,0.85],
     [0.2,-0.26,0.23,0.22,0.0,1.6,0.07],
     [-0.15,0.28,0.26,0.24,0.0,0.44,0.07]]

### Fractint IFS Dragon
##mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607, 0.787473],
##       [0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795, 0.212527]]

### C fractal
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
##       [0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5]]

### Dragon
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
##       [-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5]]

m = len(mat) # number of IFS transformations
# find xmin, xmax, ymin, ymax of the fractal using IFS algorithm
x = mat[0][4]
y = mat[0][5] 
xa = x
xb = x
ya = y
yb = y
for k in range(imgx * imgy):
    p = random.random()
    psum = 0.0
    for i in range(m):
        psum += mat[i][6]
        if p <= psum:
            break
    x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4] 
    y  = x * mat[i][2] + y * mat[i][3] + mat[i][5] 
    x = x0 
    if x < xa:
        xa = x
    if x > xb:
        xb = x
    if y < ya:
        ya = y
    if y > yb:
        yb = y

imgy = int(imgy * (yb - ya) / (xb - xa)) # auto-re-adjust the aspect ratio 
image = Image.new("RGB", (imgx, imgy))

# drawing using IFS algorithm
##x=0.0
##y=0.0 
##for k in range(imgx * imgy):
##    p=random.random()
##    psum = 0.0
##    for i in range(m):
##        psum += mat[i][6]
##        if p <= psum:
##            break
##    x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4] 
##    y  = x * mat[i][2] + y * mat[i][3] + mat[i][5] 
##    x = x0 
##    jx = int((x - xa) / (xb - xa) * (imgx - 1)) 
##    jy = (imgy - 1) - int((y - ya) / (yb - ya) * (imgy - 1))
##    image.putpixel((jx, jy), (255, 255, 255)) 

# drawing using iteration method
maxIt = 16 # max number of iterations allowed
for ky in range(imgy):
    for kx in range(imgx):
        x = float(kx) / (imgx - 1) * (xb - xa) + xa
        y = float(ky) / (imgy - 1) * (yb - ya) + ya
        queue = deque([])
        queue.append((x, y, 0))
        while len(queue) > 0: # iterate points until none left
            (x, y, i) = queue.popleft()
            # apply all (inverse) IFS transformations
            for j in range(m):
                d = mat[j][0] * mat[j][3] - mat[j][2] * mat[j][1]
                if d != 0.0:
                    xnew = ((x - mat[j][4]) * mat[j][3] - (y - mat[j][5]) * mat[j][1]) / d
                    ynew = ((y - mat[j][5]) * mat[j][0] - (x - mat[j][4]) * mat[j][2]) / d
                    if xnew >= xa and xnew <= xb and ynew >= ya and ynew <= yb:
                        if i + 1 == maxIt: break
                        queue.append((xnew, ynew, i + 1))

        image.putpixel((kx, ky), (i % 8 * 32, i % 16 * 16, i % 32 * 8))
image.save("IFSfractalUsingIterationMethod.png", "PNG")
