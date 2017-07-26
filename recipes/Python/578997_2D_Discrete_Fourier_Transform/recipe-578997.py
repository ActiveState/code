# 2D Discrete Fourier Transform (DFT) and its inverse
# Warning: Computation is slow so only suitable for thumbnail size images!
# FB - 20150102
from PIL import Image
import cmath
pi2 = cmath.pi * 2.0

def DFT2D(image):
    global M, N
    (M, N) = image.size # (imgx, imgy)
    dft2d_red = [[0.0 for k in range(M)] for l in range(N)] 
    dft2d_grn = [[0.0 for k in range(M)] for l in range(N)] 
    dft2d_blu = [[0.0 for k in range(M)] for l in range(N)] 
    pixels = image.load()
    for k in range(M):
        for l in range(N):
            sum_red = 0.0
            sum_grn = 0.0
            sum_blu = 0.0
            for m in range(M):
                for n in range(N):
                    (red, grn, blu, alpha) = pixels[m, n]
                    e = cmath.exp(- 1j * pi2 * (float(k * m) / M + float(l * n) / N))
                    sum_red += red * e
                    sum_grn += grn * e
                    sum_blu += blu * e
            dft2d_red[l][k] = sum_red / M / N
            dft2d_grn[l][k] = sum_grn / M / N
            dft2d_blu[l][k] = sum_blu / M / N
    return (dft2d_red, dft2d_grn, dft2d_blu)
        
def IDFT2D(dft2d):
    (dft2d_red, dft2d_grn, dft2d_blu) = dft2d
    global M, N
    image = Image.new("RGB", (M, N))
    pixels = image.load() 
    for m in range(M):
        for n in range(N):
            sum_red = 0.0
            sum_grn = 0.0
            sum_blu = 0.0
            for k in range(M):
                for l in range(N):
                    e = cmath.exp(1j * pi2 * (float(k * m) / M + float(l * n) / N))
                    sum_red += dft2d_red[l][k] * e
                    sum_grn += dft2d_grn[l][k] * e
                    sum_blu += dft2d_blu[l][k] * e
            red = int(sum_red.real + 0.5)
            grn = int(sum_grn.real + 0.5)
            blu = int(sum_blu.real + 0.5)
            pixels[m, n] = (red, grn, blu)
    return image

# TEST
# Recreate input image from 2D DFT results to compare to input image
image = IDFT2D(DFT2D(Image.open("input.png")))
image.save("output.png", "PNG")
