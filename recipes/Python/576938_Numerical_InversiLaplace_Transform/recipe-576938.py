# -*- coding: iso-8859-1 -*-

# laplace.py with mpmath
#   appropriate for high precision

# Talbot suggested that the Bromwich line be deformed into a contour that begins
# and ends in the left half plane, i.e., z \to \infty at both ends.
# Due to the exponential factor the integrand decays rapidly
# on such a contour. In such situations the trapezoidal rule converge
# extraordinarily rapidly.
# For example here we compute the inverse transform of F(s) = 1/(s+1) at t = 1
#
# >>> error = Talbot(1,24)-exp(-1)
# >>> error
#   (3.3306690738754696e-015+0j)
#
# Talbot method is very powerful here we see an error of 3.3e-015
# with only 24 function evaluations
#
# Created by Fernando Damian Nieuwveldt      
# email:fdnieuwveldt@gmail.com
# Date : 25 October 2009
#
# Adapted to mpmath and classes by Dieter Kadelka
# email: Dieter.Kadelka@kit.edu
# Date : 27 October 2009
#
# Reference
# L.N.Trefethen, J.A.C.Weideman, and T.Schmelzer. Talbot quadratures
# and rational approximations. BIT. Numerical Mathematics,
# 46(3):653 670, 2006.

from mpmath import mpf,mpc,pi,sin,tan,exp 

# testfunction: Laplace-transform of exp(-t)
def F(s):
  return 1.0/(s+1.0)

class Talbot(object):

  def __init__(self,F=F,shift=0.0):
    self.F = F
    # test = Talbot() or test = Talbot(F) initializes with testfunction F

    self.shift = shift
    # Shift contour to the right in case there is a pole on the 
    #   positive real axis :
    # Note the contour will not be optimal since it was originally devoloped 
    #   for function with singularities on the negative real axis For example
    #   take F(s) = 1/(s-1), it has a pole at s = 1, the contour needs to be 
    #   shifted with one unit, i.e shift  = 1. 
    # But in the test example no shifting is necessary
 
    self.N = 24
    # with double precision this constant N seems to best for the testfunction
    #   given. For N = 22 or N = 26 the error is larger (for this special
    #   testfunction).
    # With laplace.py:
    # >>> test.N = 500
    # >>> print test(1) - exp(-1)
    # >>> -2.10032517928e+21
    # Huge (rounding?) error!
    # with mp_laplace.py
    # >>> mp.dps = 100
    # >>> test.N = 500
    # >>> print test(1) - exp(-1)
    # >>> -5.098571435907316903360293189717305540117774982775731009465612344056911792735539092934425236391407436e-64

  def __call__(self,t):
    
    if t == 0:
      print "ERROR:   Inverse transform can not be calculated for t=0"
      return ("Error");
          
    # Initiate the stepsize
    h = 2*pi/self.N
 
    ans =  0.0
    # parameters from
    # T. Schmelzer, L.N. Trefethen, SIAM J. Numer. Anal. 45 (2007) 558-571
    c1 = mpf('0.5017')
    c2 = mpf('0.6407')
    c3 = mpf('0.6122')
    c4 = mpc('0','0.2645')
      
  # The for loop is evaluating the Laplace inversion at each point theta i
  #   which is based on the trapezoidal rule
    for k in range(self.N):
      theta = -pi + (k+0.5)*h
      z = self.shift + self.N/t*(c1*theta/tan(c2*theta) - c3 + c4*theta)
      dz = self.N/t * (-c1*c2*theta/sin(c2*theta)**2 + c1/tan(c2*theta)+c4)
      ans += exp(z*t)*self.F(z)*dz
          
    return ((h/(2j*pi))*ans).real        
