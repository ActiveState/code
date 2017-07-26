# Chaotic Function Analysis Graph
# GrX = Xn
# GrY = Xn+1
# FB - 201012094
import math
import random
from PIL import Image
imgx = 800
imgy = 600
image = Image.new("RGB", (imgx, imgy))
# drawing region
xa = 0.0
xb = 1.0
ya = 0.0
yb = 1.0

x0 = random.random() # initial x does not matter for this type of graph
x1 = x0 # prev x
x2 = x1 # prev of prev x

maxIt = 100000

for i in range(maxIt):
    x2 = x1
    x1 = x0

    # chaotic function to graph
    # x0 = math.fmod(math.fabs(math.sin(3.0 * x1 + 0.3)), 1.0) # (0)
    # x0 = math.fmod((x1 + math.pi) ** 2.0, 1.0)             # (1)
    # x0 = math.fmod((x1 + x2 + math.pi) ** 2.0, 1.0)        # (2) PRNG?
    x0 = 4.0 * x1 * (1.0 - x1) # (3) logistic equation in chaotic state
    # x0 = (x2 + 3.0) * x1 * (1.0 - x1) # (4) ?

    xi = int((imgx - 1) * (x1 - xa) / (xb - xa))
    yi = int((imgy - 1) * (x0 - ya) / (yb - ya))
    if xi >=0 and xi < imgx and yi >= 0 and yi < imgy:
        image.putpixel((xi, yi), (255, 255, 255))
    
image.save("chaotic_function_graph.png", "PNG")
