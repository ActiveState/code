# -*- coding: utf-8 -*-
"""
Created on Wed April 15th 2015

"""

from decimal import Decimal

def eng(num):
   return Decimal(num).normalize().to_eng_string() 
    
if __name__ == '__main__':
        
    test = [-78951,-500,1e-3,0.005,0.05,0.12,10,23.3456789,50,150,250,800,1250,
            127e11,51234562]
        
    for x in test:
         print "%s: %s " % (x,eng(x))
        
