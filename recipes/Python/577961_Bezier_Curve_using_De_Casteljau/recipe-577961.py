# Random Bezier Curve using De Casteljau's algorithm
# http://en.wikipedia.org/wiki/Bezier_curve
# http://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm
# FB - 201111244
import random
from PIL import Image, ImageDraw
imgx = 500
imgy = 500
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)

def B(coorArr, i, j, t):
    if j == 0:
        return coorArr[i]
    return B(coorArr, i, j - 1, t) * (1 - t) + B(coorArr, i + 1, j - 1, t) * t

n = random.randint(3, 6) # number of control points
coorArrX = []
coorArrY = []
for k in range(n):
    x = random.randint(0, imgx - 1)
    y = random.randint(0, imgy - 1)
    coorArrX.append(x)
    coorArrY.append(y)

# plot the curve
numSteps = 10000    
for k in range(numSteps):
    t = float(k) / (numSteps - 1)
    x = int(B(coorArrX, 0, n - 1, t))
    y = int(B(coorArrY, 0, n - 1, t))
    try:
        image.putpixel((x, y), (0, 255, 0))
    except:
        pass

# plot the control points
cr = 3 # circle radius
for k in range(n):
    x = coorArrX[k]
    y = coorArrY[k]
    try:
        draw.ellipse((x - cr, y - cr, x + cr, y + cr), (255, 0, 0))
    except:
        pass

image.save("BezierCurve.png", "PNG")
