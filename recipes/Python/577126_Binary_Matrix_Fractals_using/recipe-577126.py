# Binary Matrix Fractals using iteration method
# FB - 201003184
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))

### Sierpinski triangle
##bm = [[1,0], \
##      [1,1]]

# Sierpinski square
bm = [[1,1,1], \
      [1,0,1], \
      [1,1,1]]

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
maxIt = 16 # max iterations allowed

for ky in range(imgy):
    for kx in range(imgx):
        x = float(kx) / imgx * nx
        y = float(ky) / imgy * ny
        for i in range(maxIt):
            ix = int(x)
            iy = int(y)
            if bm[int(y)][int(x)] == 0:
                break
            x = (x - ix) * nx
            y = (y - iy) * ny

        r = i % 4 * 64
        g = i % 8 * 32
        b = i % 16 * 16
        image.putpixel((kx, ky), b * 65536 + g * 256 + r)

image.save("binMatItFr.png", "PNG")
