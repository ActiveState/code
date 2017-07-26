'''error function and complementary error function
'''

##/*
## * ====================================================
## * Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.
## *
## * Developed at SunPro, a Sun Microsystems, Inc. business.
## * Permission to use, copy, modify, and distribute this
## * software is freely granted, provided that this notice 
## * is preserved.
## * ====================================================
## */
##
##/* double erf(double x)
## * double erfc(double x)
## * original code from: http://sourceware.org/cgi-bin/cvsweb.cgi/~checkout~/src/newlib/libm/math/s_erf.c?rev=1.1.1.1&cvsroot=src
## * 		     x
## *		      2      |\
## *     erf(x)  =  ---------  | exp(-t*t)dt
## *	 	   sqrt(pi) \| 
## *			     0
## *
## *     erfc(x) =  1-erf(x)
## *  Note that 
## *		erf(-x) = -erf(x)
## *		erfc(-x) = 2 - erfc(x)
## *
## * Method:
## *	1. For |x| in [0, 0.84375]
## *	    erf(x)  = x + x*R(x^2)
## *          erfc(x) = 1 - erf(x)           if x in [-.84375,0.25]
## *                  = 0.5 + ((0.5-x)-x*R)  if x in [0.25,0.84375]
## *	   where R = P/Q where P is an odd poly of degree 8 and
## *	   Q is an odd poly of degree 10.
## *						 -57.90
## *			| R - (erf(x)-x)/x | <= 2
## *	
## *
## *	   Remark. The formula is derived by noting
## *          erf(x) = (2/sqrt(pi))*(x - x^3/3 + x^5/10 - x^7/42 + ....)
## *	   and that
## *          2/sqrt(pi) = 1.128379167095512573896158903121545171688
## *	   is close to one. The interval is chosen because the fix
## *	   point of erf(x) is near 0.6174 (i.e., erf(x)=x when x is
## *	   near 0.6174), and by some experiment, 0.84375 is chosen to
## * 	   guarantee the error is less than one ulp for erf.
## *
## *      2. For |x| in [0.84375,1.25], let s = |x| - 1, and
## *         c = 0.84506291151 rounded to single (24 bits)
## *         	erf(x)  = sign(x) * (c  + P1(s)/Q1(s))
## *         	erfc(x) = (1-c)  - P1(s)/Q1(s) if x > 0
## *			  1+(c+P1(s)/Q1(s))    if x < 0
## *         	|P1/Q1 - (erf(|x|)-c)| <= 2**-59.06
## *	   Remark: here we use the taylor series expansion at x=1.
## *		erf(1+s) = erf(1) + s*Poly(s)
## *			 = 0.845.. + P1(s)/Q1(s)
## *	   That is, we use rational approximation to approximate
## *			erf(1+s) - (c = (single)0.84506291151)
## *	   Note that |P1/Q1|< 0.078 for x in [0.84375,1.25]
## *	   where 
## *		P1(s) = degree 6 poly in s
## *		Q1(s) = degree 6 poly in s
## *
## *      3. For x in [1.25,1/0.35(~2.857143)], 
## *         	erfc(x) = (1/x)*exp(-x*x-0.5625+R1/S1)
## *         	erf(x)  = 1 - erfc(x)
## *	   where 
## *		R1(z) = degree 7 poly in z, (z=1/x^2)
## *		S1(z) = degree 8 poly in z
## *
## *      4. For x in [1/0.35,28]
## *         	erfc(x) = (1/x)*exp(-x*x-0.5625+R2/S2) if x > 0
## *			= 2.0 - (1/x)*exp(-x*x-0.5625+R2/S2) if -6<x<0
## *			= 2.0 - tiny		(if x <= -6)
## *         	erf(x)  = sign(x)*(1.0 - erfc(x)) if x < 6, else
## *         	erf(x)  = sign(x)*(1.0 - tiny)
## *	   where
## *		R2(z) = degree 6 poly in z, (z=1/x^2)
## *		S2(z) = degree 7 poly in z
## *
## *      Note1:
## *	   To compute exp(-x*x-0.5625+R/S), let s be a single
## *	   precision number and s := x; then
## *		-x*x = -s*s + (s-x)*(s+x)
## *	        exp(-x*x-0.5626+R/S) = 
## *			exp(-s*s-0.5625)*exp((s-x)*(s+x)+R/S);
## *      Note2:
## *	   Here 4 and 5 make use of the asymptotic series
## *			  exp(-x*x)
## *		erfc(x) ~ ---------- * ( 1 + Poly(1/x^2) )
## *			  x*sqrt(pi)
## *	   We use rational approximation to approximate
## *      	g(s)=f(1/x^2) = log(erfc(x)*x) - x*x + 0.5625
## *	   Here is the error bound for R1/S1 and R2/S2
## *      	|R1/S1 - f(x)|  < 2**(-62.57)
## *      	|R2/S2 - f(x)|  < 2**(-61.52)
## *
## *      5. For inf > x >= 28
## *         	erf(x)  = sign(x) *(1 - tiny)  (raise inexact)
## *         	erfc(x) = tiny*tiny (raise underflow) if x > 0
## *			= 2 - tiny if x<0
## *
## *      7. Special case:
## *         	erf(0)  = 0, erf(inf)  = 1, erf(-inf) = -1,
## *         	erfc(0) = 1, erfc(inf) = 0, erfc(-inf) = 2, 
## *	   	erfc/erf(NaN) is NaN
## */



