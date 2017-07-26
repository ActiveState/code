#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also 
does a remarkable job of converting SVG files into other formats.

This is an enhanced Version of Rick Muller's Code from http://code.activestate.com/recipes/325823-draw-svg-images-in-python/
"""

import os
display_prog = "display"

class Scene:
    def __init__(self,name="svg",height=400,width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%d\" width=\"%d\" >\n" % (self.height,self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items: var += item.strarray()            
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return        

class Line:
    def __init__(self,start,end,color,width):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" style=\"stroke:%s;stroke-width:%d\"/>\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1],colorstr(self.color),self.width)]

class Circle:
    def __init__(self,center,radius,fill_color,line_color,line_width):
        self.center = center
        self.radius = radius
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;stroke:%s;stroke-width:%d\"  />\n" % (colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Ellipse:
    def __init__(self,center,radius_x,radius_y,fill_color,line_color,line_width):
        self.center = center
        self.radiusx = radius_x
        self.radiusy = radius_y
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
    def strarray(self):
        return ["  <ellipse cx=\"%d\" cy=\"%d\" rx=\"%d\" ry=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius_x,self.radius_y),
                "    style=\"fill:%s;stroke:%s;stroke-width:%d\"/>\n" % (colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Polygon:
    def __init__(self,points,fill_color,line_color,line_width):
        self.points = points
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
    def strarray(self):
        polygon="<polygon points=\""
        for point in self.points:
            polygon+=" %d,%d" % (point[0],point[1])
        return [polygon,\
               "\" \nstyle=\"fill:%s;stroke:%s;stroke-width:%d\"/>\n" %\
               (colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Rectangle:
    def __init__(self,origin,height,width,fill_color,line_color,line_width):
        self.origin = origin
        self.height = height
        self.width = width
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;stroke:%s;stroke-width:%d\" />\n" %\
                (self.width,colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Text:
    def __init__(self,origin,text,size,color):
        self.origin = origin
        self.text = text
        self.size = size
        self.color = color
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\" fill=\"%s\">\n" %\
                (self.origin[0],self.origin[1],self.size,colorstr(self.color)),
                "   %s\n" % self.text,
                "  </text>\n"]

def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def test():
    scene = Scene("test")
    scene.add(Rectangle((100,100),200,200,(0,255,255),(0,0,0),1))
    scene.add(Line((200,200),(200,300),(0,0,0),1))
    scene.add(Line((200,200),(300,200),(0,0,0),1))
    scene.add(Line((200,200),(100,200),(0,0,0),1))
    scene.add(Line((200,200),(200,100),(0,0,0),1))
    scene.add(Circle((200,200),30,(0,0,255),(0,0,0),1))
    scene.add(Circle((200,300),30,(0,255,0),(0,0,0),1))
    scene.add(Circle((300,200),30,(255,0,0),(0,0,0),1))
    scene.add(Circle((100,200),30,(255,255,0),(0,0,0),1))
    scene.add(Circle((200,100),30,(255,0,255),(0,0,0),1))
    scene.add(Text((50,50),"Testing SVG",24,(0,0,0)))
    scene.write_svg()
    scene.display()
    return

if __name__ == "__main__": test()
