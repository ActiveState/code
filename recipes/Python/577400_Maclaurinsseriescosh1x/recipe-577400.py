#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 21/09/10
#version :2.6

"""
maclaurin_cosh-1 is a function to compute cosh-1(x) using maclaurin series
and the interval of convergence is -1 < x < +1 and -inf < y < +inf
cosh-1(y) = ln(y + sqrt(y**2 -1) and y = ln(1+x/1-x)
cosh-1(y) = 2(x + x^3/3 + x^5/5 + x^7/7 ......)
"""

from math import *

def maclaurin_cosh_inverse(value, k):
    """
    Compute maclaurin's series approximation for cosh-1(value).
    """
 
    global first_value    
    first_value = 0.0
    
    #attempt to Approximate cosh-1(x) for a given value    
    try:
        value_y = value + sqrt(value**2-1)
        value_x = (value_y -1)/float(value_y + 1)
        for item in xrange(1,k,2):
            next_value = value_x **item/item
            first_value += next_value

        return 2*(first_value)
    
    #Raise TypeError if input is not a number   
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_cosh_inverse1 = maclaurin_cosh_inverse(3,100)
    print maclaurin_cosh_inverse1
    maclaurin_cosh_inverse2 = maclaurin_cosh_inverse(5,100)
    print maclaurin_cosh_inverse2
    maclaurin_cosh_inverse3 = maclaurin_cosh_inverse(7,100)
    print maclaurin_cosh_inverse3
    
#####################################################################

#FT python "C:
#1.76274717404
#2.29243166949
#2.63391575704
