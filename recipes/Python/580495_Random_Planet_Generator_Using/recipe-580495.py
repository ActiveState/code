# Random Planet Generator Using 3D Plasma Fractal
# and Voxel-based Ray Tracing for rendering
# (Instead of generating 2D Plasma Fractal and projecting onto sphere,
# it generates 3D Plasma Fractal (cube) and cuts sphere from it.)
# FB - 20160125
import math
import random
from PIL import Image
imgx = 256; imgy = 256; imgz = 256
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
print "Creating voxels..."
# each voxel can have RGB color
voxelRGB = [[[(0, 0, 0) for x in range(imgx)] for y in range(imgy)] for z in range(imgz)]
# each voxel can have an opacity coefficient 0 or 1 (for simplicity)
opacity = [[[0 for x in range(imgx)] for y in range(imgy)] for z in range(imgz)]
eye = (imgx / 2.0, imgy / 2.0, -imgz / 2.0)
mx = imgx - 1; my = imgy - 1; mz = imgz - 1
f = 5.0 # roughness

def rnd():
    return (random.random() - .5) * f

def putvoxel(x, y, z, r, g, b):
    global voxelRGB, opacity
    x = int(round(x)); y = int(round(y)); z = int(round(z))
    voxelRGB[z][y][x] = (int(round(r)), int(round(g)), int(round(b)))
    opacity[z][y][x] = 1

def getvoxel(x, y, z):
    return voxelRGB[int(round(z))][int(round(y))][int(round(x))]

def CreatePlasmaCube(): # using non-recursive Diamond-square Algorithm
    global voxelRGB, opacity
    # corners
    for kz in range(2):
        for ky in range(2):
            for kx in range(2):
                putvoxel(mx * kx, my * ky, mz * kz, \
                    random.randint(0, 255), \
                    random.randint(0, 255), \
                    random.randint(0, 255))

    j = -1
    while True:
        j += 1; j2 = 2 ** j
        jx = float(mx) / j2; jy = float(my) / j2; jz = float(mz) / j2
        if jx < 1 and jy < 1 and jz < 1: break
        for m in range(j2):
            z0 = m * jz; z1 = z0 + jz; z = z0 + jz / 2.0        
            for i in range(j2):
                y0 = i * jy; y1 = y0 + jy; y = y0 + jy / 2.0        
                for k in range(j2):
                    x0 = k * jx; x1 = x0 + jx; x = x0 + jx / 2.0
                
                    a = getvoxel(x0, y0, z0); b = getvoxel(x1, y0, z0)
                    c = getvoxel(x0, y1, z0); d = getvoxel(x1, y1, z0)
                    e = getvoxel(x0, y0, z1); f = getvoxel(x1, y0, z1)
                    g = getvoxel(x0, y1, z1); h = getvoxel(x1, y1, z1)

                    # center
                    putvoxel(x, y, z, \
                        (a[0] + b[0] + c[0] + d[0] + e[0] + f[0] + g[0] + h[0]) / 8.0, \
                        (a[1] + b[1] + c[1] + d[1] + e[1] + f[1] + g[1] + h[1]) / 8.0, \
                        (a[2] + b[2] + c[2] + d[2] + e[2] + f[2] + g[2] + h[2]) / 8.0)

                    # centers of 6 faces
                    putvoxel(x, y, z0, \
                        (a[0] + b[0] + c[0] + d[0]) / 4.0, \
                        (a[1] + b[1] + c[1] + d[1]) / 4.0, \
                        (a[2] + b[2] + c[2] + d[2]) / 4.0)
                    putvoxel(x, y, z1, \
                        (e[0] + f[0] + g[0] + h[0]) / 4.0, \
                        (e[1] + f[1] + g[1] + h[1]) / 4.0, \
                        (e[2] + f[2] + g[2] + h[2]) / 4.0)
                    putvoxel(x, y0, z, \
                        (a[0] + b[0] + e[0] + f[0]) / 4.0, \
                        (a[1] + b[1] + e[1] + f[1]) / 4.0, \
                        (a[2] + b[2] + e[2] + f[2]) / 4.0)
                    putvoxel(x, y1, z, \
                        (c[0] + d[0] + g[0] + h[0]) / 4.0, \
                        (c[1] + d[1] + g[1] + h[1]) / 4.0, \
                        (c[2] + d[2] + g[2] + h[2]) / 4.0)
                    putvoxel(x0, y, z, \
                        (a[0] + c[0] + e[0] + g[0]) / 4.0, \
                        (a[1] + c[1] + e[1] + g[1]) / 4.0, \
                        (a[2] + c[2] + e[2] + g[2]) / 4.0)
                    putvoxel(x1, y, z, \
                        (b[0] + d[0] + f[0] + h[0]) / 4.0, \
                        (b[1] + d[1] + f[1] + h[1]) / 4.0, \
                        (b[2] + d[2] + f[2] + h[2]) / 4.0)

                    # centers of 12 edges
                    putvoxel(x, y0, z0, \
                        (a[0] + b[0]) / 2.0 + jx * rnd(), \
                        (a[1] + b[1]) / 2.0 + jx * rnd(), \
                        (a[2] + b[2]) / 2.0 + jx * rnd())
                    putvoxel(x0, y, z0, \
                        (a[0] + c[0]) / 2.0 + jy * rnd(), \
                        (a[1] + c[1]) / 2.0 + jy * rnd(), \
                        (a[2] + c[2]) / 2.0 + jy * rnd())
                    putvoxel(x1, y, z0, \
                        (b[0] + d[0]) / 2.0 + jy * rnd(), \
                        (b[1] + d[1]) / 2.0 + jy * rnd(), \
                        (b[2] + d[2]) / 2.0 + jy * rnd()) 
                    putvoxel(x, y1, z0, \
                        (c[0] + d[0]) / 2.0 + jx * rnd(), \
                        (c[1] + d[1]) / 2.0 + jx * rnd(), \
                        (c[2] + d[2]) / 2.0 + jx * rnd())
                    putvoxel(x, y0, z1, \
                        (e[0] + f[0]) / 2.0 + jx * rnd(), \
                        (e[1] + f[1]) / 2.0 + jx * rnd(), \
                        (e[2] + f[2]) / 2.0 + jx * rnd())
                    putvoxel(x0, y, z1, \
                        (e[0] + g[0]) / 2.0 + jy * rnd(), \
                        (e[1] + g[1]) / 2.0 + jy * rnd(), \
                        (e[2] + g[2]) / 2.0 + jy * rnd())
                    putvoxel(x1, y, z1, \
                        (f[0] + h[0]) / 2.0 + jy * rnd(), \
                        (f[1] + h[1]) / 2.0 + jy * rnd(), \
                        (f[2] + h[2]) / 2.0 + jy * rnd()) 
                    putvoxel(x, y1, z1, \
                        (g[0] + h[0]) / 2.0 + jx * rnd(), \
                        (g[1] + h[1]) / 2.0 + jx * rnd(), \
                        (g[2] + h[2]) / 2.0 + jx * rnd())
                    putvoxel(x0, y0, z, \
                        (a[0] + e[0]) / 2.0 + jz * rnd(), \
                        (a[1] + e[1]) / 2.0 + jz * rnd(), \
                        (a[2] + e[2]) / 2.0 + jz * rnd())
                    putvoxel(x1, y0, z, \
                        (b[0] + f[0]) / 2.0 + jz * rnd(), \
                        (b[1] + f[1]) / 2.0 + jz * rnd(), \
                        (b[2] + f[2]) / 2.0 + jz * rnd())
                    putvoxel(x0, y1, z, \
                        (c[0] + g[0]) / 2.0 + jz * rnd(), \
                        (c[1] + g[1]) / 2.0 + jz * rnd(), \
                        (c[2] + g[2]) / 2.0 + jz * rnd())
                    putvoxel(x1, y1, z, \
                        (d[0] + h[0]) / 2.0 + jz * rnd(), \
                        (d[1] + h[1]) / 2.0 + jz * rnd(), \
                        (d[2] + h[2]) / 2.0 + jz * rnd())

