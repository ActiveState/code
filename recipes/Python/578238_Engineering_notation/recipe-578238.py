# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 15:49:13 2012

@author: Cambium
"""
from math import *

def powerise10(x):
    """ Returns x as a * 10 ^ b with 0<= a <10
    """
    if x == 0: return 0 , 0
    Neg = x <0
    if Neg : x = -x
    a = 1.0 * x / 10**(floor(log10(x)))
    b = int(floor(log10(x)))
    if Neg : a = -a
    return a ,b
    
def eng(x):
    """Return a string representing x in an engineer friendly notation"""
    a , b = powerise10(x)
    if -3<b<3: return "%.4g" % x
    a = a * 10**(b%3)
    b = b - b%3
    return "%.4g*10^%s" %(a,b)
    
    
if __name__ == '__main__':
        
    test = [-78951,-500,1e-3,0.005,0.05,0.12,10,23.3456789,50,150,250,800,1250,
            127e11,51234562]
        
    for x in test:
         print "%s: %s " % (x,powerise10(x))
         
    for x in test:
         print "%s: %s " % (x,eng(x))
        
