#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 09/09/09
#version :2.6.1

"""
Class Interval is the base class for every Rectangle Method's approximation
and inherits from tuple. However four main functions are defined within
Interval, delta_X, and the three different approximation's methods, the
leftEndPoint, the rightEndPoint, and the midPoint. Though, RectangleMethod
class inherits from Interval class, and call the three approximation's
methods to approximate a curve function y = f(x) and compare those methods'
results. And I chose the midPoint method to compute my ell_en and logarithm
functions.

"""

from collections import namedtuple

class Interval(namedtuple('Interval','n,a,b')):
    """
    Interval class inherits from tuple
    """

    #set __slots__ to an empty tuple keep memory requirements low    
    __slots__ = ()
    
    @property
    def delta_X(self):
        """
        Compute Delta_X the length value of each part of the
        subinterval[a,b] divided into n equal parts
        """

        return (self.b - self.a )/float(self.n)

    @property
    def leftEndPoint(self):
        """
        Compute the value of Xk of each point using the
        left endpoint of each subinterval
        """
        
        # Start with an empty list
        left_list = []

        #attempt to create a list of Xk points using the left endpoint
        try:
            for k in range(1,self.n+1):
                left_end_point = self.a + (k - 1)* self.delta_X
                left_list.append(left_end_point)
            return left_list
        
        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"
            
    @property
    def rightEndPoint(self):
        """
        Compute the value of Xk of each point using the
        right endpoint of each subinterval
        """
        
        # Start with an empty list
        right_list = []
        
        #attempt to create a list of Xk points using the right endpoint       
        try:
            for k in range(1,(self.n +1)):
                right_end_point = self.a + (k * self.delta_X)
                right_list.append(right_end_point)
            return right_list     

        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"
            
    @property
    def midPoint(self):
        """
        Compute the value of Xk of each point using the midPoint
        of each subinterval
        """

        # Start with an empty list
        mid_list = []

        #attempt to create a list of Xk points using the midPoint        
        try:
            for k in range(1,self.n + 1):
                mid_point = self.a + ((k - 1/2.0)* self.delta_X)
                mid_list.append(mid_point)
            return mid_list
        
        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"

