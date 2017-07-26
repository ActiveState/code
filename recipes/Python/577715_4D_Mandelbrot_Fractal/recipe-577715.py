# Random 2D Slice Of 4D Mandelbrot Fractal
# FB - 20120707
import math
import random
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
# drawing area (xa < xb & ya < yb)
xa = -2.0
xb = 2.0
ya = -2.0
yb = 2.0
maxIt = 256 # max number of iterations allowed
# random rotation angles to convert 2d plane to 4d plane
xy = random.random() * 2.0 * math.pi
xz = random.random() * 2.0 * math.pi
xw = random.random() * 2.0 * math.pi
yz = random.random() * 2.0 * math.pi
yw = random.random() * 2.0 * math.pi
zw = random.random() * 2.0 * math.pi
sxy = math.sin(xy)
cxy = math.cos(xy)
sxz = math.sin(xz)
cxz = math.cos(xz)
sxw = math.sin(xw)
cxw = math.cos(xw)
syz = math.sin(yz)
cyz = math.cos(yz)
syw = math.sin(yw)
cyw = math.cos(yw)
szw = math.sin(zw)
czw = math.cos(zw)
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
        x0=x*cxy-y*sxy;y=x*sxy+y*cxy;x=x0 # xy-plane rotation
        x0=x*cxz-z*sxz;z=x*sxz+z*cxz;x=x0 # xz-plane rotation 
        x0=x*cxw-z*sxw;w=x*sxw+z*cxw;x=x0 # xw-plane rotation
        y0=y*cyz-z*syz;z=y*syz+z*cyz;y=y0 # yz-plane rotation
        y0=y*cyw-w*syw;w=y*syw+w*cyw;y=y0 # yw-plane rotation
        z0=z*czw-w*szw;w=z*szw+w*czw;z=z0 # zw-plane rotation
        x = x + origx
        y = y + origy
        cx = x
        cy = y
        cz = z
        cw = w
        for i in range(maxIt):
            # iteration using quaternion numbers
            x0 = x * x - y * y - z * z - w * w + cx
            y = 2.0 * x * y + cy
            z = 2.0 * x * z + cz
            w = 2.0 * x * w + cw
            x = x0
            # iteration using hyper-complex numbers
            # x0 = x * x - y * y - z * z - w * w + cx
            # y0 = 2.0 * x * y - 2.0 * z * w + cy
            # z0 = 2.0 * x * z - 2.0 * y * w + cz
            # w = 2.0 * x * w + 2.0 * z * y + cw
            # x = x0
            # y = y0
            # z = z0
            if x * x + y * y + z * z + w * w > 4.0: break
        pixels[kx, ky] = (i % 4 * 64, i % 8 * 32, i % 16 * 16)
image.save("4D_Mandelbrot_Fractal.png", "PNG")
