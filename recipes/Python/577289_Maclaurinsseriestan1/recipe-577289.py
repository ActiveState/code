#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_tan-1 is a function to compute tan-1(x) using maclaurin series
and the interval of convergence is -1 <= x <= +1
sin(x) = x - x^3/3 + x^5/5 - x^7/7 ...........
"""

from math import *

def error(number):
    """ Raises interval of convergence error."""
    
    if number > 1 or number < -1 :
        raise TypeError,\
            "\n<The interval of convergence should be -1 <= value <= 1 \n"

def maclaurin_cot(value, k):
    """
    Compute maclaurin's series approximation for tan-1(x)
    """
    global first_value    
    first_value = 0.0
    
    #attempt to Approximate tan-1(x) for a given value 
    try:
        error(value)
        for item in xrange(1,k,4):
            next_value = value**item/float(item)
            first_value += next_value
            
        for arg in range(3,k,4):
            next_value = -1* value **arg/float(arg)
            first_value += next_value
            
        return round(first_value*180/pi,2)
    
    #Raise TypeError if input is not within
    #the interval of convergence
    except TypeError,exception:
        print exception 

if __name__ == "__main__":
    
    maclaurin_cot1 = maclaurin_cot(0.305730681,100)
    print maclaurin_cot1
    maclaurin_cot2 = maclaurin_cot(0.75355405,100)
    print maclaurin_cot2
    maclaurin_cot3 = maclaurin_cot(0.577350269,100)
    print maclaurin_cot3
#################################################################
#"C:\python
#17.0
#37.0
#30.0
