# Sierpinski Square combination fractal using recursion.
# (Combination of Sierpinski Square and 2 other square fractals!)
# FB - 201008102
from PIL import Image, ImageDraw
imgx = 2187
imgy = 2187
image = Image.new("L", (imgx, imgy))
draw = ImageDraw.Draw(image)

def ssf (x, y, a): # Sierpinski square fractal
    global draw
    # draw rectangle
    draw.line ([(int(x), int(y)),(int(x + a), int(y))], 255)
    draw.line ([(int(x), int(y)),(int(x), int(y + a))], 255)
    draw.line ([(int(x), int(y + a)),(int(x + a), int(y + a))], 255)
    draw.line ([(int(x + a), int(y)),(int(x + a), int(y + a))], 255)
    
    a = float(a) / 3
    if a < 1: return
    for j in range(3):
        for k in range(3):
            if not( k == 1 and j == 1):
                ssf(x + a * k, y + a * j, a)

def s0 (x, y, a): # top-left
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    s0(x - b, y - b, b) # top-left
    s1(x - b, y + a, b) # bottom-left
    s2(x + a, y - b, b) # top-right

def s1 (x, y, a): # bottom-left
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    s0(x - b, y - b, b) # top-left
    s1(x - b, y + a, b) # bottom-left
    s3(x + a, y + a, b) # bottom-right

def s2 (x, y, a): # top-right
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    s0(x - b, y - b, b) # top-left
    s2(x + a, y - b, b) # top-right
    s3(x + a, y + a, b) # bottom-right

def s3 (x, y, a): # bottom-right
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    s1(x - b, y + a, b) # bottom-left
    s2(x + a, y - b, b) # top-right
    s3(x + a, y + a, b) # bottom-right

def t0 (x, y, a): # top
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    t0(x + b, y - b, b) # top
    t2(x - b, y + b, b) # left
    t3(x + a, y + b, b) # right

def t1 (x, y, a): # bottom
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    t1(x + b, y + a, b) # bottom
    t2(x - b, y + b, b) # left
    t3(x + a, y + b, b) # right

def t2 (x, y, a): # left
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    t0(x + b, y - b, b) # top
    t1(x + b, y + a, b) # bottom
    t2(x - b, y + b, b) # left

def t3 (x, y, a): # right
    ssf(x, y, a)
    b = float(a) / 3
    if b < 1: return
    t0(x + b, y - b, b) # top
    t1(x + b, y + a, b) # bottom
    t3(x + a, y + b, b) # right
 
# MAIN
mx2 = imgx / 2
my2 = imgy / 2
my4 = my2 / 2

# center Sierpinski square
ssf(mx2 - my4, my2 - my4, my2)

# 4 corners
s0(mx2 - my4 - my2 / 3, my2 - my4 - my2 / 3, my2 / 3) # top-left
s1(mx2 - my4 - my2 / 3, my2 - my4 + my2    , my2 / 3) # bottom-left
s2(mx2 - my4 + my2    , my2 - my4 - my2 / 3, my2 / 3) # top-right
s3(mx2 - my4 + my2    , my2 - my4 + my2    , my2 / 3) # bottom-right

# 4 sides
t0(mx2 - my4 + my2 / 3, my2 - my4 - my2 / 3, my2 / 3) # top
t1(mx2 - my4 + my2 / 3, my2 - my4 + my2    , my2 / 3) # bottom
t2(mx2 - my4 - my2 / 3, my2 - my4 + my2 / 3, my2 / 3) # left
t3(mx2 - my4 + my2    , my2 - my4 + my2 / 3, my2 / 3) # right

image.save("SqPlusSq3.png", "PNG")
