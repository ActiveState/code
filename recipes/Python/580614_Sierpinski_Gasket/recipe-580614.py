#!/usr/bin/env python
# coding: UTF-8
#
## @package _16_sierpinski
#
# Draws a Sierpinski Gasket.
#
# Usage: _16_sierpinski [number_of_divisions]
#
# @author Paulo Roma Cavalcanti 
# @since 09/02/2016
# @see http://paulbourke.net/fractals/gasket/
# @see https://en.wikipedia.org/wiki/Sierpinski_triangle
# @see http://ecademy.agnesscott.edu/~lriddle/ifs/siertri/siertri.htm
# @see http://www.oftenpaper.net/sierpinski.htm

import sys
try:
  from tkinter import *  # python 3
except ImportError:
  from Tkinter import *  # python 2

##  Creates a Sierpinski Gasket, by recursively partitioning
 #  an initial triangle (a,b,c) into three or four new triangles.
 #
 #  - There will be:
 #    - @f$3^{count}@f$ red triangles or 
 #    - @f$4^{count}@f$ if the fourth triangle is drawn.
 #
 #  - The number of white triangles is a Geometric Progression, starting at 1 and with ratio 3, given by:
 #     - P(0) = 0
 #     - P(n) = 3 * P(n-1) + 1
 #     - P(n) = @f$\frac{(3^n-1)}{2}.@f$
 #
 #  @param a first vertex coordinates.
 #  @param b second vertex coordinates.
 #  @param c third vertex coordinates.
 #  @param n number of subdivisions on each edge (depth of recursion).
 #  @param fourth whether to add the fourth triangle.
 #
def Sierpinski(a, b, c, n, fourth=False):
    ## list of points (a set of triangles).
    points = []

    ## Pushes three vertices to the list of points.
    def triangle( a, b, c ):
        points.append ( a )
        points.append ( b )
        points.append ( c )

    ## Returns a point on segment p1-p2 corresponding to parameter s.
    def mix(p1,p2,s):
        return [(p1[0]+p2[0])*s, (p1[1]+p2[1])*s]

    ## Divides triangle (a,b,c), by recursively subdividing
     # each edge at its middle point, and connecting the new points.
    def divideTriangle( a, b, c, count ):
        # check for end of recursion
        if ( count == 0 ):
            triangle( a, b, c )
        else:
            # bisect the sides
            ab = mix( a, b, 0.5 )
            ac = mix( a, c, 0.5 )
            bc = mix( b, c, 0.5 )

            count -= 1

            # three new triangles
            divideTriangle( a, ab, ac, count )
            divideTriangle( c, ac, bc, count )
            divideTriangle( b, bc, ab, count )

            # add the middle triangle
            if ( fourth ): divideTriangle( ac, bc, ab, count )

    divideTriangle (a, b, c, n)
    return points

## Draw triangles, given in points, on canvas c.
def draw(c, points, contour=False):
    w = c.winfo_width()//2
    h = c.winfo_height()//2
    centerx = w
    centery = h
    c.delete(ALL)
    for i in range(0,len(points),3):
        if ( not contour ):
            c.create_polygon(centerx+w*points[i]  [0],centery-h*points[i  ][1], 
                             centerx+w*points[i+1][0],centery-h*points[i+1][1], 
                             centerx+w*points[i+2][0],centery-h*points[i+2][1], fill='red', outline='black')
        else: 
            c.create_line(centerx+w*points[i]  [0],centery-h*points[i  ][1], 
                          centerx+w*points[i+1][0],centery-h*points[i+1][1], 
                          centerx+w*points[i+2][0],centery-h*points[i+2][1],
                          centerx+w*points[i]  [0],centery-h*points[i  ][1], fill='black', width=2)

## Main program.
def main(argv=None):

    ## Resize the graphics when the window changes.
    def resize(event=None):
        global pts
        draw(canvas, pts, cntVar.get()=='ON')

    ## Redraw the graphics when the scale changes
    def redraw(event=None):
        global pts

        # Initialize the corners of the gasket with three points.
        vertices = [
            [ -1, -1 ],
            [  0,  1 ],
            [  1, -1 ]
        ]
        pg = lambda n: (3**n-1)//2 
        ndiv = slider.get()
        pts = Sierpinski( vertices[0], vertices[1], vertices[2], ndiv, fillVar.get()=='ON' )
        lr.configure(text="Red Triangles = %d     "%(len(pts)//3))
        la.configure(text="   White Triangles = %d"%(pg(ndiv)))
        resize(event)

    ndiv = 2

    if argv is None:
       argv = sys.argv
    if len(argv) > 1:
       try:
          ndiv = abs(int(argv[1]))
       except:
          ndiv = 3 

    root = Tk()
    root.title("Sierpinski Gasket")
    bot = Frame(root)
    bot.pack(side=BOTTOM)
    top = Frame(root)
    top.pack(side=TOP)
    canvas = Canvas(root,width=400,height=400);
    canvas.bind("<Configure>", resize)
    canvas.pack(expand=YES,fill=BOTH)

    slider = Scale(bot, from_=0, to=8, command=redraw, orient=HORIZONTAL)
    slider.set(ndiv)
    slider.pack(side=LEFT, anchor = W)

    cntVar = StringVar()  # create a checkbutton for the drawing style
    cntVar.set ( "OFF" )
    c = Checkbutton (bot, text="Contour", variable=cntVar, onvalue="ON", offvalue="OFF", command=resize)
    c.pack(side=BOTTOM)

    fillVar = StringVar()  # create another checkbutton for the number of triangles
    fillVar.set ( "OFF" )
    c = Checkbutton (bot, text="Fill", variable=fillVar, onvalue="ON", offvalue="OFF", command=redraw)
    c.pack(side=LEFT)

    lr = Label(top, text="")
    lr.pack(side=LEFT,anchor = W)
    la = Label(top, text="")
    la.pack(side=RIGHT,anchor = E)

    redraw(None)

    mainloop()

if __name__=='__main__':
    sys.exit(main())
