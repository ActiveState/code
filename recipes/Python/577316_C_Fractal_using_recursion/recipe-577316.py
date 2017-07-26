# C fractal using recursion
# FB - 201007187
from PIL import Image, ImageDraw
import math

imgx = 512
imgy = 512
image = Image.new("L", (imgx, imgy))
draw = ImageDraw.Draw(image)

def c (xa, ya, xb, yb):
    global draw
    xd = xb - xa
    yd = yb - ya
    d = math.hypot(xd, yd)
    if d < 2: return
    x = xa + xd * 0.5 - yd * 0.5
    y = ya + xd * 0.5 + yd * 0.5
    draw.line ([(int(xa), int(ya)),(int(x), int(y))], 255)
    draw.line ([(int(x), int(y)),(int(xb), int(yb))], 255)
    c(xa, ya, x, y)
    c(x, y, xb, yb)

# main
mx = imgx -1
my = imgy - 1
c(mx / 4, my / 4, mx - mx / 4, my / 4)

image.save("c.png", "PNG")
