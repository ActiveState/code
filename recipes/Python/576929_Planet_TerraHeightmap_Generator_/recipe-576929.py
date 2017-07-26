#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageChops, ImageOps, ImageFilter
import pygame.display, pygame.image
import random
import sys
from math import ceil

percentWater = .70
mapSize = 600 #in pixels
maxSize = 1.40 # 1 to 5 How big should the slices be cut, smaller slices create more islands, larger slices create less
shape = 1.40 # 1 mean roundish continents .5 is twice as tall as it is wide, 2.0 is twice as wide as tall
driftRate = .70 # As the world ages how much slower does it drift.  1 creates a more textured world but takes longer
roughness = 1 #High numbers make a world faster, with more "ridges", but also makes things less "smooth"
filename = 'heightmap.bmp'

xrand = lambda ms = mapSize*3: int(randType(0, ms))
yrand = lambda ms = mapSize*2: int(randType(0-(ms/2), ms))
randType =  random.uniform #change to alter variability



def normalize(image): 
    image = image.filter(ImageFilter.BLUR)
    picture = ImageChops.blend(ImageOps.equalize(image), image, .5)
    return ImageChops.multiply(picture, picture)

def finish(image): #called when window is closed, or iterations stop
    picture = normalize(image)
    picture.save(filename)
    pygame.quit()
    sys.exit();

def drawPieSlices(oval, orig, action):
    fl = action[1]
    img = Image.new('L', (mapSize*2,mapSize))
    draw = ImageDraw.Draw(img)
    draw.pieslice([oval[0],oval[1],mapSize*4,oval[3]], 90, 270, fill=fl)
    del draw
    orig = action[0](orig, img)
    img = Image.new('L', (mapSize*2,mapSize))
    draw = ImageDraw.Draw(img)
    draw.pieslice([0-oval[0],oval[1],oval[2]-mapSize*2,oval[3]], 270, 90, fill=fl)
    del draw
    return action[0](orig, img)

def drawOval(oval, orig, action):
    img = Image.new('L', (mapSize*2,mapSize))
    draw = ImageDraw.Draw(img)
    draw.ellipse(oval, fill=action[1])
    del draw
    return action[0](orig, img)

def cutOval(orig, smallness=1):
    smallness = smallness ** driftRate
    landAction = lambda: (
        ImageChops.add, 
        ceil(randType(1,roughness*smallness*(percentWater)))
        )
    seaAction = lambda: (
        ImageChops.subtract, 
        ceil(randType(1,roughness*smallness*(1.0-percentWater)))
        )
    action = seaAction() if random.random() < percentWater else landAction()
    oval = [xrand(mapSize*2),yrand(mapSize),1,1] #x,y,x,y
    oval[2] = int(oval[0]+(mapSize*maxSize*shape)*smallness)
    oval[3] = int(oval[1]+(mapSize*maxSize)*smallness)
    if oval[2] > mapSize*2: #if x values cross our border, we needto wrap
        ret = drawPieSlices(oval, orig, action)
    else:
        ret = drawOval(oval, orig, action)
    return ret

imageToPygame = lambda i: pygame.image.fromstring(i.tostring(), i.size, i.mode)

def highestPointOnSphere(sphere):
    extremes = sphere.getextrema()
    return extremes[0]/255.0 if percentWater > .5 else 1-(extremes[1]/255.0)

def createSphere():
    pygame.init() #Need this to render the output
    sphere = Image.new('L', (mapSize*2,mapSize))
    img = ImageDraw.Draw(sphere)
    baseline = (256*(1.0-(percentWater)))
    img.rectangle([0-mapSize,0,mapSize*4,mapSize], fill=baseline)
    del img
    return sphere

def sphereToPicture(sphere):
    picture = normalize(sphere)
    picture = ImageOps.colorize(picture, (10,0,100), (0,256,0))
    picture = imageToPygame(picture)
    return picture

def generatePlanet(sphere, displayInterval = 50):
    extrema = highestPointOnSphere(sphere)
    i = 0
    picture = sphereToPicture(sphere)
    pygame.display.set_mode(picture.get_size())
    main_surface = pygame.display.get_surface()
    del picture
    while extrema > driftRate/(roughness*10*maxSize):
        sphere = cutOval(sphere, extrema)
        i = i+1
        if displayInterval > 0 and i%displayInterval == 0:
            picture = sphereToPicture(sphere)
            main_surface.blit(picture, (0, 0))
            pygame.display.update()
            del picture

        for event in pygame.event.get(): #When people close the window
            if event.type == pygame.QUIT:    
                return image
        extrema = highestPointOnSphere(sphere)
    return sphere
if __name__ == '__main__':
    finish(generatePlanet(createSphere(), 50))
