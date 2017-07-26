'''\
An experiment with python properties using TVM equations as an example

A TVM object works like a financial calculator.
Given any four of (n, i, pmt, pv, fv) TVM object can calculate the fifth.
This version assumes payments are at end of compounding period.

Example:
>>> loan=TVM()
>>> loan.n=3*12           # set number of payments to 36
>>> loan.pv=6000          # set present value to 6000
>>> loan.i=6/12.          # set interest rate to 6% annual
>>> loan.fv=0             # set future value to zero
>>> loan.pmt              # ask for payment amount
-182.5316247083343        # payment (note sign)

Alternative style:
>>> TVM(n=36, pv=6000, pmt=-200, fv=0).i*12
12.2489388032796
'''

from math import log
from __future__ import division

class TVM (object):
    '''A Time Value of Money class using properties'''

    def __init__(self, n=None, i=None, pv=None, pmt=None, fv=None):
        self.__n=n
        self.__i=i
        self.__pv=pv
        self.__pmt=pmt
        self.__fv=fv

    def __repr__(self):
        return "TVM(n=%s, i=%s, pv=%s, pmt=%s, fv=%s)" %   \
              (self.__n, self.__i, self.__pv, self.__pmt, self.__fv)

    def __get_a(self):
        '''calculate 'a' intermediate value'''
        return (1+self.__i/100)**self.__n-1

    def __get_b(self):
        '''calculate 'b' intermediate value'''
        return 100/self.__i

    def __get_c(self):
        '''calculate 'c' intermediate value'''
        return self.__get_b()*self.__pmt

    def get_n(self):
        c=self.__get_c()
        self.__n = log((c-self.__fv)/(c+self.__pv))/log(1+self.__i/100)
        return self.__n
    def set_n(self,value):
        self.__n=value
    n = property(get_n, set_n, None, 'number of payments')

    def get_i(self):
        # need to do an iterative solution - no closed form solution exists
        # trying Newton's method
        INTTOL=0.0000001      # tolerance
        ITERLIMIT=1000        # iteration limit
        # initial guess for interest
        if self.__i:
            i0=self.__i
        else:
            i0=1.0
        # 10% higher interest rate - to get a slope calculation
        i1=1.1*i0
        def f(tvm,i):
            '''function used in Newton's method; pmt(i)-pmt'''
            a = (1+i/100)**self.__n-1
            b = 100/i
            out = -(tvm.__fv+tvm.__pv*(a+1))/(a*b)-tvm.__pmt
            return out
        fi0 = f(self,i0)
        if abs(fi0)<INTTOL:
            self.__i=i0
            return i0
        else:
            n=0
            while 1:                    # Newton's method loop here
                fi1 = f(self,i1)
                if abs(fi1)<INTTOL:
                    break
                if n>ITERLIMIT:
                    print "Failed to converge; exceeded iteration limit"
                    break
                slope=(fi1-fi0)/(i1-i0)
                i2=i0-fi0/slope           # New 'i1'
                fi0 = fi1
                i0=i1
                i1=i2
                n+=1
            self.__i = i1
            return self.__i

    def set_i(self,value):
        self.__i=value
    i = property(get_i, set_i, None, 'interest rate')

    def get_pv(self):
        a=self.__get_a()
        c=self.__get_c()
        self.__pv = -(self.__fv+a*c)/(a+1)
        return self.__pv
    def set_pv(self,value):
        self.__pv=value
    pv = property(get_pv, set_pv, None, 'present value')

    def get_pmt(self):
        a=self.__get_a()
        b=self.__get_b()
        self.__pmt = -(self.__fv+self.__pv*(a+1))/(a*b)
        return self.__pmt
    def set_pmt(self,value):
        self.__pmt=value
    pmt = property(get_pmt, set_pmt, None, 'payment')

    def get_fv(self):
        a=self.__get_a()
        c=self.__get_c()
        self.__fv = -(self.__pv+a*(self.__pv+c))
        return self.__fv
    def set_fv(self,value):
        self.__fv=value
    fv = property(get_fv, set_fv, None, 'future value')
