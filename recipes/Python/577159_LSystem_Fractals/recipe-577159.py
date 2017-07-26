# L-System Fractals
# FB - 201003276
import math
from PIL import Image, ImageDraw
# image size
imgx = 512
imgy = 512 # will be auto-re-adjusted

# generate the fractal drawing string
def L_system(level, initial_state, trgt, rplcmnt, trgt2, rplcmnt2):
    state = initial_state
   
    for counter in range(level):
        state2 = ''
        for character in state:
            if character == trgt:
                state2 += rplcmnt
            elif character == trgt2:
                state2 += rplcmnt2
            else:
                state2 += character
        state = state2
    return state

def draw_fractal(length, numAngle, level, initial_state, trgt, rplcmnt, trgt2, rplcmnt2):
    global imgx, imgy
    fractal = L_system(level, initial_state, trgt, rplcmnt, trgt2, rplcmnt2)
    na = 2.0 * math.pi / numAngle
    sn = []
    cs = []
    for i in range(numAngle):
        sn.append(math.sin(na * i))
        cs.append(math.cos(na * i))

    # find xmin, xmax, ymin, ymax
    x = 0.0
    y = 0.0
    xa = x
    xb = x
    ya = y
    yb = y
    k = 0
    for ch in fractal:
        if ch == 'F':
            # turtle forward(length)
            x += length * cs[k]
            y += length * sn[k]
            if x < xa:
                xa = x
            if x > xb:
                xb = x
            if y < ya:
                ya = y
            if y > yb:
                yb = y
        elif ch == '+':
            # turtle right(angle)
            k = (k + 1) % numAngle
        elif ch == '-':
            # turtle left(angle)
            k = ((k - 1) + numAngle) % numAngle

    # draw the fractal
    imgy = round(imgy * (yb - ya) / (xb - xa)) # auto-re-adjust the aspect ratio 
    image = Image.new("L", (imgx, imgy))
    draw = ImageDraw.Draw(image)
    x = 0.0
    y = 0.0
    jx = int((x - xa) / (xb - xa) * (imgx - 1)) 
    jy = int((y - ya) / (yb - ya) * (imgy - 1))
    k = 0
    for ch in fractal:
        if ch == 'F':
            # turtle forward(length)
            x0 = x + length * cs[k]
            y0 = y + length * sn[k]
            jx0 = int((x - xa) / (xb - xa) * (imgx - 1)) 
            jy0 = int((y - ya) / (yb - ya) * (imgy - 1))
            draw.line ([(jx, jy),(jx0, jy0)], 255)
            x = x0
            y = y0
            jx = jx0
            jy = jy0
        elif ch == '+':
            # turtle right(angle)
            k = (k + 1) % numAngle
        elif ch == '-':
            # turtle left(angle)
            k = ((k - 1) + numAngle) % numAngle

    image.save("L_System.png", "PNG")

# main       
if __name__ == '__main__':
   
    # Levy Dragon
    # draw_fractal(1, 4, 16, 'FX', 'X', 'X+YF+', 'Y', '-FX-Y')

    # Koch Snowflake
    # draw_fractal(1, 6, 6, 'F++F++F', 'F', 'F-F++F-F', '', '')

    # Levy C
    draw_fractal(1, 8, 17, 'F', 'F', '+F--F+', '', '')

    # Hilbert Space-filling Curve fractal
    # draw_fractal(1, 4, 5, 'L', 'L', '+RF-LFL-FR+', 'R', '-LF+RFR+FL-')
