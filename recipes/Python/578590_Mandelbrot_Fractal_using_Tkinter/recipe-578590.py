# Mandelbrot Fractal using Tkinter
# FB36 - 20130706
import Tkinter
from Tkinter import *
WIDTH = 640; HEIGHT = 480
xa = -2.0; xb = 1.0
ya = -1.5; yb = 1.5
maxIt = 256

window = Tk()
canvas = Canvas(window, width = WIDTH, height = HEIGHT, bg = "#000000")
img = PhotoImage(width = WIDTH, height = HEIGHT)
canvas.create_image((0, 0), image = img, state = "normal", anchor = Tkinter.NW)

for ky in range(HEIGHT):
    for kx in range(WIDTH):
        c = complex(xa + (xb - xa) * kx / WIDTH, ya + (yb - ya) * ky / HEIGHT)
        z = complex(0.0, 0.0)
        for i in range(maxIt):
            z = z * z + c
            if abs(z) >= 2.0:
                break
        rd = hex(i % 4 * 64)[2:].zfill(2)
        gr = hex(i % 8 * 32)[2:].zfill(2)
        bl = hex(i % 16 * 16)[2:].zfill(2)
        img.put("#" + rd + gr + bl, (kx, ky))

canvas.pack()
mainloop()
