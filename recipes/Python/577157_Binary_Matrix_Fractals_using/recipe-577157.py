# Binary matrix fractals using recursion
# FB - 201003265
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("L", (imgx, imgy))

### Sierpinski triangle
##bm = [[1,0], \
##      [1,1]]

# Sierpinski square
bm = [[1,1,1], \
      [1,0,1], \
      [1,1,1]]

### Vicsek fractal
##bm = [[1,0,1], \
##      [0,1,0], \
##      [1,0,1]]

### Snowflake
##bm = [[1,1,0], \
##      [1,0,1], \
##      [0,1,1]]

### Hexaflake
##bm = [[1,1,0], \
##      [1,1,1], \
##      [0,1,1]]

### A spiral fractal
##bm = [[0,0,1,1,0], \
##      [1,0,1,0,0], \
##      [1,1,1,1,1], \
##      [0,0,1,0,1], \
##      [0,1,1,0,0]]

nx = len(bm[0])
ny = len(bm)

def bmf(x0, y0, x1, y1):
    global image, bm, nx, ny
    xd = x1-x0
    yd = y1-y0
    if xd < 2 and yd < 2:
        image.putpixel((int(x0), int(y0)), 255)
        return
    for i in range(ny):
        for k in range(nx):
            if bm[i][k] > 0:
                bmf(x0+xd*k/nx, y0+yd*i/ny, x0+xd*(k+1)/nx, y0+yd*(i+1)/ny)

# main
bmf(0, 0, imgx-1, imgy-1)
image.save("binMatFrR.png", "PNG")
