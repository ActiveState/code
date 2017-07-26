# Dynamical Billiards Simulation Map (Fractal?)
# FB - 201011077
# More info:
# http://en.wikipedia.org/wiki/Dynamical_billiards
# http://www.scholarpedia.org/article/Dynamical_billiards
import math
import random
import time
from PIL import Image, ImageDraw
imgx = 300
imgy = 200
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)

coloring = random.randint(0, 7) # choose a coloring method
print 'Using the coloring method: ' + str(coloring)

maxSteps = 200 # of steps of ball motion (in constant speed)

n = random.randint(1, 7) # of circular obstacles
crMax = int(min(imgx - 1, imgy - 1) / 4) # max circle radius
crMin = 10 # min circle radius

# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = random.randint(crMin, crMax) # circle radius
        cx = random.randint(cr, imgx - 1 - cr) # circle center x
        cy = random.randint(cr, imgy - 1 - cr) # circle center y
        flag = True
        if i > 0:
            for j in range(i):
                if math.hypot(cx - cxList[j], cy - cyList[j]) < cr + crList[j]:
                    flag = False
                    break
        if flag == True:
            break
    draw.ellipse((cx - cr, cy - cr, cx + cr, cy + cr))
    cxList.append(cx)
    cyList.append(cy)
    crList.append(cr)
    
# initial direction of the ball
a = 2.0 * math.pi * random.random()

t0 = time.time()

for y0 in range(imgy):
    for x0 in range(imgx):
        x = float(x0)
        y = float(y0)
        s = math.sin(a)
        c = math.cos(a)

        # print '%completed' every 10 seconds
        t = time.time()
        if t - t0 >= 10:
            print '%' + str(int(100 * (imgx * y0 + x0) / (imgx * imgy)))
            t0 = t

        # initial location of the ball must be outside of the circle(s)
        flag = True
        for i in range(n):
            if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
                flag = False
                break

        if flag:
            for i in range(maxSteps):
                xnew = x + c
                ynew = y + s

                # reflection from the walls
                if xnew < 0 or xnew > imgx - 1:
                    c = -c
                    xnew = x
                if ynew < 0 or ynew > imgy - 1:
                    s = -s
                    ynew = y

                # reflection from the circle(s)
                for i in range(n):
                    if math.hypot(xnew - cxList[i], ynew - cyList[i]) <= crList[i]:
                        # angle of the circle point
                        ca = math.atan2(ynew - cyList[i], xnew - cxList[i])
                        # reversed collision angle of the ball
                        rca = math.atan2(-s, -c)
                        # reflection angle of the ball
                        rab = rca + (ca - rca) * 2
                        s = math.sin(rab)
                        c = math.cos(rab)
                        xnew = x
                        ynew = y

                x = xnew
                y = ynew

            # Color the starting point according to the final point!
            # The color can be decided in many different ways.
            # Only 8 methods implemented here.
            if coloring == 0:
                # absolute distance method
                d = math.hypot(x, y) / math.hypot(imgx - 1, imgy - 1)
            elif coloring == 1:
                # relative distance method
                d = math.hypot(x - x0, y - y0) / math.hypot(imgx - 1, imgy - 1)
            elif coloring == 2:
                # x+y method
                d = (x + y) / (imgx + imgy - 2)
            elif coloring == 3:
                # x*y method
                d = x * y / ((imgx - 1) * (imgy - 1))
            elif coloring == 4:
                # x-coordinate method
                d = x / (imgx - 1)
            elif coloring == 5:
                # y-coordinate method
                d = y / (imgy - 1)
            elif coloring == 6:
                # absolute angle method by taking the image center as origin
                ang = math.atan2(y - (imgy - 1) / 2, x - (imgx - 1) / 2)
            elif coloring == 7:
                # relative angle method by taking the starting point as origin
                ang = math.atan2(y - y0, x - x0)
            if coloring >= 6:
                # convert the angle from -pi..pi to 0..2pi
                if ang < 0: ang = 2 * math.pi - math.fabs(ang)
                d = ang / 2 * math.pi # convert the angle to 0..1

            k = int(d * 255)
            rd = k % 8 * 32
            gr = k % 16 * 16
            bl = k % 32 * 16
            image.putpixel((x0, y0), (rd, gr, bl))

print 'Calculations completed.'    
image.save('Dynamical_Billiards_Map_color' + str(coloring) + '.png', 'PNG')
