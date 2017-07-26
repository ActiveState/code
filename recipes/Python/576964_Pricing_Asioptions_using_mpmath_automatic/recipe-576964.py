# -*- coding: iso-8859-1 -*-

# mp_laplace.py
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
# Automatic precision control by D. Kadelka 2009-11-26
#
# Reference
# L.N.Trefethen, J.A.C.Weideman, and T.Schmelzer. Talbot quadratures
# and rational approximations. BIT. Numerical Mathematics,
# 46(3):653 670, 2006.

try:
  import psyco
  psyco.full()
except ImportError:
  print 'Psyco not installed, the program will just run slower'

from mpmath import mp,mpf,mpc,pi,sin,tan,exp,floor,log10

# testfunction: Laplace-transform of exp(-t)
def F(s):
  return 1.0/(s+1.0)

class Talbot(object):

  # parameters from
  # T. Schmelzer, L.N. Trefethen, SIAM J. Numer. Anal. 45 (2007) 558-571
  c1 = mpf('0.5017')
  c2 = mpf('0.6407')
  c3 = mpf('0.6122')
  c4 = mpc('0','0.2645')
  # High precision of these parameters not needed
      
  def __init__(self,F=F,shift=0.0,prec=50):
    self.F = F
    # test = Talbot() or test = Talbot(F) initializes with testfunction F
    # Assumption: F realvalued and analytic

    self.shift = mpf(shift)
    # Shift contour to the right in case there is a pole on the 
    #   positive real axis :
    # Note the contour will not be optimal since it was originally devoloped 
    #   for function with singularities on the negative real axis For example
    #   take F(s) = 1/(s-1), it has a pole at s = 1, the contour needs to be 
    #   shifted with one unit, i.e shift  = 1. 
    # But in the test example no shifting is necessary
 
    self.N = 12
    # with double precision this constant N seems to best for the testfunction
    #   given. For N = 11 or N = 13 the error is larger (for this special
    #   testfunction).

    self.prec = prec
    # calculations with prec more digits

  def __call__(self,t):
  
    with mp.extradps(self.prec):
      t = mpf(t)
      if t == 0:
        print "ERROR:   Inverse transform can not be calculated for t=0"
        return ("Error");
            
      N = 2*self.N
      # Initiate the stepsize (mit aktueller Präsision)
      h = 2*pi/N
   
    # The for loop is evaluating the Laplace inversion at each point theta i
    #   which is based on the trapezoidal rule
      ans =  0.0
      for k in range(self.N):
        theta = -pi + (k+0.5)*h
        z = self.shift + N/t*(Talbot.c1*theta/tan(Talbot.c2*theta) - Talbot.c3 + Talbot.c4*theta)
        dz = N/t * (-Talbot.c1*Talbot.c2*theta/sin(Talbot.c2*theta)**2 + Talbot.c1/tan(Talbot.c2*theta)+Talbot.c4)
        v1 = exp(z*t)*dz
        prec = floor(max(log10(abs(v1)),0))
        with mp.extradps(prec):
          value = self.F(z)
        ans += v1*value
            
      return ((h/pi)*ans).imag

*********************************************************************************
# -*- coding: iso-8859-1 -*-

# asian.py

# Title : Numerical inversion of the Laplace transform for pricing Asian options
#         The Geman and Yor model
# 
# Numerical inversion is done by Asian's method.
#
################################################################################
## Created by Fernando Damian Nieuwveldt                                        
## Date : 26 October 2009                                                      
## email : fdnieuwveldt@gmail.com
## This was part work of my masters thesis (The Asian method not mpmath part) 
## in Applied Mathematics at the University of Stellenbosch, South Africa
## Thesis title : A Survey of Computational Methods for Pricing Asian Options
## For reference details contact me via email.
################################################################################
# Example : 
# Asian(2,2,1,0,0.1,0.02,100)
# 0.0559860415440030213974642963090994900722---mp.dps = 100
# Asian(2,2,1,0,0.05,0.02,250)
# 0.03394203103227322980773---mp.dps = 150
# 
# NB : Computational time increases as the volatility becomes small, because of
#      the argument for the hypergeometric function becomes large
# 
# H. Geman and M. Yor. Bessel processes, Asian options and perpetuities.
# Mathematical Finance, 3:349 375, 1993.
# L.N.Trefethen, J.A.C.Weideman, and T.Schmelzer. Asian quadratures
# and rational approximations. BIT. Numerical Mathematics,
# 46(3):653 670, 2006.

