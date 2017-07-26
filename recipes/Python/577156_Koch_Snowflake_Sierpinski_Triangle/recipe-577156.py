# Koch Snowflake and Sierpinski Triangle combination fractal using recursion
# FB - 201003265
from PIL import Image, ImageDraw
import math

imgx = 512
imgy = 512
image = Image.new("L", (imgx, imgy))
draw = ImageDraw.Draw(image)

def tf (x0, y0, x1, y1, x2, y2):
    global draw
    a = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    b = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    c = math.sqrt((x0 - x2) ** 2 + (y0 - y2) ** 2)
    if (a < 2) or (b < 2) or (c < 2): return
    x3 = (x0 + x1) / 2
    y3 = (y0 + y1) / 2
    x4 = (x1 + x2) / 2
    y4 = (y1 + y2) / 2
    x5 = (x2 + x0) / 2
    y5 = (y2 + y0) / 2

    draw.line ([(int(x3), int(y3)),(int(x4), int(y4))], 255)
    draw.line ([(int(x4), int(y4)),(int(x5), int(y5))], 255)
    draw.line ([(int(x5), int(y5)),(int(x3), int(y3))], 255)
    tf(x0, y0, x3, y3, x5, y5)
    tf(x3, y3, x1, y1, x4, y4)
    tf(x5, y5, x4, y4, x2, y2)


def sf (ax, ay, bx, by):
    f = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
    if f < 1: return
    f3 = f / 3
    cs = (bx - ax) / f
    sn = (by - ay) / f
    cx = ax + cs * f3
    cy = ay + sn * f3
    h = f3 * math.sqrt(3) / 2
    dx = (ax + bx) / 2 + sn * h
    dy = (ay + by) / 2 - cs * h
    ex = bx - cs * f3
    ey = by - sn * f3
    tf(cx, cy, dx, dy, ex, ey)
    sf(ax, ay, cx, cy)
    sf(cx, cy, dx, dy)
    sf(dx, dy, ex, ey)
    sf(ex, ey, bx, by)


# main
mx2 = imgx / 2
my2 = imgy / 2
r = my2
a = 2 * math.pi / 3
for k in range(3):
    x0 = mx2 + r * math.cos(a * k)
    y0 = my2 + r * math.sin(a * k)
    x1 = mx2 + r * math.cos(a * (k + 1))
    y1 = my2 + r * math.sin(a * (k + 1))
    sf(x0, y0, x1, y1)

x2 = mx2 + r * math.cos(a)
y2 = my2 + r * math.sin(a)
tf(x0, y0, x1, y1, x2, y2)

image.save("sfplustf.png", "PNG")
