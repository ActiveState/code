#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date :  15/07/10
#version :2.6

from decimal import Decimal as D,Context, localcontext

def maclaurin_ln(value, k):
    """
    Compute maclaurin's series approximation for ln(value).
    """

    first_value = 0
    
    #attempt to Approximate ln(x) for a given value    
    try:
        value_x = (value - D("1.0"))/(value + D("1.0"))
        for item in xrange(1,k,2):
            next_value = value_x**item/item
            first_value += next_value
            
        return 2*(first_value)
    
    #Raise TypeError if input is not a number   
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    with localcontext(Context(prec=67)):
        for arg in xrange(7,28,10):
            print "ln(%s) = %s " %\
            (arg, maclaurin_ln(arg,D("10000")))
    
#######################################################################

#FT  "C:\Maclaurin_lndecimal1.py"
#ln(7) = 1.945910149055313305105352743443179729637084729581861188459390149937
#ln(17) = 2.833213344056216080249534617873126535588203012585744787297237737878
#ln(27) = 3.295836866004329074185735710767577113942471673468248355204083000896
##########################################################################################

Version : Python 3.2

#from decimal import Decimal as D

#from decimal import *
#from math import *

#def maclaurin_ln(value, k):
#    """
#    Compute maclaurin's series approximation for ln(value).
#    """
    
#    global first_value    
#    first_value = 0
#    
#    #attempt to Approximate ln(x) for a given value    
#    try:
#        value_x = (value - 1)/(value + 1)
#        for item in range(1,k,2):
#            next_value = value_x**item/item
#            first_value += next_value
#            
#        return 2* first_value
#    
#    #Raise TypeError if input is not a number   
#    except TypeError:
#        print('Please enter an integer or a float value')
#if __name__ == "__main__":
#
#   
#    with localcontext(Context(prec=170)):
#        for arg in range(7,28,10):
#            print("ln(%s) = %s " %\
#            (arg, maclaurin_ln(D(arg),10000)))
#    getcontext().prec = 17
#    for arg in range(7,28,10):
#       
#        print("ln(%s) = %s " %\
#        (arg, maclaurin_ln(D(arg),10000)))
