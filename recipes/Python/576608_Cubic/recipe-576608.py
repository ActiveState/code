#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 10/01/09
#version :2.4

"""Solving polynomial equations involve using long and synthetic division.
I applied in my program Cubic.py, however, the synthetic division.
Finding the integers and rational zeros (a) of a polynomial p(x), if any,
shows us that (x - a)s are factors of p(x) and p(x)/(x - a) = q(x)
therefore p(x) can be written p(x) = (x - a)q(x)"""


from Quadratic import *

class Cubic(object):
    """ Class that represent a Cubic Polynomial Equation
    with a,b,c,d properties"""

    def __init__(self,a,b,c,d):
        """ Cubic constructor takes a,b,c,d coefficients """
        
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d
        
        self.signb = self._checkSign(self.__b)
        self.signc = self._checkSign(self.__c)
        self.signd = self._checkSign(self.__d)
  
    def __str__(self):
        """ String representation of Cubic Polynomial Equation"""
        
        try:
            self.c1 = Cubic.syntheticDivision(self)[0]
            self.c2 = Cubic.syntheticDivision(self)[1]
            if self.c1 == float and self.c2 == float:
                self.c3 ="-"
                self.c4 ="+"
            else :
                self.c3 = self._checkSign(float(Cubic.syntheticDivision(self)[0])*-1)
                self.c4 = self._checkSign(float(Cubic.syntheticDivision(self)[1])*-1)
                

            if self.__d == 0:
                return "\n<Cubic Equation: p(x) = %sx%s %s %sx%s %s %sx = 0 \n \
                        \n<The linear factorization : p(x) = %sx(x%s%s)(x%s%s) \n\
                        " % (self.__a,chr(252),self.signb,self.__b,chr(253),
                        self.signc,self.__c,self.__a,self.c3,-1*float(self.c1),
                        self.c4,-1*float(self.c2))
        
            else :
                if self.__a == 1:
                    for i in Cubic.integerZero(self):
                        if (((self.__a*(i**3)) + (self.__b*(i**2))+ (self.__c*i )+ self.__d == 0)
                            and float(i) != float(self.c2) and float(i) != float(self.c1)):
                            return "\n<Cubic Equation: p(x) = %sx%s %s %sx%s %s %sx %s %s = 0 \
                                    \n\n<The integers zeros  are :\n\n%s\n \
                                    \n<The linear factorization : p(x) = (x%s%s)(x%s%s)(x%s%s) \n\
                                    " % (self.__a,chr(252),self.signb,self.__b,chr(253),self.signc,
                                    self.__c,self.signd,self.__d,Cubic.integerZero(self),self.c3,
                                    -1*float(self.c1),self.c4,-1*float(self.c2),(self._checkSign(-1*i)),-1*i)
                       
                    return "\n<None of the integers zeros %s \n\n checks p(x) = %sx%s %s %sx%s %s %sx %s %s = 0\n\n " \
                            % (Cubic.integerZero(self),self.__a,chr(252),self.signb,self.__b,chr(253),self.signc,self.__c,
                                self.signd,self.__d)
        
                else :
                    for j in Cubic.nonintegersRationalZero(self)[1]:
                        if ((self.__a*(float(str(j))**3)) + (self.__b*(float(str(j))**2))+
                            (self.__c*float(str(j)) )+ self.__d == 0.00):
                            return "\n<Cubic Equation: p(x) = %sx%s %s %sx%s %s %sx %s %s = 0 \
                                \n\n<The integers Zeros are :\n\n %s \
                                \n\n<The nonintegers Rational Zeros are :\n\n %s \
                                \n<The linear factorization : p(x) = (x%s%s)(x%s%s)(x%s%s) \n\
                                " % (self.__a,chr(252),self.signb,self.__b,chr(253),self.signc,self.__c,
                                self.signd,self.__d,Cubic.integerZero(self),nonintegersRationalZero(self)[0],
                                self.c3,-1*float(self.c1),self.c4,-1*float(self.c2),(self._checkSign(-1*j)),-1*j)
                        
                    return "\n<None of the non integers zeros %s \n\n checks p(x) = %sx%s %s %sx%s %s %sx %s %s  = 0\n\n" \
                             % (Cubic.nonintegersRationalZero(self)[0],self.__a,chr(252),self.signb,self.__b,
                                chr(253),self.signc,self.__c,self.signd,self.__d)
        except TypeError:
            if self.__a == 1:
                 raise "\n<complex solutions \n\n<The integers zeros are %s " \
                  % Cubic.integerZero(self)
            else :   
                raise "\n<complex solutions \n\n<The nonintegers zeros are %s " \
                  % Cubic.nonintegersRationalZero(self)[0]

    def get_a(self):
        """ Get method for _a attribute """
        
        return self.__a
        
    def set_a(self,value):
        """ Set method for _a attribute """
        
        self.__a = value
        
    def del_a(self):
        """Delete method for _a attribute"""
        
        del self.__a

    #Create a property
    _a = property(get_a,set_a,del_a,"a coefficient")

    def get_b(self):
        """ Get method for _b attribute """

        return self.__b

    def set_b(self,value):
        """ Set method for _b attribute """
        
        self.__b = value
        
    def del_b(self):
        """Delete method for D attribute"""

        del self.__b

    #Create a property
    _b = property(get_b,set_b,del_b,"b coefficient")

    def get_c(self):
        """ Get method for _c attribute """

        return self.__c

    def set_c(self,value):
        """ Set method for _c attribute """
        
        self.__c = value
        
    def del_c(self):
        """Delete method for _c attribute"""

        del self.__c

    #Create a property
    _c = property(get_c,set_c,del_c,"c coefficient")

    def get_d(self):
        """ Get method for _d attribute """

        return self.__d

    def set_d(self,value):
        """ Set method for _d attribute """
        
        self.__d = value
        
    def del_d(self):
        """Delete method for F attribute"""

        del self.__d

    #Create a property
    _d = property(get_d,set_d,del_d,"d coefficient")
    
    def _checkSign(self,value):
        """ Utility method to check the values's sign
        and return a sign string"""
        
        if value >= 0:
            return "+"
        else :
            return ""
        
    def integerZero(self):
        """ Computes Integers zeros of d coefficient """
        
        res = []
        for item in range (1,abs(self.__d)+1):
            if self.__d%item == 0:
                res.append(item)
                res.append(-1*item)
        return res
    
    def nonintegersRationalZero(self):
        """ Computes noninteger rational zeros """
        
        res1 = []
        res2 = []
        res3 = []
        res4 = []
        
        for b in range(1,abs(self.__a)+1):
            if self.__a%b == 0:
                res1.append(b)
        for i in Cubic.integerZero(self):
            if i>0:
                for j in res1:
                    if  i%j!=0:
                        res2.append( "%2.2f" % ((i)/float(j)) ),res2.append( "%2.2f" % ((-i)/float(j)) )
                        for x in res2:
                            if res2.count(x)>1:
                                res2.remove(x)
                                if x == ("%2.2f" % ((i)/float(j))):
                                    res3.append("%d/%d" % (i,j)),res3.append("%d/%d" % (-i,j))
                        res4.append("%d/%d" % (i,j)),res4.append("%d/%d" % (-i,j))     
                        for w in res3:
                            if w in res4:
                               res4.remove(w)
        return (res4,res2)
    
    def syntheticDivision(self):
        """ Computes coefficients A,B,C by synthetic division """
        
        assert self.__a != 0,"(a) coefficient should be differtent than zero"
        
        self._A = self.__a
        self._B = self.__b
        self._C = self.__c
        
        y = Quadratic()
        if self.__d != 0 and (self.__b**2 - 4*(self.__a *self.__c))>=0:
            for i in Cubic.integerZero(self):
                if (self.__a*((i)**3)) + (self.__b*((i)**2) )+(self.__c*(i) )+ self.__d == 0:
                    self._A = self.__a
                    self._B = self.__b + self._A*i
                    self._C = self.__c + self._B*i
            y(a=self._A,b=self._B,c=self._C)
            return  Quadratic.__call__(y)
            
        else:            
            
            y(a=self._A,b=self._B,c=self._C)
            return  Quadratic.__call__(y)            
             
        
    


        
