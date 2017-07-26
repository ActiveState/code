#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 21/09/10
#version :2.6

"""
maclaurin_tanh-1 is a function to compute tanh-1(x) using maclaurin series
and the interval of convergence is -1 < x < +1 and -inf < y < +inf
tanh-1(y) = ln(1+y/1-y)/2 and y = 1+x/1-x
tanh-1(y) = x + x^3/3 + x^5/5 + x^7/7 ...........)
"""



def maclaurin_coth(value, k):
    """
    Compute maclaurin's series approximation for tanh-1(value).
    """
 
    global first_value    
    first_value = 0.0
    
    #attempt to Approximate tanh-1(x) for a given value    
    try:
        value_y =float((1+value  )/(1-value))
        value_x = (value_y -1)/float(value_y + 1)
        for item in xrange(1,k,2):
            next_value = value_x **item/item
            first_value += next_value

        return first_value
    
    #Raise TypeError if input is not a number   
    except TypeError:
        print 'Please enter an integer or a float value'

if __name__ == "__main__":
    
    maclaurin_coth_1 = maclaurin_coth(0.3,100)
    print maclaurin_coth_1
    maclaurin_coth_2 = maclaurin_coth(0.5,100)
    print maclaurin_coth_2
    maclaurin_coth_3 = maclaurin_coth(0.7,100)
    print maclaurin_coth_3  

#####################################################################

#FT python "C:

#0.309519604203
#0.549306144334
#0.867300527694

  
