# 3D surface fitting to N random points
# using inverse distance weighted averages.
# FB - 201003162
from PIL import Image
import random
import math

# image size
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))

# random color palette coefficients
kr = random.randint(1, 7)
kg = random.randint(1, 7)
kb = random.randint(1, 7)
ir = 2**kr
ig = 2**kg
ib = 2**kb
jr = 2**(8-kr)
jg = 2**(8-kg)
jb = 2**(8-kb)

# select n random points
n=random.randint(5, 50)
arx=[]
ary=[]
arz=[]

for i in range(n):
    arx.append(random.randint(0, imgx-1))
    ary.append(random.randint(0, imgy-1))
    arz.append(random.randint(0, 255))

for y in range(imgy):
    for x in range(imgx):
        flag=False
        sumv=0.0
        sumw=0.0
        for i in range(n):
            dx=x-arx[i]
            dy=y-ary[i]
            if(dx==0 and dy==0):
                flag=True
                z=arz[i]
                break
            else:
                # wgh=1.0/math.pow(math.sqrt(dx*dx+dy*dy),1.0) # linear
                wgh=1.0/math.pow(math.sqrt(dx*dx+dy*dy),2.0) # quadratic
                # wgh=1.0/math.pow(math.sqrt(dx*dx+dy*dy),3.0) # cubic
                sumw+=wgh
                sumv+=(wgh*arz[i])
            
        if flag==False:
            z=int(sumv/sumw)

        # z to RGB
        r = z % ir * jr
        g = z % ig * jg
        b = z % ib * jb
        image.putpixel((x, y), b * 65536 + g * 256 + r)

image.save("rndSurface.png", "PNG")
