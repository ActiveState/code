#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_cosh is a function to compute cosh(x) using maclaurin series
and the interval of convergence is -inf < x < +inf 
cosh(x) = 1+ x^2/2! + x^4/4! + x^6/6! ...........
"""

from math import *

def maclaurin_cosh(value, k):
    """
    Compute maclaurin's series approximation for cosh(x).
    """
    
    global first_value
    first_value = 0.0
    
    #attempt to Approximate cosh(x) for a given value
    try:
        for item in xrange(0,k,2):
            next_value =(value*pi/180)**item/factorial(item)
            first_value += next_value
             
        return first_value

    #Raise TypeError if input is not a number
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_cosh1 = maclaurin_cosh(70,100)
    print maclaurin_cosh1
    maclaurin_cosh2 = maclaurin_cosh(45,100)
    print maclaurin_cosh2
    maclaurin_cosh3 = maclaurin_cosh(30,100)
    print maclaurin_cosh3
######################################################################
#C:\python
#1.8438869882
#1.32460908925
#1.14023832108