if __name__ == "__main__":

    cubic1 = Cubic(1,3,-7,-21)
    print cubic1
    print
    cubic5 = Cubic(1,-3,-13,15)
    print cubic5
    print
    cubic2 = Cubic(1,2,-7,-10)
    print cubic2
    print
    cubic3 = Cubic(5,-1,-2,0)
    print cubic3
    print
    cubic4 = Cubic(2,-6,-13,18)
    print cubic4
    print
    cubic4 = Cubic(2,3,-4,-3)
    print cubic4
    print
    

################################################################################################

#c:\hp\bin\Python>python "C:\Documents\Programs\Cubic.py"

#<Cubic Equation: p(x) = 1x³ + 3x²  -7x  -21 = 0

#<The integers zeros  are :

#[1, -1, 3, -3, 7, -7, 21, -21]

#<The linear factorization : p(x) = (x-2.65)(x+2.65)(x+3)


#<Cubic Equation: p(x) = 1x³  -3x²  -13x + 15 = 0

#<The integers zeros  are :

#[1, -1, 3, -3, 5, -5, 15, -15]

#<The linear factorization : p(x) = (x-1.0)(x+3.0)(x-5)


#<None of the integers zeros [1, -1, 2, -2, 5, -5, 10, -10]

# checks p(x) = 1x³ + 2x²  -7x  -10 = 0


