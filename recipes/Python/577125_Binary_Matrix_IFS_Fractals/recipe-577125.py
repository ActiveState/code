# Binary Matrix IFS Fractals
# FB - 201003173
from PIL import Image
import random
# image size
imgx = 512
imgy = 512
image = Image.new("L", (imgx, imgy))

### Sierpinski triangle
##bm = [[1,0], \
##      [1,1]]

### Sierpinski square
##bm = [[1,1,1], \
##      [1,0,1], \
##      [1,1,1]]

### Snowflake
##bm = [[1,1,0], \
##      [1,0,1], \
##      [0,1,1]]

# Hexaflake
bm = [[1,1,0], \
      [1,1,1], \
      [0,1,1]]

### A spiral fractal
##bm = [[0,0,1,1,0], \
##      [1,0,1,0,0], \
##      [1,1,1,1,1], \
##      [0,0,1,0,1], \
##      [0,1,1,0,0]]

### Another spiral fractal
##bm = [[1,0,0,1,1], \
##      [1,0,1,0,0], \
##      [0,1,1,1,0], \
##      [0,0,1,0,1], \
##      [1,1,0,0,1]]

# size of the matrix
n = len(bm)
m = len(bm[0])

x = 0.0
y = 0.0

for i in range(imgx * imgy):
    j = random.randint(0, m - 1)
    k = random.randint(0, n - 1)
    if bm[k][j] > 0:
        x = (x + j) / m
        y = (y + k) / n
        image.putpixel((int(x * (imgx - 1)), int(y * (imgy - 1))), 255)

image.save("binMatIFSfr.png", "PNG")
