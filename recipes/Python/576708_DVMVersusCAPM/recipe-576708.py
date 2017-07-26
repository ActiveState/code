#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 07/03/09
#version :2.6.1

"""
collections module's extras in python 2.6.1 were used in my program, DVMextrapolating
DVMgordonsModel and CAPM subclasses of namedtuple Python class provide the cost of equity
the calculation of the dividend growth g in two different ways, and the value of the company
if the cost of equity Ke is known.
I used an utility method and the try/exceptions statements to raise errors
"""

import math as m
from collections import namedtuple

class MyError:
    """ Demonstrate imporper operation on negative number"""
     
    def _negativeNumberException(self,*args):
        """ Utility method to raise a negative number exception"""
        
        for item in args:
            if item <0:

                raise ValueError,\
                    " <The value %s should be a positive number " % item

class DVMextrapolating(namedtuple('DVMextrapolating','dividend_just_paid,dividend_n_years,n,share_price,Ke'),MyError):
    """ DVMeModel class inherits from tuple and MyError class """

    #set __slots__ to an empty tuple keep memory requirements low    
    __slots__ = ()
    
    #Pick Myerror method
    _negativeNumberException =MyError._negativeNumberException
    
    @property
    def g_extrapolatingModel(self):
        """ Compute g using extrapolating """

        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.dividend_just_paid,self.dividend_n_years,self.n)
            return "%2.2f" % ((float(m.pow((self.dividend_just_paid/self.dividend_n_years),(1/float(self.n)))) -1))

        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"

        #division by zero raises ZeroDivisionError exception
        except ZeroDivisionError:
            raise ZeroDivisionError, "\n<Please check and re-enter the values"
            
    @property
    def valueOfShare(self):
        """ Compute the share value """

        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.dividend_just_paid,self.dividend_n_years,self.Ke)
            return "%2.2f" % (((self.dividend_just_paid*
                    (1+float(self.g_extrapolatingModel)))/(self.Ke-float(self.g_extrapolatingModel)))) 

        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"
            
        #division by zero raises ZeroDivisionError exception
        except ZeroDivisionError:
            raise ZeroDivisionError, "\n<Please check and re-enter the values"
            
    @property
    def costOfEquity(self):
        """ Compute cost of equity using DVM Model """
        
        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.dividend_just_paid,self.share_price)
            return "%2.1f" % ((((self.dividend_just_paid*
                    (1+float(self.g_extrapolatingModel))/self.share_price))+ float(self.g_extrapolatingModel))*100)

        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"

        #division by zero raises ZeroDivisionError exception
        except ZeroDivisionError:
            raise ZeroDivisionError, "\n<Please check and re-enter the values"
            
    def __str__(self):
        """ String representation of DVMeModel"""
        
        if self.Ke == None:
            return "\n< Extrapolating Growth Model g = %s\n \
                  \n< Cost of equity Ke = %s \n\
                  \n< Market value of the share Po = %s" % \
                  (self.g_extrapolatingModel,(self.costOfEquity+'%'),('$'+ str(self.share_price))) 

        else:
            return "\n< Extrapolating Growth Model g = %s\n \
                  \n< Cost of equity Ke = %s \n\
                  \n< Market value of the share Po = %s" % \
                  (self.g_extrapolatingModel,self.Ke,('$'+ str(self.valueOfShare))) 

