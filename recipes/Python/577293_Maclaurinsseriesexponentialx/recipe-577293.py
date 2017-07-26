#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_expenantial is a function to compute e^x using maclaurin series
and the interval of convergence is -inf < x < + inf 
e^x = 1 + x + x^2/2! + x^3/3! + x^4/4! ...........
"""
from math import *

def maclaurin_expenantial(value, k):
    """
    Compute maclaurin's series approximation for e^x

    """
    
    first_value = 0.0
    
    #attempt to Approximate e^x for a given value
    try:
        for item in xrange(k):
            next_value = float(value**item)/factorial(item)
            first_value += next_value

        return first_value

    #Raise TypeError if input is not a number     
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
   maclaurin_exp1 =  maclaurin_expenantial(1,100)
   print maclaurin_exp1
   maclaurin_exp2 =  maclaurin_expenantial(3,100)
   print maclaurin_exp2
   maclaurin_exp3 = maclaurin_expenantial(7,100)
   print maclaurin_exp3

#####################################################################
#"C:python
#urine series\
#2.71828182846
#20.0855369232
#1096.63315843
#####################################################################
