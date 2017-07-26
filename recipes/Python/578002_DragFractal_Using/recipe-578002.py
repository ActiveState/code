# Dragon Fractal using Iteration method
# FB - 20120106
from collections import deque
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
maxIt = 16 # max iterations allowed

xa = -1.0 / 3
xb = 7.0 / 6
ya = -1.0 / 3
yb = 2.0 / 3

for ky in range(imgy):
    for kx in range(imgx):
        x = float(kx) / (imgx - 1) * (xb - xa) + xa
        y = float(ky) / (imgy - 1) * (yb - ya) + ya
        queue = deque([])
        queue.append((x, y, 0))
        while len(queue) > 0:
            (x, y, i) = queue.popleft()
            # try 1. transformation
            xnew = x + y
            ynew = y - x
            if xnew >= xa and xnew <= xb and ynew >= ya and ynew <= yb:
                if i + 1 == maxIt: break
                queue.append((xnew, ynew, i + 1))
            # try 2. transformation                
            xnew = 1.0 - x + y
            ynew = 1.0 - x - y
            if xnew >= xa and xnew <= xb and ynew >= ya and ynew <= yb:
                if i + 1 == maxIt: break
                queue.append((xnew, ynew, i + 1))

        image.putpixel((kx, ky), (i % 8 * 32, 255 - i % 16 * 16, i % 16 * 16))

image.save("DragonFractal_Iter.png", "PNG")
