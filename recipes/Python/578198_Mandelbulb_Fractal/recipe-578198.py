# Random 2D Cross-section Of (3D) Mandelbulb Fractal
# http://en.wikipedia.org/wiki/Mandelbulb
# FB - 20120707
import math
import random
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
n = 8
# drawing area (xa < xb & ya < yb)
xa = -1.5
xb = 1.5
ya = -1.5
yb = 1.5
maxIt = 256 # max number of iterations allowed
pi2 = math.pi * 2.0
# random rotation angles to convert 2d plane to 3d plane
xy = random.random() * pi2
xz = random.random() * pi2
yz = random.random() * pi2
sxy = math.sin(xy) ; cxy = math.cos(xy)
sxz = math.sin(xz) ; cxz = math.cos(xz)
syz = math.sin(yz) ; cyz = math.cos(yz)

origx = (xa + xb) / 2.0 ; origy = (ya + yb) / 2.0
for ky in range(imgy):
    b = ky * (yb - ya) / (imgy - 1)  + ya
    for kx in range(imgx):
        a = kx * (xb - xa) / (imgx - 1)  + xa
        x = a ; y = b ; z = 0.0
        # 3d rotation around center of the plane
        x = x - origx ; y = y - origy
        x0=x*cxy-y*sxy;y=x*sxy+y*cxy;x=x0 # xy-plane rotation
        x0=x*cxz-z*sxz;z=x*sxz+z*cxz;x=x0 # xz-plane rotation 
        y0=y*cyz-z*syz;z=y*syz+z*cyz;y=y0 # yz-plane rotation
        x = x + origx ; y = y + origy

        cx = x ; cy = y ; cz = z
        for i in range(maxIt):
            r = math.sqrt(x * x + y * y + z * z)
            t = math.atan2(math.hypot(x, y), z)
            p = math.atan2(y, x)
            rn = r ** n
            x = rn * math.sin(t * n) * math.cos(p * n) + cx
            y = rn * math.sin(t * n) * math.sin(p * n) + cy
            z = rn * math.cos(t * n) + cz
            if x * x + y * y + z * z > 4.0: break
        pixels[kx, ky] = (i % 4 * 64, i % 8 * 32, i % 16 * 16)
image.save("Mandelbulb.png", "PNG")
