#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_cos is a function to compute cos(x) using maclaurin series
and the interval of convergence is -inf < x < +inf 
cos(x) = 1- x^2/2! + x^4/4! - x^6/6! ...........
"""

from math import *

def maclaurin_cos(value,k):
    """
    Compute maclaurin's series approximation for cos(x).
    """
    
    global first_value
    first_value = 0.0
    
    #attempt to Approximate cos(x) for a given value
    try:
        for item in xrange(0,k,4):
            next_value = (value*pi/180)**item/factorial(item)
            first_value += next_value
            
        for item in xrange(2,k,4):
            next_value = -1*(value*pi/180)**item/factorial(item)
            first_value += next_value
             
        return first_value

    #Raise TypeError if input is not a number
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_cos1 = maclaurin_cos(70,100)
    print maclaurin_cos1
    maclaurin_cos2 = maclaurin_cos(45,100)
    print maclaurin_cos2
    maclaurin_cos3 = maclaurin_cos(30,100)
    print maclaurin_cos3
#####################################################################
#"C:\python 
#0.342020143326
#0.707106781187
#0.866025403784    
#####################################################################
