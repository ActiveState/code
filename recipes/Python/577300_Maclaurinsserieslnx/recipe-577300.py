#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 10/07/10
#version :2.6

"""
maclaurin_ln is a function to compute ln(x) using maclaurin series
and the interval of convergence is -1 < x < +1
ln(y) = ln(1+x/1-x)= 2(x + x^3/3 + x^5/5 + x^7/7 ...........)
"""


def maclaurin_ln(value, k):
    """
    Compute maclaurin's series approximation for ln(value).
    """
        
    first_value = 0.0
    
    #attempt to Approximate ln(x) for a given value    
    try:
        value_x = (value - 1)/float(value + 1)
        for item in xrange(1,k,2):
            next_value = value_x **item/item
            first_value += next_value
            
        return 2*(first_value)
    
    #Raise TypeError if input is not a number   
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_ln_1 = maclaurin_ln(2,100)
    print maclaurin_ln_1
    maclaurin_ln_2 = maclaurin_ln(5,100)
    print maclaurin_ln_2
    maclaurin_ln_3 = maclaurin_ln(777,10000)
    print maclaurin_ln_3
    print 
    for arg in xrange(7,28,10):
        print "ln(%s) = %s " %\
        (arg, maclaurin_ln(arg,10000))
###########################################################################

#"C: python \Maclaurin_ln
#0.69314718056
#1.60943791243
#6.65544035037

#ln(7) = 1.94591014906
#ln(17) = 2.83321334406
#ln(27) = 3.295836866