class DVMgordonsModel(namedtuple('DVMgordonsModel','dividend_just_paid,return_on_equity,dividend_payout,share_price,Ke'),MyError):
    """ DVMgModel class inherits from tuple and MyError classes """

    #set __slots__ to an empty tuple keep memory requirements low      
    __slots__ = ()
    
    #Pick Myerror method
    _negativeNumberException =MyError._negativeNumberException
    
    @property
    def g_gordonsModel(self):
        """ Compute g using Gordons growth Model """
        
        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.return_on_equity,self.dividend_payout)
            return self.return_on_equity * (1-self.dividend_payout)

        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"
            
    @property
    def valueOfShare(self):
        """ Compute the share value """
        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.dividend_just_paid,self.Ke)        
            return "%2.2f" % (((self.dividend_just_paid*
                    (1+float(self.g_gordonsModel)))/(self.Ke-self.g_gordonsModel)))

        #Raise TypeError if input is not numerical        
        except TypeError:
            print "\n<The entered value is not a number"

        #division by zero raises ZeroDivisionError exception        
        except ZeroDivisionError:
            raise ZeroDivisionError, "\n<Please check and re-enter the values"
            
    @property
    def costOfEquity(self):
        """ Compute cost of equity using DVM Model """
        
        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.dividend_just_paid,self.share_price)        
            return "%2.1f" % ((((self.dividend_just_paid*
                    (1+float(self.g_gordonsModel)))/(self.share_price))+ float(self.g_gordonsModel))*100 )

        #Raise TypeError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"

        #division by zero raises ZeroDivisionError exception        
        except ZeroDivisionError:
            raise ZeroDivisionError, "\n<Please check and re-enter the values"
            
    def __str__(self):
        """ String representation of DVMgModel"""
        
        if self.Ke == None:

            return "\n< Gordon's Growth Model g = %s\n \
                  \n< Cost of equity Ke = %s \n\
                  \n< Market value of the share Po = %s" % \
                  (self.g_gordonsModel,(self.costOfEquity+'%'),('$'+ str(self.share_price)))        

        else:
            return "\n< Gordon's Growth Model g = %s\n \
                  \n< Cost of equity Ke = %s \n\
                  \n< Market value of the share Po = %s" % \
                  (self.g_gordonsModel,self.Ke,('$'+ str(self.valueOfShare)))        

class CAPM(namedtuple('CAPM','Rf,Beta,Rm'),MyError):
    """ CAPM class inherits from tuple and MyError class """

    #set __slots__ to an empty tuple keep memory requirements low            
    __slots__ = ()
    
    #Pick Myerror method
    _negativeNumberException =MyError._negativeNumberException
    
    @property
    def Ke(self):
        """ Compute cost of equity using CAPM model """
        
        try:
            #Test for negative numbers input and raise the exception
            self._negativeNumberException(self.Rf,self.Beta,self.Rm)
            return self.Rf + self.Beta*(self.Rm - self.Rf)

        #Raise ValueError if input is not numerical
        except TypeError:
            print "\n<The entered value is not a number"
            
    def __str__(self):
        """ String representation of CAPM"""
        
        return "\n< Ke = %s" % self.Ke+"%"        

if __name__ == '__main__':
    a = CAPM('Rf','Beta','Rm')
    b = [7,0.7,17]
    a = a._make(b)
    print "\n"+"\4"*43
    print a
    print "\n"+"\4"*43    
    c = DVMextrapolating('dividend_just_paid','dividend_n_years','n','share_price','Ke')
    d = [0.24,0.1525,4,None,a.Ke/100]
    c = c._make(d)
    print c
    
    print "\n"+"\4"*43
    e = DVMgordonsModel('dividend_just_paid','return_on_equity','dividend_payout','share_price','Ke')

    f = [0.18,0.2,0.72,None,0.127]
    e = e._make(f)
    print e

    print "\n"+"\4"*43
    g = [0.25,0.17,7,17.50,None]
    c = c._make(g)
    print c
    
    print "\n"+"\4"*43
    h = [0.17,0.3,0.37,1.77,None]
    e = e._make(h)
    print e
    
    print "\n"+"\4"*43
    print
    print c.g_extrapolatingModel
    print c.costOfEquity
    print e.g_gordonsModel
    print e.costOfEquity

    print "\n"+"\5"*43    
    m = [None,0.5,0.57,None,None]
    e = e._make(m)
    print e.g_gordonsModel 
    
##########################################################################################

#  c:\Python26>python "C:\Users\Fouad Teniou\Documents\python\DVM_Versus_CAPM7.py"

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#< Ke = 14.0%

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#< Extrapolating Growth Model g = 0.12

#< Cost of equity Ke = 0.14

#< Market value of the share Po = $13.44

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#< Gordon's Growth Model g = 0.056

#< Cost of equity Ke = 0.127

#< Market value of the share Po = $2.68

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#< Extrapolating Growth Model g = 0.06

