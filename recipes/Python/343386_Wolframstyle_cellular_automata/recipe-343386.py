#!/usr/bin/env python
"""
 CellularAutomata.py: Wolfram-style cellular automata in Python

 Options:
 -h #  Use a screen of height # for the simulation
 -w #  Use a screen of width # for the simulation
 -r      Use a random initial row (rather than the standard single 1 in the middle)
 -R #  Use rule # for the simulation

"""

import getopt,sys
from random import randint

def ca_data(height,width,dorandom,rulenum):
    # Create the first row, either randomly, or with a single 1
    if dorandom:
        first_row = [randint(0,1) for i in range(width)]
    else:
        first_row = [0]*width
        first_row[width/2] = 1
    results = [first_row]

    # Convert the rule number to a list of outcomes. 
    rule = [(rulenum/pow(2,i)) % 2 for i in range(8)]

    for i in range(height-1):
        data = results[-1]
        # Determine the new row based on the old data. We first make an
        #  integer out of the value of the old row and its two neighbors
        #  and then use that value to get the outcome from the table we
        #  computed earlier
        new = [rule[4*data[(j-1)%width]+2*data[j]+data[(j+1)%width]]
               for j in range(width)]
        results.append(new)
    return results

def pil_render(data,height,width,fname="bs.png"):
    import Image, ImageDraw
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        for x in range(width):
            if data[y][x]: draw.point((x,y),(0,0,0))
    img.save(fname,"PNG")
    return

def main():
    opts,args = getopt.getopt(sys.argv[1:],'h:w:rR:')
    height = 500
    width = 500
    dorandom = 0
    rule = 22
    for key,val in opts:
        if key == '-h': height = int(val)
        if key == '-w': width = int(val)
        if key == '-r': dorandom = 1
        if key == '-R': rule = int(val)
    data = ca_data(height,width,dorandom,rule)
    pil_render(data,height,width)
    return

if __name__ == '__main__': main()
