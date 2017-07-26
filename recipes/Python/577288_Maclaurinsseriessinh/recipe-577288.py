#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_sinh is a function to compute sinh(x) using maclaurin series
and the interval of convergence is -inf < x < +inf 
sinh(x) = x + x^3/3! + x^5/5! + x^7/7! ...........
"""

from math import *

def maclaurin_sinh(value, k):
    """
    Compute maclaurin's series approximation for sinh(x)
    """
    
    global first_value    
    first_value = 0.0
    
    #attempt to Approximate sinh(x) for a given value    
    try:
        for item in xrange(1,k,2):
            next_value = (value*pi/180)**item/factorial(item)
            first_value += next_value
            
        return first_value
    
    #Raise TypeError if input is not a number   
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_sinh1 = maclaurin_sinh(70,100)
    print maclaurin_sinh1
    maclaurin_sinh2 = maclaurin_sinh(45,100)
    print maclaurin_sinh2
    maclaurin_sinh3 = maclaurin_sinh(30,100)
    print maclaurin_sinh3
######################################################################"C:\python 
#1.54916726832
#0.868670961486
#0.547853473888
#####################################################################



    
