#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_binomial is a function to compute(1+x)^m using maclaurin
binomial series and the interval of convergence is -1 < x < 1
(1+x)^m = 1 + mx + m(m-1)x^2/2! + m(m-1)(m-2)x^3/3!...........
note: if m is a nonegative integer the binomial is a polynomial of
degree m and it is valid on -inf < x < +inf,thus, the error function
will not be valid. 
"""

from math import *

def error(number):
    """ Raises interval of convergence error."""
    
    if number >= 1 or number <= -1 :
        raise TypeError,\
            "\n<The interval of convergence should be -1 < value < 1 \n"
    
  

def maclaurin_binomial(value,m,k):
    """
    Compute maclaurin's binomial series approximation for (1+x)^m.
    """
    global first_value
    first_value = 0.0
    error(value)

    #attempt to Approximate (1+x)^m for given values 
    try:
        
        for item in xrange(1,k):
            next_value =m*(value**item)/factorial(item)
            
            for i in range(2,item+1):              
                next_second_value =(m-i+1)
                next_value *= next_second_value
            first_value += next_value

        return first_value + 1
    
    #Raise TypeError if input is not within
    #the interval of convergence
    except TypeError,exception:
        print exception

    #Raise OverflowError if an over flow occur 
    except OverflowError:
        print '\n<Please enter a lower k value to avoid the Over flow\n '


if __name__ == "__main__":
    maclaurin_binomial_1 = maclaurin_binomial(0.777,-0.5,171)
    print maclaurin_binomial_1 
    maclaurin_binomial_2 = maclaurin_binomial(0.37,0.5,171)
    print maclaurin_binomial_2
    maclaurin_binomial_3 = maclaurin_binomial(0.3,0.717,171)
    print maclaurin_binomial_3 


########################################################################
#c:python 
#
#0.750164116353
#1.17046999107
#1.20697252357
#######################################################################
#Version : Python 3.2 

#import math
    
#def maclaurin_binomial(value,m,k):
#    """
#    Compute maclaurin's binomial series approximation for (1+x)^m.
#    """
#    global first_value
#    first_value = 0.0
#    
#    #attempt to Approximate (1+x)^m for given values 
#    try:
#        
#        for item in range(1,k):
#            next_value =m*(value**item)/math.factorial(item)
#            
#            for i in range(2,item+1):              
#                next_second_value =(m-i+1)
#                next_value *= next_second_value
#            first_value += next_value

#        return first_value + 1
#    
#    #Raise TypeError if input is not within
#    #the interval of convergence
#    except TypeError as exception:
#        print (exception)
#
#    #Raise OverflowError if an over flow occur 
#    except OverflowError:
#        print ('\n<Please enter a lower k value to avoid the Over flow\n ')
#
#
#if __name__ == "__main__":
#    maclaurin_binomial_1 = maclaurin_binomial(0.777,-0.5,171)
#    print (maclaurin_binomial_1 )
#    maclaurin_binomial_2 = maclaurin_binomial(0.37,0.5,171)
#    print (maclaurin_binomial_2)
#    maclaurin_binomial_3 = maclaurin_binomial(0.3,0.717,171)
#    print (maclaurin_binomial_3)
######################################################################################

#decimal Version Python 3.2 

#from math import *
#from decimal import Decimal as D,Context, localcontext
#def error(number):
#    """ Raises interval of convergence error."""

#    if number >= 1 or number <= -1 :
#        raise TypeError("\n<The interval of convergence should be -1 < value < 1 \n")



#def maclaurin_binomial(value,m,k):
#    """
#    Compute maclaurin's binomial series approximation for (1+x)^m.
#    """
#    global first_value
#    first_value = 0
#
#    #attempt to Approximate (1+x)^m for given values
#    try:
#
#        for item in range(1,k):
#            next_value = (m*(value**item))/factorial(item)

#            for i in range(2,item+1):
#                next_second_value =(m-i+1)
#                next_value *= next_second_value
#            first_value += next_value
#
#        return (first_value) + (1)
#
#    #Raise TypeError if input is not within
#    #the interval of convergence
#    except TypeError as exception:
#        print(exception)
#
#    #Raise OverflowError if an over flow occur
#    except OverflowError:
#        print('\n<Please enter a lower k value to avoid the Over flow\n ')
#
#
#if __name__ == "__main__":
#
#    with localcontext(Context(prec= 1777)):
#        for arg in range(2,-8,-2):
#            print(maclaurin_binomial(D("0.777"),arg,171))
