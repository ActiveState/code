#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 03/08/10
#version :2.6

"""
maclaurin_cos_pow2 is a function to compute cos(x) using maclaurin series
and the interval of convergence is -inf < x < +inf 
cos²(x) = 1- x^2 + 2^3*x^4/4! - 2^5*x^6/6! ...........
"""

from math import *

def maclaurin_cos_pow2(value,k):
    """
    Compute maclaurin's series approximation for cos^2(x).
    """
    
    global first_value
    first_value = 0.0
    
    #attempt to Approximate cos^2(x) for a given value
    try:
        for item in xrange(4,k,4):
            next_value = (2**(item-1))*(value*pi/180)**item/factorial(item)
            first_value += next_value
            
        for item in xrange(2,k,4):
            next_value = -1*(2**(item-1))*((value*pi/180)**item/factorial(item))
            first_value += next_value
             
        return first_value +1

    #Raise TypeError if input is not a number
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_cos1 = maclaurin_cos_pow2(135,100)
    print maclaurin_cos1
    maclaurin_cos2 = maclaurin_cos_pow2(45,100)
    print maclaurin_cos2
    maclaurin_cos3 = maclaurin_cos_pow2(30,100)
    print maclaurin_cos3

    
#############################################################

#FT python "C:
#0.5
#0.5
#0.75
