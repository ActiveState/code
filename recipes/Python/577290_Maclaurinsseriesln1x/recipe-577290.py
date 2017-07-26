#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_ln is a function to compute ln(1+x) using maclaurin series
and the interval of convergence is -1 < x <= 1
ln(1+x) = x- x^2/2 +x^3/3 - x^4/4! + ...........
"""

from math import *

def error(number):
    """ Raises interval of convergence error."""
    
    if number > 1 or number <= -1 :
        raise TypeError,\
            "\n<The interval of convergence should be -1 < value <= 1 \n"

def maclaurin_ln(value,k):
    """
    Compute maclaurin's series approximation for ln(1+x).
    """
    
    global first_value    
    first_value = 0.0
    
    #attempt to Approximate ln(1+x) for a given value
    try:
        
        error(value)
        for item in xrange(1,k,2):
            next_value =(value**item)/float(item)
            first_value += next_value
            
        for item in xrange(2,k,2):
            next_value = -1*(value**item)/float(item)
            first_value += next_value
            
        return first_value

    #Raise TypeError if input is not within
    #the interval of convergence
    except TypeError,exception:
        print exception 



if __name__ == "__main__":
    
   macllaurin_ln1 =  maclaurin_ln(1,700000) # ln(2)
   print macllaurin_ln1
   macllaurin_ln2 =  maclaurin_ln(0.7,1000) 
   print macllaurin_ln2
   macllaurin_ln3 =  maclaurin_ln(0.3,1000) 
   print macllaurin_ln3

#####################################################################  
#"C:\python
#0.693147894846
#0.530628251062
#0.262364264467
#####################################################################
