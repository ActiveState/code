#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_series_one is a function to compute 1/1-x using maclaurin series
and the interval of convergence is -1 < x < 1 
1/x-1 = 1 + x + x^2 + x^3+ ...........
"""

def error(number):
    """ Raises interval of convergence error."""
    
    if number >= 1 or number <= -1 :
        raise TypeError,\
            "\n<The interval of convergence should be -1 < value < 1 \n"

def maclaurin_series_one(value, k):
    """
    Compute maclaurin's series approximation for 1/1-x
    """
    
    first_value = 0.0
    
    #attempt to Approximate 1/1-x for a given value
    try:
        error(value)
        for item in xrange(k):
            next_value = value**item
            first_value += next_value
       
        return first_value
    
    #Raise TypeError if input is not within the interval of convergence
    except TypeError, exception:
        print exception 

if __name__ == "__main__":
    
   print maclaurin_series_one(0.1,1000)
   print maclaurin_series_one(0.3,100)
   print maclaurin_series_one(0.7,100)
#####################################################################

#"C:\python
#1.11111111111
#1.42857142857
#3.33333333333
