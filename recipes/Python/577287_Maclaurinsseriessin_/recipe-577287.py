#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_sin is a function to compute sin(x) using maclaurin series
and the interval of convergence is -inf < x < +inf 
sin(x) = x - x^3/3! + x^5/5! - x^7/7! ...........
"""

from math import *

def maclaurin_sin(value,k):
    """
    Compute maclaurin's series approximation for sin(x)
    """
    
    global first_value    
    first_value = 0.0

    #attempt to Approximate sin(x) for a given value    
    try:
        for item in xrange(1,k,4):
            next_value = (value*pi/180)**item/factorial(item)
            first_value += next_value
            
        for item in xrange(3,k,4):
            next_value = -1*(value*pi/180)**item/factorial(item)
            first_value += next_value
            
        return first_value
    
    #Raise TypeError if input is not a number
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_sin1 = maclaurin_sin(70,100)
    print maclaurin_sin1
    maclaurin_sin2 = maclaurin_sin(45,100)
    print maclaurin_sin2
    maclaurin_sin3 = maclaurin_sin(30,100)
    print maclaurin_sin3
#####################################################################
#"C:\python
#0.939692620786
#0.707106781187
#0.5
#####################################################################
