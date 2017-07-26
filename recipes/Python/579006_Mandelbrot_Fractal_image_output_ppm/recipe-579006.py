# Mandelbrot Fractal image output to ppm file
# FB - 20150117
imgx = 512; imgy = 512
xa = -2.0; xb = 1.0
ya = -1.5; yb = 1.5
maxIt = 256
rgbPixels = ""
for ky in range(imgy):
    for kx in range(imgx):
        c = complex(xa + (xb - xa) * kx / imgx, ya + (yb - ya) * ky / imgy)
        z = complex(0.0, 0.0)
        for i in range(maxIt):
            z = z * z + c
            if abs(z) >= 2.0:
                break
        rgbPixels += chr(i % 4 * 64) + chr(i % 8 * 32) + chr(i % 16 * 16)

f = open("ManFr.ppm", "wb")
f.write("P6\n")
f.write("# ManFr.ppm\n") # comment
f.write(str(imgx) + " " + str(imgy) + "\n")
f.write(str(255) + "\n") # max color value
f.write(rgbPixels)
f.close()
