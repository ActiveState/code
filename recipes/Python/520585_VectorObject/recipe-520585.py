#a class used for creating any object moving in 2D or a Vector Object (VObject)
#for direction use degrees, think of a 2d environment like:
#
#                  90
#                   |
#                   |
#           180 ----+----- 0
#                   |
#                   |
#                  270
#

from math import cos as _cos, sin as _sin, radians as _rad

class VObject():
    def __init__(self,x,y,speed,direction):
        self.x = x
        self.y = y
        self.s = speed
        self.d = _rad(direction)    

    def update(self,time=1):
        distance = self.s*time
        y = (_sin(self.d))*distance
        x = (_cos(self.d))*distance
        self.x += x
        self.y += y

    def addspeed(self,speed):
        self.s += speed

    def steer(self,angle):
        self.d += _rad(angle)

    def getx(self): return self.x
    def gety(self): return self.y
