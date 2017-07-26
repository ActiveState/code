from random import *
from numpy import *

darts=input("How many darts? ")

x=random.random(darts)
y=random.random(darts)
one=ones(darts)

dist=sqrt(x*x+y*y)
print "dist ",dist
hit=(less_equal(dist,one)==True)
print "hit ",hit
hits=sort(hit)
print "hits ",hits
hitsnum=hits.searchsorted(True, side="right") - hits.searchsorted(True, side="left")
print "hitsnum ",hitsnum

pic=4.0*hitsnum/darts
print "Pi calculated as ",pic
error=100*(pic-3.1415926535897932)/(3.1415926535897932)
print "Error is ", error, "%"
