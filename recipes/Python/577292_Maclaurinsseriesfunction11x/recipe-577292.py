#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/07/10
#version :2.6

"""
maclaurin_series_two is a function to compute 1/1+x^2 using maclaurin series
and the interval of convergence is -1 < x < 1 
1/1+x^2 = 1 - x^2 + x^4- x^6 ...........
"""

def error_two(number):
    """ Raises interval of convergence error."""
    
    if number >= 1 or number <= -1 :
        raise TypeError,\
            "\n<The interval of convergence should be -1 < value < 1 \n"

def maclaurin_series_two(value, k):
    """
    Compute maclaurin's series approximation for 1/1+x^2
    """
    
    global first_value
    first_value = 0.0
    
    #attempt to Approximate 1/1+x^2 for a given value
    try:
        error_two(value)
        for item in xrange(0,k,4):
            next_value = value**item
            first_value += next_value
            
        for item in xrange(2,k,4):
            next_value = -1*(value**item)
            first_value += next_value
            
        return first_value
    
    #Raise TypeError if input is not within the interval of convergence
    except TypeError, exception:
        print exception 

if __name__ == "__main__":

   maclaurin_series1 = maclaurin_series_two(0.1,100)
   print maclaurin_series1
   maclaurin_series2 = maclaurin_series_two(0.3,100)
   print maclaurin_series2
   maclaurin_series3 = maclaurin_series_two(0.7,100)
   print maclaurin_series3 

###################################################################
#"C:\python 
#0.990099009901
#0.917431192661
#0.671140939597
