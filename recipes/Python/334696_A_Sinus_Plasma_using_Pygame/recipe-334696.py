import pygame
from pygame.locals import *
import random
import Numeric
from math import *

WIDTH = 320     #width of screen
HEIGHT = 240    #height of screen

    
def main():
    pygame.display.init()
    
    screen = pygame.display.set_mode((WIDTH,HEIGHT),DOUBLEBUF,32)
    pixels = pygame.surfarray.pixels3d(screen)
    
    width = len(pixels)-1
    height = len(pixels[0])-1
    freq = 100.0
    
    for y in xrange(height):
        for x in xrange(width):
            z1 = sin(x/freq*1.7*pi)
            z2 = sin((x/3+y)/freq*1.5*pi)
            z3 = sin(y/freq*0.1*pi)
            
            z = abs(z1+z2+z3)*255
            pixels[x,y] = (z,z/4,z*4)

    pygame.display.update()
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                done = True
        
if __name__ == "__main__":
    main()
