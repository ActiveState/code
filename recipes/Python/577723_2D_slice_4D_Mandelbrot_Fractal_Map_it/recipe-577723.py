## {{{ http://code.activestate.com/recipes/577715/ (r3)
# Random 2D Slice Of 4D Mandelbrot Fractal
# FB - 201105231
"""Random 2D Slice Of 4D Mandelbrot Fractal.
                          Modified by Symion 2011
    Now works with Visual Python v5.40.
    Produce 2D slice of 4D Mandelbrot Fractal and Map it in 3D!

Visual Python Controls:
    Click Left Mouse Key = Navigate
    Press Right Mouse Key = Spin
    Press Both Keys = Zoom
    q = Point size - 1
    w = Point size + 1
    e = Point shape + 1
    r = Scene Alignment
"""
vp_flag = 0

if vp_flag == 0:
    from visual import *
else:
    import random
    from math import *
    from PIL import Image
imgx = 512
imgy = 512
forge = 0
pcc = 0
pii = 0
psize = 3
pshape = 0

if vp_flag == 0:
    scene.width=imgx
    scene.height=imgy
    image = [points(size=psize, shape="square")]
    forward = vector(scene.forward)
    print "Number of Points objects: {0}".format(len(image))
else:
    image = Image.new("RGB", (imgx, imgy))
#
print __doc__
# drawing area (xa < xb & ya < yb)
xa = -2.0
xb = 2.0
ya = -2.0
yb = 2.0
maxIt = 32 # max number of iterations allowed
maxit = maxIt / 2.0
if True:
    # random rotation angles to convert 2d plane to 4d plane
    xy = random.random() * 2.0 * pi
    xz = random.random() * 2.0 * pi
    xw = random.random() * 2.0 * pi
    yz = random.random() * 2.0 * pi
    yw = random.random() * 2.0 * pi
    zw = random.random() * 2.0 * pi

else:
    # default rotation angles
    xy=1.3536589728
    xz=2.30808965705
    xw=3.50029464114
    yz=3.37449518258
    yw=4.23401560176
    zw=2.44695022478

sxy = sin(xy)
cxy = cos(xy)
sxz = sin(xz)
cxz = cos(xz)
sxw = sin(xw)
cxw = cos(xw)
syz = sin(yz)
cyz = cos(yz)
syw = sin(yw)
cyw = cos(yw)
szw = sin(zw)
czw = cos(zw)

origx = (xa + xb) / 2.0
origy = (ya + yb) / 2.0

for ky in range(imgy):
    b = ky * (yb - ya) / (imgy - 1)  + ya
    for kx in range(imgx):
        a = kx * (xb - xa) / (imgx - 1)  + xa
        x = a
        y = b
        z = 0 # c = 0
        w = 0 # d = 0
        # 4d rotation around center of the plane
        x = x - origx
        y = y - origy
        x0 = x * cxy - y * sxy
        y = x * sxy + y * cxy
        x = x0 # xy-plane rotation
        x0 = x * cxz - z * sxz
        z = x * sxz + z * cxz
        x = x0 # xz-plane rotation 
        x0 = x * cxw - z * sxw
        w = x * sxw + z * cxw
        x = x0 # xw-plane rotation
        y0 = y * cyz - z * syz
        z = y * syz + z * cyz
        y = y0 # yz-plane rotation
        y0 = y * cyw - w * syw
        w = y * syw + w * cyw
        y = y0 # yw-plane rotation
        z0 = z * czw - w * szw
        w = z * szw + w * czw
        z = z0 # zw-plane rotation
        x = x + origx
        y = y + origy
        if forge:
            for i in range(maxIt):
                # iteration using quaternion numbers
                x0 = x * x - y * y - z * z - w * w + a
                y = 2.0 * x * y + b
                z = 2.0 * x * z
                w = 2.0 * x * w
                x = x0
                s = x * x + y * y + z * z + w * w # 4d absolute value squared
                if s > 4.0:
                    break
        else:
            for i in range(maxIt):
                # iteration using hyper-complex numbers
                x0 = x * x - y * y - z * z - w * w + a
                y0 = 2.0 * x * y - 2.0 * z * w + b
                z0 = 2.0 * x * z - 2.0 * y * w
                w = 2.0 * x * w + 2.0 * z * y
                x = x0
                y = y0
                z = z0
                s = x * x + y * y + z * z + w * w # 4d absolute value squared
                if s > 4.0:
                    break
        pcc += i
        pii += 1
        if (i%maxIt) != 0:
            if vp_flag == 0:
                if len(image[-1].pos) > 9999:
                    image.append(points(size=psize, shape="square"))
                    print "Number of Points objects: {0}".format(len(image))
                c = (i/maxit, i/maxit, i/maxit)
                image[-1].append((kx-256, ky-256, i/maxit))
                image[-1].color[-1] = c
            else:
                image.putpixel((kx, ky), (i % 4 * 64, i % 8 * 32, i % 16 * 16))
if vp_flag == 0:
    scene.autoscale=False
    scene.range=mag(scene.mouse.camera)/sqrt(3)
    scene.visible = True
else:
    image.save("4D_Mandelbrot_Fractal.png", "PNG")
print "Finished!"
print "{0} / {1} = {2}".format(pcc, pii, pcc / pii)
mess = "Base Set:\nxy={0}, xz={1}, xw={2}, yz={3}, yw={4}, zw={5}"
print mess.format(xy, xz, xw, yz, yw, zw)
if vp_flag == 0:
    while 1:
        if scene.mouse.events>0:
            mk = scene.mouse.getevent()
            if mk.release == "left":
                scene.center = mk.pos
        elif scene.kb.keys:
            km = scene.kb.getkey()
            if km in ["x", "X"]:
                break
            elif km in ["w"]:
                psize = psize%50
                psize += 1
                for a in image:
                    a.size = psize
            elif km in ["q"]:
                psize -= 1
                if psize<1:
                    psize = 50
                for a in image:
                    a.size = psize
            elif km in ["e"]:
                pshape = (pshape+1)%2
                for a in image:
                    a.shape = ["square","round"][pshape]
            elif km in ["r"]:
                scene.forward = forward