# cx, cy, cz: center; r: radius (in voxels)
def CreateSphere(cx, cy, cz, r):
    global voxelRGB, opacity
    # sphere is set of voxels which have distance = r to center
    for z in range(imgz):
        for y in range(imgy):
            for x in range(imgx):
                dx = x - cx
                dy = y - cy
                dz = z - cz
                d = math.sqrt(dx * dx + dy * dy + dz * dz)
                if abs(d - r) > 1.0:
                    voxelRGB[z][y][x] = (0, 0, 0)
                    opacity[z][y][x] = 0

# Ray Tracer (traces the ray and returns an RGB color)
def RayTrace(rayX, rayY, rayZ, dx, dy, dz):
    while True:
        rayX += dx; rayY += dy; rayZ += dz # move the ray by 1 voxel
        rayXint = int(round(rayX)); rayYint = int(round(rayY)); rayZint = int(round(rayZ))
        # if ray goes outside of the voxel-box
        if rayXint < 0 or rayXint > imgx - 1 \
            or rayYint < 0 or rayYint > imgy - 1 \
            or rayZint < 0 or rayZint > imgz - 1:
            return (0, 0, 0)
        # if ray hits an object
        if opacity[rayZint][rayYint][rayXint] == 1:
            return voxelRGB[rayZint][rayYint][rayXint]

def CreateScene():
    print "Creating scene..."
    CreatePlasmaCube()
    CreateSphere(imgx / 2.0, imgy / 2.0, imgz / 2, min(imgx / 2.0, imgy / 2.0, imgz / 2))

def RenderScene():
    print "Rendering scene..."
    for ky in range(imgy):
        print str(100 * ky / (imgy - 1)).zfill(3) + "%"
        for kx in range(imgx):
            dx = kx - eye[0]
            dy = ky - eye[1]
            dz = 0.0 - eye[2]
            d = math.sqrt(dx * dx + dy * dy + dz * dz)
            dx = dx / d; dy = dy / d; dz = dz / d # ray unit vector
            pixels[kx, ky] = RayTrace(kx, ky, 0, dx, dy, dz)

# MAIN
CreateScene()
RenderScene()
image.save("RandomPlanet.png", "PNG")