#<Cubic Equation: p(x) = 5x³  -1x²  -2x = 0

#<The linear factorization : p(x) = 5x(x-0.74)(x+0.54)


#<None of the non integers zeros ['1/2', '-1/2', '3/2', '-3/2', '9/2', '-9/2']

 #checks p(x) = 2x³  -6x²  -13x + 18  = 0


#<None of the non integers zeros ['1/2', '-1/2', '3/2', '-3/2']

 #checks p(x) = 2x³ + 3x²  -4x  -3  = 0


#c:\hp\bin\Python
##########################################################################################

#Version : Python 3.2

#from Quadratic5_7 import *

#class Cubic(object):
#    """ Class that represent a Cubic Polynomial Equation
#    with a,b,c,d properties"""
#
#    def __init__(self,a,b,c,d):
#        """ Cubic constructor takes a,b,c,d coefficients """
#        
#        self.__a = a
#        self.__b = b
#        self.__c = c
#        self.__d = d
#        
#        self.signb = self._checkSign(self.__b)
#        self.signc = self._checkSign(self.__c)
#        self.signd = self._checkSign(self.__d)
#  
#    def __str__(self):
#        """ String representation of Cubic Polynomial Equation"""
#        
#        try:
#            self.c1 = Cubic.syntheticDivision(self)[0]
#            self.c2 = Cubic.syntheticDivision(self)[1]
#            if self.c1 == float and self.c2 == float:
#                self.c3 ="-"
#                self.c4 ="+"
#            else :
#                self.c3 = self._checkSign(float(Cubic.syntheticDivision(self)[0])*-1)
#                self.c4 = self._checkSign(float(Cubic.syntheticDivision(self)[1])*-1)
#                
#
#            if self.__d == 0:
#                return "\n<Cubic Equation: p(x) = %sx%s %s %sx%s %s %sx = 0 \n \
#                        \n<The linear factorization : p(x) = %sx(x%s%s)(x%s%s) \n\
#                        " % (self.__a,chr(179),self.signb,self.__b,chr(178),
#                        self.signc,self.__c,self.__a,self.c3,-1*float(self.c1),
#                        self.c4,-1*float(self.c2))
#        
#            else :
#                if self.__a == 1:
#                    for i in Cubic.integerZero(self):
#                        if (((self.__a*(i**3)) + (self.__b*(i**2))+ (self.__c*i )+ #self.__d == 0)
#                            and float(i) != float(self.c2) and float(i) != float(self.c1)):
#                            return "\n<Cubic Equation: p(x) = %sx%s %s %sx%s %s %sx %s %#s = 0 \
#                                    \n\n<The integers zeros  are :\n\n%s\n \
#                                    \n<The linear factorization : p(x) = (x%s%s)(x%s%s)(x%s%s) \n\
#                                    " % (self.__a,chr(179),self.signb,self.__b,chr(178),self.signc,
#                                    self.__c,self.signd,self.__d,Cubic.integerZero(self),self.c3,
#                                    -1*float(self.c1),self.c4,-1*float(self.c2),(self._checkSign(-1*i)),-1*i)
                       
