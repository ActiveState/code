# Random percolation cluster fractals
# FB - 201003243
from PIL import Image
from PIL import ImageDraw
import random
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
maxIt = imgx * imgy / 1.25
for i in range(maxIt):
    x = random.randint(0, imgx - 1)
    y = random.randint(0, imgy - 1)
    r = random.randint(1, 255)
    g = random.randint(1, 255)
    b = random.randint(1, 255)
    r2 = random.randint(1, 255)
    g2 = random.randint(1, 255)
    b2 = random.randint(1, 255)
    image.putpixel((x, y), (r, g, b))
    ImageDraw.floodfill(image, (x, y), (r2, g2, b2), (0, 0, 0))

image.save("percolation.png", "PNG")
