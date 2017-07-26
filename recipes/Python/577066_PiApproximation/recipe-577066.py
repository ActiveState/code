#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 23/02/10
#version :2.6

"""
Pi_approximation uses the subinterval_length function and return
its value and yield all the points values while using the subinterval_point
function and Pi function compute Pi approximation with 16 decimal places
the greater the value of the number the more precise is Pi value 
"""

class Pi_Approximation(object):
    """
    Class that represent Pi approximation
    """
    def __init__(self, number):
        """
        Pi_Approximation constructor takes the number constant
        """
        self.number = number
        
    def subinterval_length(self):
        """
        Compute subinterval_length 
        """
        sub_length = 2/float(self.number)
        return sub_length
    
    def subinterval_point(self):
        """
        Compute the value of each point 
        """

        #attempt to yield all the Xk points values using the subinterval_point        
        try:
            for item in range(1,self.number + 1):
                sub_point = -1 + ((item - 1/2.0)* Pi_Approximation.subinterval_length(self))
                yield sub_point
        
        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"
    
    def Pi(self):
        """
        Computing Pi value.
        """

        #attempt to Approximate Pi for a given value        
        try:
 
            my_sum = 0    #Set my_sum to 0
            
            # using subinterval_point function to compute Pi approximation.
            # the greater the value of the number the more accurate result
            for self.point in Pi_Approximation.subinterval_point(self):
            
                self.pi_X = pow((1-self.point**2),0.5)
                my_sum += self.pi_X
                pi = (my_sum * Pi_Approximation.subinterval_length(self))*2
                yield repr(pi)
                
        #Raise TypeError if input is not numerical
        except TypeError:
            print  "\n<The entered value is not a number" 

if __name__ == '__main__':
    for arg in xrange(600000,2700000,300000):
    
        pi = Pi_Approximation(arg)
        for i in pi.Pi():
            pass
        print i

#######################################################################
# FT python "C:\Users\Pi1.py"
#
# 3.1415926556860203
# 3.1415926547308004
# 3.1415926543309367
# 3.1415926541200871
# 3.1415926539930723
# 3.141592653909842
# 3.14159265385199

#######################################################################