#                    return "\n<None of the integers zeros %s \n\n checks p(x) = %sx%s %s #%sx%s %s %sx %s %s = 0\n\n " \
#                            % (Cubic.integerZero(self),self.__a,chr(179),self.signb,self.__b,chr(178),self.signc,self.__c,
#                                self.signd,self.__d)
#        
#                else :
#                    for j in Cubic.nonintegersRationalZero(self)[1]:
#                        if ((self.__a*(float(str(j))**3)) + (self.__b*(float(str(j))**2))#+
#                            (self.__c*float(str(j)) )+ self.__d == 0.00):
#                            return "\n<Cubic Equation: p(x) = %sx%s %s %sx%s %s %sx %s %#s = 0 \
#                                \n\n<The integers Zeros are :\n\n %s \
#                                \n\n<The nonintegers Rational Zeros are :\n\n %s \
#                                \n<The linear factorization : p(x) = (x%s%s)(x%s%s)(x%s%#s) \n\
#                                " % (self.__a,chr(179),self.signb,self.__b,chr(178),self.signc,self.__c,
#                                self.signd,self.__d,Cubic.integerZero(self),nonintegersRationalZero(self)[0]
#                                self.c3,-1*float(self.c1),self.c4,-1*float(self.c2),(self._checkSign(-1*j)),-1*j)
                        
#                    return "\n<None of the non integers zeros %s \n\n checks p(x) = %sx%#s %s %sx%s %s %sx %s %s  = 0\n\n" \
#                             % (Cubic.nonintegersRationalZero(self)[0],self.__a,chr(179),self.signb,self.__b,
#                                chr(178),self.signc,self.__c,self.signd,self.__d)
#        except TypeError:
#            if self.__a == 1:
#                 raise "\n<complex solutions \n\n<The integers zeros are %s " \
#                  % Cubic.integerZero(self)
#            else :   
#                raise "\n<complex solutions \n\n<The nonintegers zeros are %s " \
#                  % Cubic.nonintegersRationalZero(self)[0]
#
#    def get_a(self):
#        """ Get method for _a attribute """
#        
#        return self.__a
#        
#    def set_a(self,value):
#        """ Set method for _a attribute """
#        
#        self.__a = value
#        
#    def del_a(self):
#       """Delete method for _a attribute"""
#        
#        del self.__a
#    #Create a property
#    _a = property(get_a,set_a,del_a,"a coefficient")

#    def get_b(self):
#        """ Get method for _b attribute """
#
#        return self.__b
#
#    def set_b(self,value):
#        """ Set method for _b attribute """
#        
#        self.__b = value
#        
#    def del_b(self):
#        """Delete method for D attribute"""
#
#        del self.__b
#
#    #Create a property
#    _b = property(get_b,set_b,del_b,"b coefficient")
#
#    def get_c(self):
#        """ Get method for _c attribute """
#
#        return self.__c
#
#    def set_c(self,value):
#        """ Set method for _c attribute """
#        
#        self.__c = value
#        
#    def del_c(self):
#        """Delete method for _c attribute"""
        del self.__c