from math import *

tiny= 1e-300
half=  5.00000000000000000000e-01
one =  1.00000000000000000000e+00
two =  2.00000000000000000000e+00
erx =  8.45062911510467529297e-01

## Coefficients for approximation to  erf on [0,0.84375]

efx =  1.28379167095512586316e-01
efx8=  1.02703333676410069053e+00
pp0  =  1.28379167095512558561e-01
pp1  = -3.25042107247001499370e-01
pp2  = -2.84817495755985104766e-02
pp3  = -5.77027029648944159157e-03
pp4  = -2.37630166566501626084e-05
qq1  =  3.97917223959155352819e-01
qq2  =  6.50222499887672944485e-02
qq3  =  5.08130628187576562776e-03
qq4  =  1.32494738004321644526e-04
qq5  = -3.96022827877536812320e-06

def erf1(x):
    '''erf(x) for x in [0,0.84375]'''
    e, i = frexp(x)
    if abs(i)>28:
        if abs(i)>57:
            return 0.125*(8.0*x+efx8*x)
        return x + efx*x
    z = x*x
    r = pp0+z*(pp1+z*(pp2+z*(pp3+z*pp4)))
    s = one+z*(qq1+z*(qq2+z*(qq3+z*(qq4+z*qq5))))
    y = r/s
    return x + x*y

def erfc1(x):
    '''erfc(x)for x in [0,0.84375]'''
    e,i = frexp(x)
    if abs(i)>56:
        return one-x
    z = x*x
    r = pp0+z*(pp1+z*(pp2+z*(pp3+z*pp4)))
    s = one+z*(qq1+z*(qq2+z*(qq3+z*(qq4+z*qq5))))
    y = r/s
    if (x<0.25):
        return one-(x+x*y)
    else:
        r = x*y
        r += (x-half)
        return half - r

## Coefficients for approximation to  erf  in [0.84375,1.25] 

pa0  = -2.36211856075265944077e-03
pa1  =  4.14856118683748331666e-01
pa2  = -3.72207876035701323847e-01
pa3  =  3.18346619901161753674e-01
pa4  = -1.10894694282396677476e-01
pa5  =  3.54783043256182359371e-02
pa6  = -2.16637559486879084300e-03
qa1  =  1.06420880400844228286e-01
qa2  =  5.40397917702171048937e-01
qa3  =  7.18286544141962662868e-02
qa4  =  1.26171219808761642112e-01
qa5  =  1.36370839120290507362e-02
qa6  =  1.19844998467991074170e-02

def erf2(x):
    '''erf(x) for x in [0.84375,1.25]'''
    s = fabs(x)-one
    P = pa0+s*(pa1+s*(pa2+s*(pa3+s*(pa4+s*(pa5+s*pa6)))))
    Q = one+s*(qa1+s*(qa2+s*(qa3+s*(qa4+s*(qa5+s*qa6)))))
    if x>=0:
        return erx + P/Q
    return -erx - P/Q

def erfc2(x):
    '''erfc(x) for x in [0.84375, 1.25]'''
    return one-erf2(x)

## Coefficients for approximation to  erfc in [1.25,1/0.35]

