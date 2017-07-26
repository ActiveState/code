# dot2svg.py
# Author: Simon Frost, UCSD
# Date  : 17th October 2003
# Description: This is a simple demonstration of how to use
# WinGraphViz (http://home.so-net.net.tw/oodtsen/wingraphviz/index.htm)
# from Python (http://www.python.org) using Mark Hammond's win32all extensions
# (http://starship.python.net/crew/mhammond/win32/). It takes a graph in DOT
# format, and writes the graph in SVG.

from win32com.client import Dispatch
import sys

def toSVG(filename):
    graphViz=Dispatch("WINGRAPHVIZ.dot")
    f=open(filename,'r')
    data = f.read()
    f.close()
    img=graphViz.toSVG(data)
    f=open(str(filename)+'.svg','w')
    f.write(img)
    f.close()
    
if __name__=="__main__":
    if len(sys.argv)<2:
        print "Usage: python dot2svg.py mygraph.dot"
    filename=sys.argv[1]
    toSVG(filename)
