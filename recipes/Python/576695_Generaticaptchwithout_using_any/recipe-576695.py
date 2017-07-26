from PIL import Image, ImageDraw
from random import *

def symbols():
  sym = [None] * 10
  sym[0] = (0,1,1,1,1,1,1)
  sym[1] = (0,1,0,0,0,0,1)
  sym[2] = (1,1,1,0,1,1,0)
  sym[3] = (1,0,1,1,1,1,0)
  sym[4] = (1,0,0,1,1,0,1)
  sym[5] = (1,0,1,1,0,1,1)
  sym[6] = (1,1,1,1,0,1,1)
  sym[7] = (0,0,0,1,1,1,1)
  sym[8] = (1,1,1,1,1,1,1)
  sym[9] = (1,0,1,1,1,1,1)
  return sym

def drawsymbol(im,sym,len,pos,step,dr,lines):
  draw = ImageDraw.Draw(im)
  dir = [(-1,0),(0,+1),(+1,0),(0,-1),(0,-1),(-1,0),(0,+1)]
  x,y = pos
  for i,l in enumerate(sym):
    xf, yf = x+dir[i][0]*len, y+dir[i][1]*len
    rx = [x] if abs(x-xf) == 0 else range(min(x,xf),max(x,xf),step)
    ry = [y] if abs(y-yf) == 0 else range(min(y,yf),max(y,yf),step)
    if l:
      for cx in rx:
        for cy in ry:
          for n in range(lines):
            dx, dy = 0,0
            dsx,dsy = 0,0
            while 0 in [dx,dy]:
              dx, dy = randint(-dr,dr), randint(-dr,dr)
              dsx, dsy = randint(-dr,dr), randint(-dr,dr)
            draw.line([cx+dsx,cy+dsy,cx+dx,cy+dy],fill=0,width=1)
    x,y = xf, yf

def drawnoise(im,step,dr):
  draw = ImageDraw.Draw(im)
  w,h = im.size
  for x in range(0,w,step):
    for y in range(0,h,step):
      draw.line([x+randint(-dr,dr),y+randint(-dr,dr),x+randint(-dr,dr),y+randint(-dr,dr)],fill=0,width=1)

if __name__ == "__main__":
  sym = symbols()
  nums = [randint(0,9) for x in range(10)]
  im = Image.new('L', (230,50), 220)
  drawnoise(im,10,30)
  for i,s in enumerate(nums):
    drawsymbol(im,sym[s],12,(22*(i+1),25),1,4,2)
  print 'Number',''.join(str(x) for x in nums),'generated as captcha.jpg'
  im.save('captcha.jpg')