ra0  = -9.86494403484714822705e-03
ra1  = -6.93858572707181764372e-01
ra2  = -1.05586262253232909814e+01
ra3  = -6.23753324503260060396e+01
ra4  = -1.62396669462573470355e+02
ra5  = -1.84605092906711035994e+02
ra6  = -8.12874355063065934246e+01
ra7  = -9.81432934416914548592e+00
sa1  =  1.96512716674392571292e+01
sa2  =  1.37657754143519042600e+02
sa3  =  4.34565877475229228821e+02
sa4  =  6.45387271733267880336e+02
sa5  =  4.29008140027567833386e+02
sa6  =  1.08635005541779435134e+02
sa7  =  6.57024977031928170135e+00
sa8  = -6.04244152148580987438e-02

def erf3(x):
    '''erf(x) for x in [1.25,2.857142]'''
    x0=x
    x = fabs(x)
    s = one/(x*x)
    R=ra0+s*(ra1+s*(ra2+s*(ra3+s*(ra4+s*(ra5+s*(ra6+s*ra7))))))
    S=one+s*(sa1+s*(sa2+s*(sa3+s*(sa4+s*(sa5+s*(sa6+s*(sa7+s*sa8)))))))
    z = ldexp(x0,0)
    r = exp(-z*z-0.5625)*exp((z-x)*(z+x)+R/S)
    if(x0>=0):
        return one-r/x
    else:
        return  r/x-one;

def erfc3(x):
    '''erfc(x) for x in [1.25,1/0.35]'''
    return one-erf3(x)

## Coefficients for approximation to  erfc in [1/.35,28]

rb0  = -9.86494292470009928597e-03
rb1  = -7.99283237680523006574e-01
rb2  = -1.77579549177547519889e+01
rb3  = -1.60636384855821916062e+02
rb4  = -6.37566443368389627722e+02
rb5  = -1.02509513161107724954e+03
rb6  = -4.83519191608651397019e+02
sb1  =  3.03380607434824582924e+01
sb2  =  3.25792512996573918826e+02
sb3  =  1.53672958608443695994e+03
sb4  =  3.19985821950859553908e+03
sb5  =  2.55305040643316442583e+03
sb6  =  4.74528541206955367215e+02
sb7  = -2.24409524465858183362e+01

def erf4(x):
    '''erf(x) for x in [1/.35,6]'''
    x0=x
    x = fabs(x)
    s = one/(x*x)
    R=rb0+s*(rb1+s*(rb2+s*(rb3+s*(rb4+s*(rb5+s*rb6)))))
    S=one+s*(sb1+s*(sb2+s*(sb3+s*(sb4+s*(sb5+s*(sb6+s*sb7))))))
    z  = ldexp(x0,0)
    r  =  exp(-z*z-0.5625)*exp((z-x)*(z+x)+R/S)
    if(z>=0):
        return one-r/x
    else:
        return  r/x-one;

def erfc4(x):
    '''erfc(x) for x in [2.857142,6]'''
    return one-erf4(x)

def erf5(x):
    '''erf(x) for |x| in [6,inf)'''
    if x>0:
        return one-tiny
    return tiny-one

def erfc5(x):
    '''erfc(x) for |x| in [6,inf)'''
    if (x>0):
        return tiny*tiny
    return two-tiny

#############
##inf = float('inf')
##nan = float('nan')
###########
inf = float(9e999)

def Erf(x):
    '''return the error function of x'''
    f = float(x)
    if (f == inf):
        return 1.0
    elif (f == -inf):
        return -1.0
##    elif (f is nan):
##        return nan
    else:
        if (abs(x)<0.84375):
            return erf1(x)
        elif (0.84375<=abs(x)<1.25):
            return erf2(x)
        elif (1.25<=abs(x)<2.857142):
            return erf3(x)
        elif (2.857142<=abs(x)<6):
            return erf4(x)
        elif (abs(x)>=6):
            return erf5(x)
    
def Erfc(x):
    '''return the complementary of error function of x'''
    f = float(x)
    if (f == inf):
        return 0.0
    elif (f is -inf):
        return 2.0
##    elif (f == nan):
##        return nan
    else:
        if (abs(x)<0.84375):
            return erfc1(x)
        elif (0.84375<=abs(x)<1.25):
            return erfc2(x)
        elif (1.25<=abs(x)<2.857142):
            return erfc3(x)
        elif (2.857142<=abs(x)<6):
            return erfc4(x)
        elif (abs(x)>=6):
            return erfc5(x)