#    #Create a property
#    _c = property(get_c,set_c,del_c,"c coefficient")
#
#    def get_d(self):
#        """ Get method for _d attribute """

#        return self.__d
#    def set_d(self,value):
#        """ Set method for _d attribute """
#        
#        self.__d = value
#        
#    def del_d(self):
#        """Delete method for F attribute"""
#
#        del self.__d
#
#    #Create a property
#    _d = property(get_d,set_d,del_d,"d coefficient")
#    
#    def _checkSign(self,value):
#        """ Utility method to check the values's sign
#        and return a sign string"""
#        
#        if value >= 0:
#            return "+"
#        else :
#            return ""
#        
#    def integerZero(self):
#        """ Computes Integers zeros of d coefficient """
#        
#        res = []
#        for item in range (1,abs(self.__d)+1):
#            if self.__d%item == 0:
#                res.append(item)
#                res.append(-1*item)
#        return res
#    
#    def nonintegersRationalZero(self):
#        """ Computes noninteger rational zeros """
#        
#        res1 = []
#        res2 = []
#        res3 = []
#        res4 = []
#        
#        for b in range(1,abs(self.__a)+1):
#            if self.__a%b == 0:
#                res1.append(b)
#        for i in Cubic.integerZero(self):
#            if i>0:
#                for j in res1:
#                    if  i%j!=0:
#                        res2.append( "%2.2f" % ((i)/float(j)) ),res2.append( "%2.2f" % ((-i)/float(j)) )
#                        for x in res2:
#                            if res2.count(x)>1:
#                                res2.remove(x)
#                                if x == ("%2.2f" % ((i)/float(j))):
#                                    res3.append("%d/%d" % (i,j)),res3.append("%d/%d" % (-i,j))
#                        res4.append("%d/%d" % (i,j)),res4.append("%d/%d" % (-i,j))     
#                        for w in res3:
#                            if w in res4:
#                               res4.remove(w)
#        return (res4,res2)
#    
#    def syntheticDivision(self):
#        """ Computes coefficients A,B,C by synthetic division """
#        
#        assert self.__a != 0,"(a) coefficient should be differtent than zero"
#        
#        self._A = self.__a
#        self._B = self.__b
#        self._C = self.__c
#        
#        y = Quadratic()
#        if self.__d != 0 and (self.__b**2 - 4*(self.__a *self.__c))>=0:
#            for i in Cubic.integerZero(self):
#                if (self.__a*((i)**3)) + (self.__b*((i)**2) )+(self.__c*(i) )+ self.__d #== 0:
#                    self._A = self.__a
#                    self._B = self.__b + self._A*i
#                    self._C = self.__c + self._B*i
#            y(a=self._A,b=self._B,c=self._C)
#            return  Quadratic.__call__(y)
#            
#        else:            
#            
#            y(a=self._A,b=self._B,c=self._C)
#            return  Quadratic.__call__(y)            
#             
#        
#    


        
#if __name__ == "__main__":
#    cubic1 = Cubic(1,3,-7,-21)
#    print(cubic1)
#    print()
#    cubic5 = Cubic(1,-3,-13,15)
#    print(cubic5)
#    print()
#    cubic2 = Cubic(1,2,-7,-10)
#    print(cubic2)
#    print()
#    cubic3 = Cubic(5,-1,-2,0)
#    print(cubic3)
#    print()
#    cubic4 = Cubic(2,-6,-13,18)
#    print(cubic4)
#    print()
#    cubic4 = Cubic(2,3,-4,-3)
#    print(cubic4)
#    print()
#