# adapted to mp_laplace by D. Kadelka 2009-11-17
# Automatic precision control by D. Kadelka 2009-11-26
# email: Dieter.Kadelka@stoch.uni-karlsruhe.de

# Example:
# from asian import Asian
# f = Asian()
# print f
# Pricing Asian options: The Geman and Yor model with
#   S = 2, K = 2, T = 1, t = 0, sig = 0.1, r = 0.02
# print f()
# 0.0559860415440029
# f.ch_sig('0.05')
# print f
# Pricing Asian options: The Geman and Yor model with
#   S = 2, K = 2, T = 1, t = 0, sig = 0.05, r = 0.02
# print f()
# 0.0345709175410301
# f.N = 100
# print f()
# 0.0339410537085201
# from mpmath import mp
# mp.dps = 50
# f.update()
# 0.033941053708520319031364170122438704213486236188948

try:
  import psyco
  psyco.full()
except ImportError:
  print 'Psyco not installed, the program will just run slower'

from mpmath import mp,mpf,mpc,pi,sin,tan,exp,gamma,hyp1f1,sqrt,log10,floor
from mp_laplace import Talbot

class Asian(object):

  def G(self,s): # Laplace-Transform
    zz = 2*self.v + 2 + s
    mu = sqrt(self.v**2+2*zz)
    a  = mu/2 - self.v/2 - 1
    b  = mu/2 + self.v/2 + 2
    v1 = (2*self.alp)**(-a)*gamma(b)/gamma(mu+1)/(zz*(zz - 2*(1 + self.v)))
    prec = floor(max(log10(abs(v1)),mp.dps))+self.prec
    # additional precision needed for computation of hyp1f1
    with mp.extradps(prec):
      value = hyp1f1(a,mu + 1,self.beta)*v1
    return value
 
  def update(self):
  # Geman and Yor's variable
  # possibly with infinite precision (strings)
    self.S = mpf(self.parameter['S'])
    self.K = mpf(self.parameter['K'])
    self.T = mpf(self.parameter['T'])
    self.t = mpf(self.parameter['t'])
    self.sig = mpf(self.parameter['sig'])
    self.r = mpf(self.parameter['r'])

    self.v = 2*self.r/(self.sig**2) - 1
    self.alp  = self.sig**2/(4*self.S)*self.K*self.T
    self.beta = -1/(2*self.alp)
    
    self.f.shift = self.shift
 
  def __init__(self,S=2,K=2,T=1,t=0,sig='0.1',r='0.02',N=50,shift=0.0,prec=0):
    # Strings allowed for infinite precision
    # prec compensates rounding errors not catched with automatic precision control
    # parameters may be changed later
    # after changing mp.dps or any of these parameters (except prec, N and t),
    #   update (v,alp,beta depend on these parameters)

    self.N = N  
    self.shift = shift
    self.prec = max(prec,0)
    self.parameter = {'S':S,'K':K,'T':T,'t':t,'sig':sig,'r':r}
  # input: possibly strings with infinite precision
    self.f = Talbot(self.G,shift=self.shift,prec=0)
    self.update()

  def __call__(self):
    # Initialize the stepsize (with actual precision)
    self.f.N = self.N
    tau  = ((self.sig**2)/4)*(self.T - self.t)
    # Evaluation of the integral at tau
    return 4*exp(tau*(2*self.v+2))*exp(-self.r*(self.T - self.t))*self.S/(self.T*self.sig**2)*self.f(tau)

  # Update Parameters
  def ch_S(self,S):
    self.parameter['S'] = S
    self.update()

  def ch_K(self,K):
    self.parameter['K'] = K
    self.update()

  def ch_T(self,T):
    self.parameter['T'] = T
    self.update()

  def ch_t(self,t):
    self.parameter['t'] = t
    self.update()

  def ch_r(self,r):
    self.parameter['r'] = r
    self.update()

  def ch_sig(self,sig):
    self.parameter['sig'] = sig
    self.update()
 
  # Actual Parametes
  def __str__(self):
    s = 'Pricing Asian options: The Geman and Yor model with\n'
    s += "  S = %(S)s, K = %(K)s, T = %(T)s, t = %(t)s, sig = %(sig)s, r = %(r)s" % self.parameter
    return s
   