#< Cost of equity Ke = 7.5%

#< Market value of the share Po = $17.5

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#< Gordon's Growth Model g = 0.189

#< Cost of equity Ke = 30.3%

#< Market value of the share Po = $1.77

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#0.06
#7.5
#0.189
#30.3

#♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣
#0.215

#c:\Python26>  
##########################################################################################

#Version : Python 3.2

#import math as m
#from collections import namedtuple

#class MyError:
#    """ Demonstrate imporper operation on negative number"""
     
#    def _negativeNumberException(self,*args):
#        """ Utility method to raise a negative number exception"""
#        
#        for item in args:
#            if item <0:
#
#                raise ValueError(" <The value %s should be a positive number " % item)
#
#class DVMextrapolating(namedtuple('DVMextrapolating','dividend_just_paid,dividend_n_years,n,share_price,Ke'),MyError):
#    """ DVMeModel class inherits from tuple and MyError class """
#
#    #set __slots__ to an empty tuple keep memory requirements low    
#    __slots__ = ()
#    
#    #Pick Myerror method
#    _negativeNumberException =MyError._negativeNumberException
#    
#    @property
#    def g_extrapolatingModel(self):
#        """ Compute g using extrapolating """
#
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.dividend_just_paid,self.dividend_n_years,self.n)
#            return "%2.2f" % ((float(m.pow((self.dividend_just_paid/self.dividend_n_years),(1/float(self.n)))) -1))
#
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#
#        #division by zero raises ZeroDivisionError exception
#        except ZeroDivisionError:
#            raise ZeroDivisionError("\n<Please check and re-enter the values")
#            
#    @property
#    def valueOfShare(self):
#        """ Compute the share value """
#
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.dividend_just_paid,self.dividend_n_years,self.Ke)
#            return "%2.2f" % (((self.dividend_just_paid*
#                    (1+float(self.g_extrapolatingModel)))/(self.Ke-float(self.g_extrapolatingModel)))) 
#
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#            
#        #division by zero raises ZeroDivisionError exception
#        except ZeroDivisionError:
#            raise ZeroDivisionError("\n<Please check and re-enter the values")
#            
#    @property
#    def costOfEquity(self):
#        """ Compute cost of equity using DVM Model """
#        
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.dividend_just_paid,self.share_price)
#            return "%2.1f" % ((((self.dividend_just_paid*
#                    (1+float(self.g_extrapolatingModel))/self.share_price))+ float(self.g_extrapolatingModel))*100)
#
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#
#        #division by zero raises ZeroDivisionError exception
#        except ZeroDivisionError:
#            raise ZeroDivisionError("\n<Please check and re-enter the values")
#            
#    def __str__(self):
#        """ String representation of DVMeModel"""
#        
#        if self.Ke == None:
#            return "\n< Extrapolating Growth Model g = %s\n \
#                  \n< Cost of equity Ke = %s \n\
#                  \n< Market value of the share Po = %s" % \
#                  (self.g_extrapolatingModel,(self.costOfEquity+'%'),('$'+ str(self.share_price))) 