class RectangleMethod(Interval):
    """
    Class RectangleMethod inherit from Interval class  
    """
    def Curve(self,**args):
        """
        Compute and display the Left Endpoint, the Right Endpoint
        and the midPoint approximaions of the area under a curve y = f(x)
        over an interval [a,b]
        """
        
        self.args = args
        
        count = 0   #Set count to 0
        total = 0   #Set total to 0
        
        print '\n\t\tLeft Endpoint Approximation'
        print '\t\t----------------------------'
        print '\nk\t\tX_k\t\ty','\n'
        
        # the curve y = f(x) is set to the 3rd degree of a form a + X**n
        # could be switched into higher degree or trigonometric functions
        for self.X_k in self.leftEndPoint:      
            self.left_curve = "%2.6f" % (self.args.get('a')*(float(self.X_k)**3)\
                                + self.args.get('b') *(float(self.X_k)**2)\
                                + self.args.get('c')*(float(self.X_k))+ self.args.get('d'))
            count +=1
            total += float(self.left_curve)
            
            print count,'\t\t',"%2.2f" % self.X_k,'\t\t',self.left_curve

        print '\t\t\t\t--------'
        print '\t\t\t\t',total
        print '\t\t\t\t--------'
        print 'left endpoint Approximation  =  %s' % (self.delta_X*total)
        print
        
        count_1 = 0 #Set count_1 to 0
        total_1 = 0 #Set total_1 to 0
        
        print '\n\t\tRight Endpoint Approximation'
        print '\t\t----------------------------'
        print '\nk\t\tX_k\t\ty','\n'
        
        for self.X_k in self.rightEndPoint:      
            self.right_curve = "%2.6f" % (self.args.get('a')*(float(self.X_k)**3)\
                                + self.args.get('b') *(float(self.X_k)**2)\
                             + self.args.get('c')*(float(self.X_k))+ self.args.get('d'))
            count_1 +=1
            total_1 += float(self.right_curve)
            
            print count_1,'\t\t',"%2.2f" % self.X_k,'\t\t',self.right_curve

        print '\t\t\t\t--------'
        print '\t\t\t\t',total_1
        print '\t\t\t\t--------'
        print 'right endpoint Approximation =  %s' % (self.delta_X*total_1)
        print
        
        count_2 = 0 #Set count_2 to 0
        total_2 = 0 #Set total_2 to 0
        
        print '\n\t\tMidpoint Approximation'
        print '\t\t----------------------'
        print '\nk\t\tX_k\t\ty','\n'
      
        for self.X_k in self.midPoint:      
            self.mid_curve = "%2.6f" % (self.args.get('a')*(float(self.X_k)**3)\
                            + self.args.get('b') *(float(self.X_k)**2)\
                         + self.args.get('c')*(float(self.X_k))+ self.args.get('d'))
            count_2 +=1
            total_2 += float(self.mid_curve)
            
            print count_2,'\t\t',"%2.2f" % self.X_k,'\t\t',self.mid_curve

        print '\t\t\t\t--------'
        print '\t\t\t\t',total_2
        print '\t\t\t\t--------'
        print '      midPoint Approximation =  %s' % (self.delta_X*total_2)

    def ell_en(self,number):
        """
        Computing ellen(ln) Approximation  for a given value.
        """
        
        self.number = number

        #attempt to Approximate In for a given value        
        try:
            #Set RectangleMethod n and a fields to constant values
            #and b field to a variable value, the greater the value of n
            # the more accurate the result 
            rectangleMethod = RectangleMethod(n = 100000,a = 1, b=self.number)
        
            sum_next = 0    #Set sum_next to 0
            
            #inheriting and using midPoint function from Interval class
            #to compute ln approximation.
            for self.X_k in rectangleMethod.midPoint:
            
                self.ell_en_X = 1/self.X_k
                sum_next += self.ell_en_X
                In = (sum_next * rectangleMethod.delta_X )
                yield In
                
        #Raise TypeError if input is not numerical
        except TypeError:
            print  "\n<The entered value is not a number"           
        
    def logarithm(self,base,value):
        """
        Computing logarithm approximation for a given value
        and a base of choice
        """
       
        self.base = base
        self.value = value
        
        #attempt to Approximate logarithm for a given base and value
        try:
            
            for i in self.ell_en(self.value):
                pass
            for j in self.ell_en(self.base):
                pass 
                result = round(i/j,8)
            
            return "log_b%s(%s) = : %s " % (self.base,self.value,result)

        #Raise TypeError if input is not numerical
        except TypeError:
            print  "\n<The entered value is not a number"

    def exponential(self,value):
        """
        Compute exponential e and exp(value) for a given value 
        """
        
        self.value = value
        
        #attempt to yield an approximation of exp(n) for a given value
        try:
            for k in (1,100000000):
                exp = ((1+1.0/k)**k)**value
                yield exp
            
            if self.value == 1:
                print "e = %s " % repr(exp)
            else:
                print "exp(%s) = %s " % (value,repr(exp))
                
        #Raise TypeError if input is not numerical               
        except TypeError:
            print "Please enter a number "
            
            
if __name__ == '__main__':
     
    # Create object of class RectangleMethod 
    rectangleMethod = RectangleMethod('n','a','b')

    # create a curve y = 27 - X**2 over interval [0,3] with n =10
    # for a better accuracy increase the value of n, n = 20, n = 30 ... 
    curve = RectangleMethod(10,0,3)
    curve.Curve(a=0,b=-1,c=0,d=27)

    # Create an object of ell_en to compute ln(x)    
    rectangleMethod = rectangleMethod._replace(b = 5)
    ellen = rectangleMethod.ell_en(rectangleMethod.b)
    for item in ellen:
        pass
    print '\n\t\tNatural Logarithm Approximation'
    print '\t\t-------------------------------\n'     
    print "In(%s) = : %s " % (getattr(rectangleMethod,'b'),item)    
    

    # Create an object of logarithm ( base and value)    
    log_base_x = rectangleMethod.logarithm(2,16)
    print '\n\t\tCommon Logarithm Approximation'
    print '\t\t-------------------------------\n'    
    print log_base_x
    
    # Create an object of exponential ( value )
    print '\n\t\tExponential Approximation'
    print '\t\t-------------------------\n'    
    for i in rectangleMethod.exponential(1):
        pass




#C:\Windows\system32>python "C:\programs\Rectangle_Method.py"

#                Left Endpoint Approximation
#                ----------------------------

#k               X_k             y

