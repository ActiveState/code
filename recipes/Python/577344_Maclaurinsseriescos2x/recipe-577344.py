#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 03/008/10
#version :2.6

"""
maclaurin_cos_2x is a function to compute cos(x) using maclaurin series
and the interval of convergence is -inf < x < +inf 
cos(2x) = 1- 2^2*x^2/2! + 2^4*x^4/4! - 2^6*x^6/6! ...........
"""

from math import *

def maclaurin_cos_2x(value,k):
    """
    Compute maclaurin's series approximation for cos(2x).
    """
    
    global first_value
    first_value = 0.0
    
    #attempt to Approximate cos(2x) for a given value
    try:
        for item in xrange(4,k,4):
            next_value = (2**item)*(value*pi/180)**item/factorial(item)
            first_value += next_value
            
        for item in xrange(2,k,4):
            next_value = -1*(2**item)*(value*pi/180)**item/factorial(item)
            first_value += next_value
             
        return first_value +1

    #Raise TypeError if input is not a number
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_cos_2x_1 = maclaurin_cos_2x(60,100)
    print maclaurin_cos_2x_1
    maclaurin_cos_2x_2 = maclaurin_cos_2x(45,100)
    print maclaurin_cos_2x_2
    maclaurin_cos_2x_3 = maclaurin_cos_2x(30,100)
    print maclaurin_cos_2x_3

 ######################################################################FT python "C:\
#urine series\M
#-0.5
#0.0
#0.5
 