#        else:
#            return "\n< Extrapolating Growth Model g = %s\n \
#                  \n< Cost of equity Ke = %s \n\
#                  \n< Market value of the share Po = %s" % \
#                  (self.g_extrapolatingModel,self.Ke,('$'+ str(self.valueOfShare))) 
#
#class DVMgordonsModel(namedtuple('DVMgordonsModel','dividend_just_paid,return_on_equity,dividend_payout,share_price,Ke'),MyError):
#    """ DVMgModel class inherits from tuple and MyError classes """
#
#    #set __slots__ to an empty tuple keep memory requirements low      
#    __slots__ = ()
#    
#    #Pick Myerror method
#    _negativeNumberException =MyError._negativeNumberException
#    
#    @property
#    def g_gordonsModel(self):
#        """ Compute g using Gordons growth Model """
#        
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.return_on_equity,self.dividend_payout)
#            return self.return_on_equity * (1-self.dividend_payout)
#        #Raise TypeError if input is not numerical
#       except TypeError:
#            print("\n<The entered value is not a number")
#            
#    @property
#    def valueOfShare(self):
#        """ Compute the share value """
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.dividend_just_paid,self.Ke)        
#            return "%2.2f" % (((self.dividend_just_paid*
#                    (1+float(self.g_gordonsModel)))/(self.Ke-self.g_gordonsModel)))
#
#        #Raise TypeError if input is not numerical        
#        except TypeError:
#            print("\n<The entered value is not a number")
#
#        #division by zero raises ZeroDivisionError exception        
#        except ZeroDivisionError:
#            raise ZeroDivisionError("\n<Please check and re-enter the values")
#            
#    @property
#    def costOfEquity(self):
#        """ Compute cost of equity using DVM Model """
#        
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.dividend_just_paid,self.share_price)        
#            return "%2.1f" % ((((self.dividend_just_paid*
#                    (1+float(self.g_gordonsModel)))/(self.share_price))+ float(self.g_gordonsModel))*100 )
#
#        #Raise TypeError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#
#        #division by zero raises ZeroDivisionError exception        
#        except ZeroDivisionError:
#            raise ZeroDivisionError("\n<Please check and re-enter the values")
#            
#    def __str__(self):
#        """ String representation of DVMgModel"""
#        
#        if self.Ke == None:
#
#            return "\n< Gordon's Growth Model g = %s\n \
#                  \n< Cost of equity Ke = %s \n\
#                  \n< Market value of the share Po = %s" % \
#                  (self.g_gordonsModel,(self.costOfEquity+'%'),('$'+ str(self.share_price)))        
#
#        else:
#            return "\n< Gordon's Growth Model g = %s\n \
#                  \n< Cost of equity Ke = %s \n\
#                  \n< Market value of the share Po = %s" % \
#                  (self.g_gordonsModel,self.Ke,('$'+ str(self.valueOfShare)))        
#
#class CAPM(namedtuple('CAPM','Rf,Beta,Rm'),MyError):
#    """ CAPM class inherits from tuple and MyError class """
#
#    #set __slots__ to an empty tuple keep memory requirements low            
#    __slots__ = ()
#    
#    #Pick Myerror method
#    _negativeNumberException =MyError._negativeNumberException
#    
#    @property
#    def Ke(self):
#        """ Compute cost of equity using CAPM model """
#        
#        try:
#            #Test for negative numbers input and raise the exception
#            self._negativeNumberException(self.Rf,self.Beta,self.Rm)
#            return self.Rf + self.Beta*(self.Rm - self.Rf)
#
#        #Raise ValueError if input is not numerical
#        except TypeError:
#            print("\n<The entered value is not a number")
#            
#    def __str__(self):
#        """ String representation of CAPM"""
#        
#        return "\n< Ke = %s" % self.Ke+"%"        
#
#if __name__ == '__main__':
#    a = CAPM('Rf','Beta','Rm')
#    b = [7,0.7,17]
#    a = a._make(b)
#    print("\n"+"\4"*43)
#    print(a)
#    print("\n"+"\4"*43)    
#    c = DVMextrapolating('dividend_just_paid','dividend_n_years','n','share_price','Ke')
#    d = [0.24,0.1525,4,None,a.Ke/100]
#    c = c._make(d)
#    print(c)
#    
#    print("\n"+"\4"*43)
#    e = DVMgordonsModel('dividend_just_paid','return_on_equity','dividend_payout','share_price','Ke')
#
#    f = [0.18,0.2,0.72,None,0.127]
#    e = e._make(f)
#    print(e)
#    print("\n"+"\4"*43)
#    g = [0.25,0.17,7,17.50,None]
#    c = c._make(g)
#    print(c)
#    
#    print("\n"+"\4"*43)
#    h = [0.17,0.3,0.37,1.77,None]
#    e = e._make(h)
#    print(e)
#    
#    print("\n"+"\4"*43)
#    print()
#    print(c.g_extrapolatingModel)
#    print(c.costOfEquity)
#    print(e.g_gordonsModel)
#    print(e.costOfEquity)

#    print("\n"+"\5"*43)    
#    m = [None,0.5,0.57,None,None]
#    e = e._make(m)
#    print(e.g_gordonsModel) 
