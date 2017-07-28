from __future__ import print_function
import math
import fitz
"""
@created: 2017-06-18 10:00:00

@author: (c) Jorj X. McKie

Demo for creating simple graphics with method 'Page.drawLine()'.

Dependencies:
PyMuPDF, math

License:
 GNU GPL 3+

Sketching a caustic. This is the figure the early morning sun paints onto
your desperately needed cup of coffee from an angle on your left side ...

"""
def pvon(a):                 # starting point of one sun ray
    return(math.cos(a), math.sin(a))

def pbis(a):                 # end point of one sun ray
    return(math.cos(3*a - math.pi), (math.sin(3*a - math.pi)))

# create new PDF with an empty square format page
doc = fitz.open()
doc.insertPage(-1, width = 800, height = 800)
page = doc[0]                # get the page just created

# if you want a coffee background, use some picture reflecting your
# preferred amount of milk.
page.insertImage(page.rect, "coffee.jpg")

# middle of the circle of the page
mitte = fitz.Point(page.rect.width / 2, page.rect.height / 2)

# radius leaves a border of 20 pixels
radius = page.rect.width / 2 - 20

# how many sun rays we paint
count = 200
interval = math.pi / count
color = (1, 1, 0)                                # this is plain yellow
for i in range(1, count):
    a = -math.pi / 2 + i * interval
    von = fitz.Point(pvon(a))*radius + mitte     # start point adjusted
    bis = fitz.Point(pbis(a))*radius + mitte     # end point adjusted
    page.drawLine(von, bis, width = 0.5, color = color)

doc.save("caustic.pdf", garbage = 4, deflate = True)