#1               0.00            27.000000
#2               0.30            26.910000
#3               0.60            26.640000
#4               0.90            26.190000
#5               1.20            25.560000
#6               1.50            24.750000
#7               1.80            23.760000
#8               2.10            22.590000
#9               2.40            21.240000
#10              2.70            19.710000
#                                --------
#                                244.35
#                                --------
#left endpoint Approximation  =  73.305
#
#
#                Right Endpoint Approximation
#                ----------------------------
#
#k               X_k             y
#
#1               0.30            26.910000
#2               0.60            26.640000
#3               0.90            26.190000
#4               1.20            25.560000
#5               1.50            24.750000
#6               1.80            23.760000
#7               2.10            22.590000
#8               2.40            21.240000
#9               2.70            19.710000
#10              3.00            18.000000
#                                --------
#                                235.35
#                                --------
#right endpoint Approximation =  70.605
#
#
#                Midpoint Approximation
#                ----------------------
#
#k               X_k             y
#
#1               0.15            26.977500
#2               0.45            26.797500
#3               0.75            26.437500
#4               1.05            25.897500
#5               1.35            25.177500
#6               1.65            24.277500
#7               1.95            23.197500
#8               2.25            21.937500
#9               2.55            20.497500
#10              2.85            18.877500
#                                --------
#                                240.075
#                                --------
#      midPoint Approximation =  72.0225
#
#                Natural Logarithm Approximation
#                -------------------------------
#
#In(5) = : 1.60943791237
#
#                Common Logarithm Approximation
#                -------------------------------
#
#log_b2(16) = : 4.0
#
#                Exponential Approximation
#                -------------------------
#
#e = 2.7182817983473577
#    
#        
#  
    
##########################################################################################
# Version : Python 3.2
#from collections import namedtuple

