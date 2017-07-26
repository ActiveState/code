# Draw (Bitmap Font) Text to Image
from PIL import Image, ImageDraw, ImageFont

def reverseColor(r, g, b):
    return (255 - r, 255 - g, 255 - b)
def grayscaleColor(r, g, b):
    a = (r + g + b) / 3
    return (a, a, a)

text = "Hello World!"
# textColor = (255, 255, 0) # RGB Yellow
# textBackgroundColor = (255, 0, 0) # RGB Red
textX = 400 # text width in pixels
textY = 100 # text height in pixels
textTopLeftX = 0
textTopLeftY = 0

# create new image
# imgx = 800 # image width in pixels
# imgy = 600 # image height in pixels
# image = Image.new("RGB", (imgx, imgy))

# load image
image = Image.open("input.png")
(imgx, imgy) = image.size
# image = image.resize((imgx, imgy), Image.BICUBIC)

font = ImageFont.load_default() # load default bitmap font
(width, height) = font.getsize(text)
textImage = font.getmask(text)
pixels = image.load()
for y in range(imgy):
    by = int(height * (y - textTopLeftY) / textY + 0.5)
    if by >= 0 and by < height:
        for x in range(imgx):
            bx = int(width * (x - textTopLeftX) / textX + 0.5)
            if bx >= 0 and bx < width:
                if textImage.getpixel((bx, by)) == 0: # text background
                    # pass # transparent background
                    # pixels[x, y] = textBackgroundColor
                    # (r, g, b, a) = pixels[x, y]
                    (r, g, b) = pixels[x, y]
                    pixels[x, y] = grayscaleColor(r, g, b)
                else: # text foreground
                    # pixels[x, y] = textColor                
                    # (r, g, b, a) = pixels[x, y]
                    (r, g, b) = pixels[x, y]
                    pixels[x, y] = reverseColor(r, g, b)

image.save("output.png", "PNG")
