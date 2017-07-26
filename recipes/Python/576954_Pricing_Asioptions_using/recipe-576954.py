# Title : Numerical inversion of the Laplace transform for pricing Asian options
#         The Geman and Yor model
# 
# Numerical inversion is done by Talbot's method.
#
################################################################################
## Created by Fernando Damian Nieuwveldt                                        
## Date : 26 October 2009                                                      
## email : fdnieuwveldt@gmail.com
## This was part work of my masters thesis (The Talbot method not mpmath part) 
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
# L.N.Trefethen, J.A.C.Weideman, and T.Schmelzer. Talbot quadratures
# and rational approximations. BIT. Numerical Mathematics,
# 46(3):653 670, 2006.


from mpmath import mp,mpf,mpc,pi,sin,tan,exp,gamma,hyp1f1,sqrt

def Asian(S,K,T,t,sig,r,N):

#   Assigning multi precision
    S   = mpf(S); K = mpf(K)
    sig = mpf(sig)
    T   = mpf(T); t = mpf(t)
    r   = mpf(r)
      
    
#   Geman and Yor's variable
    tau  = mpf(((sig**2)/4)*(T - t))
    v    = mpf(2*r/(sig**2) - 1)
    alp  = mpf(sig**2/(4*S)*K*T)
    beta = mpf(-1/(2*alp))
    tau  = mpf(tau)
    N    = mpf(N)
    
#   Initiate the stepsize
    h = 2*pi/N;
    mp.dps = 100

    c1 = mpf('0.5017')
    c2 = mpf('0.6407')
    c3 = mpf('0.6122')
    c4 = mpc('0','0.2645')
    
#   The for loop is evaluating the Laplace inversion at each point theta which is based on the trapezoidal
#   rule
    ans = 0.0
    
    for k in range(N/2):                # N/2 : symmetry 
      theta = -pi + (k+0.5)*h
      z     = 2*v+2 + N/tau*(c1*theta/tan(c2*theta) - c3 + c4*theta)
      dz    = N/tau*(-c1*c2*theta/sin(c2*theta)**2 + c1/tan(c2*theta)+c4)
      zz    = N/tau*(c1*theta/tan(c2*theta) - c3 + c4*theta)      
      mu    = sqrt(v**2+2*z)
      a     = mu/2 - v/2 - 1
      b     = mu/2 + v/2 + 2
      G     = (2*alp)**(-a)*gamma(b)/gamma(mu+1)*hyp1f1(a,mu + 1,beta)/(z*(z - 2*(1 + v)))
      ans  += exp(zz*tau)*G*dz
          
    return 2*exp(tau*(2*v+2))*exp(-r*(T - t))*4*S/(T*sig**2)*h/(2j*pi)*ans 