#class Interval(namedtuple('Interval','n,a,b')):
#    """
#    Interval class inherits from tuple
#    """
#
#    #set __slots__ to an empty tuple keep memory requirements low    
#    __slots__ = ()
#    
#    @property
#    def delta_X(self):
#        """
#        Compute Delta_X the length value of each part of the
#        subinterval[a,b] divided into n equal parts
#        """
#
#        return (self.b - self.a )/float(self.n)
#
#    @property
#    def leftEndPoint(self):
#        """
#        Compute the value of Xk of each point using the
#        left endpoint of each subinterval
#        """
#        
#        # Start with an empty list
#        left_list = []
#
#        #attempt to create a list of Xk points using the left endpoint
#        try:
#            for k in range(1,self.n+1):
#                left_end_point = self.a + (k - 1)* self.delta_X
#                left_list.append(left_end_point)
#            return left_list
#        
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#            
#    @property
#    def rightEndPoint(self):
#        """
#        Compute the value of Xk of each point using the
#        right endpoint of each subinterval
#        """
#        
#        # Start with an empty list
#        right_list = []
#        
#        #attempt to create a list of Xk points using the right endpoint       
#        try:
#            for k in range(1,(self.n +1)):
#                right_end_point = self.a + (k * self.delta_X)
#                right_list.append(right_end_point)
#            return right_list     
#
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#            
#    @property
#    def midPoint(self):
#        """
#        Compute the value of Xk of each point using the midPoint
#        of each subinterval
#        """
#
#        # Start with an empty list
#        mid_list = []
#
#        #attempt to create a list of Xk points using the midPoint        
#        try:
#            for k in range(1,self.n + 1):
#                mid_point = self.a + ((k - 1/2.0)* self.delta_X)
#                mid_list.append(mid_point)
#            return mid_list
#        
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#
#class RectangleMethod(Interval):
#    """
#    Class RectangleMethod inherit from Interval class  
#    """
#    def Curve(self,**args):
#        """
#        Compute and display the Left Endpoint, the Right Endpoint
#        and the midPoint approximaions of the area under a curve y = f(x)
#        over an interval [a,b]
#        """
#        
#        self.args = args
#        
#        count = 0   #Set count to 0
#        total = 0   #Set total to 0
#        
#        print('\n\t\tLeft Endpoint Approximation')
#        print('\t\t----------------------------')
#        print('\nk\t\tX_k\t\ty','\n')
#        
#        # the curve y = f(x) is set to the 3rd degree of a form a + X**n
#        # could be switched into higher degree or trigonometric functions
#        for self.X_k in self.leftEndPoint:      
#            self.left_curve = "%2.6f" % (self.args.get('a')*(float(self.X_k)**3)\
#                                + self.args.get('b') *(float(self.X_k)**2)\
#                                + self.args.get('c')*(float(self.X_k))+ self.args.get #('d'))
#            count +=1
#            total += float(self.left_curve)
#            
#            print(count,'\t\t',"%2.2f" % self.X_k,'\t\t',self.left_curve)
#
#        print('\t\t\t\t--------')
#        print('\t\t\t\t',total)
#        print('\t\t\t\t--------')
#        print('left endpoint Approximation  =  %s' % (self.delta_X*total))
#        print()
#        
#        count_1 = 0 #Set count_1 to 0
#        total_1 = 0 #Set total_1 to 0
#        
#        print('\n\t\tRight Endpoint Approximation')
#        print('\t\t----------------------------')
#        print('\nk\t\tX_k\t\ty','\n')
#        
#        for self.X_k in self.rightEndPoint:      
#            self.right_curve = "%2.6f" % (self.args.get('a')*(float(self.X_k)**3)\
#                                + self.args.get('b') *(float(self.X_k)**2)\
#                             + self.args.get('c')*(float(self.X_k))+ self.args.get('d'))
#            count_1 +=1
#            total_1 += float(self.right_curve)
#            
#            print(count_1,'\t\t',"%2.2f" % self.X_k,'\t\t',self.right_curve)
#        print('\t\t\t\t--------')
#        print('\t\t\t\t',total_1)
#        print('\t\t\t\t--------')
#        print('right endpoint Approximation =  %s' % (self.delta_X*total_1))
#        print()
#        
#        count_2 = 0 #Set count_2 to 0
#        total_2 = 0 #Set total_2 to 0
#        
#        print('\n\t\tMidpoint Approximation')
#        print('\t\t----------------------')
#        print('\nk\t\tX_k\t\ty','\n')
#      
#        for self.X_k in self.midPoint:      
#            self.mid_curve = "%2.6f" % (self.args.get('a')*(float(self.X_k)**3)\
#                            + self.args.get('b') *(float(self.X_k)**2)\
#                         + self.args.get('c')*(float(self.X_k))+ self.args.get('d'))
#            count_2 +=1
#            total_2 += float(self.mid_curve)
#            
#            print(count_2,'\t\t',"%2.2f" % self.X_k,'\t\t',self.mid_curve)
#
#        print('\t\t\t\t--------')
#        print('\t\t\t\t',total_2)
#        print('\t\t\t\t--------')
#        print('      midPoint Approximation =  %s' % (self.delta_X*total_2))
#
#    def ell_en(self,number):
#        """
#        Computing ellen(ln) Approximation  for a given value.
#        """
#        
#        self.number = number
#
#        #attempt to Approximate In for a given value        
#        try:
#            #Set RectangleMethod n and a fields to constant values
#            #and b field to a variable value, the greater n value the
#            # the more accurate result 
#            rectangleMethod = RectangleMethod(n = 100000,a = 1, b=self.number)
#        
#            sum_next = 0    #Set sum_next to 0
#            
#            #inheriting and using midPoint function from Interval class
#            #to compute ln approximation.
#            for self.X_k in rectangleMethod.midPoint:
#            
#                self.ell_en_X = 1/self.X_k
#                sum_next += self.ell_en_X
#                In = (sum_next * rectangleMethod.delta_X )
#                yield In
#                
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")           
#        
#    def logarithm(self,base,value):
#        """
#        Computing logarithm approximation for a given value
#        and a base of choice
#        """
#       
#        self.base = base
#        self.value = value
#
#        #attempt to Approximate logarithm for a given base and value
#        try:
#            
#            for i in self.ell_en(self.value):
#                pass
#            for j in self.ell_en(self.base):
#                pass 
#                result = round(i/j,8)
#            
#          return "log_b%s(%s) = : %s " % (self.base,self.value,result)
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#
#    def exponential(self,value):
#        """
#        Compute exponential e and exp(value) for a given value 
#        """
#        
#        self.value = value
#        
#        #attempt to yield an approximation of exp(n) for a given value
#        try:
#            for k in (1,100000000):
#                exp = ((1+1.0/k)**k)**value
#                yield exp
#            
#            if self.value == 1:
#                print("e = %s " % repr(exp))
#            else:
#                print("exp(%s) = %s " % (value,repr(exp)))
#                
#        #Raise TypeError if input is not numerical               
#        except TypeError:
#            print("Please enter a number ")
#
