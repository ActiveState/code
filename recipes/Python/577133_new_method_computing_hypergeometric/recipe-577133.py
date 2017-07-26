################################################################################
## Created by Fernando Damian Nieuwveldt                                        
## Date : 26 October 2009                                                      
## email : fdnieuwveldt@gmail.com
## This was part work of my masters thesis in Applied Mathematics at the
## University of Stellenbosch, South Africa
## Thesis title : A Survey of Computational Methods for Pricing Asian Options
## For reference details contact me via email.
################################################################################
# Example : 
# >>>Hypergeometric1F1(5,2,100-1000j,50)
# (7.0028644420385242e+050+8.9737757674587575e+050j)
#
# using mpmath
# Hypergeometric1F1(-1000,1,1000,2000)
# mpc(real='-2.5938207833620713892854e+215', imag='-1.1411010130233474563877e+202')
#
# Other references :
# A. ErdÃ©lyi, W. Magnus, F. Oberhettinger, and F. Tricomi. Higher
# transcendental functions. Vol. I. Robert E. Krieger Publishing Co.
# Inc., Melbourne, Fla., 1981, pg 273
#
# L.N.Trefethen, J.A.C.Weideman, and T.Schmelzer. Talbot quadratures
# and rational approximations. BIT. Numerical Mathematics,
# 46(3):653 670, 2006.


from mpmath import mp,mpf,mpc,pi,sin,tan,exp,gamma
mp.dps = 100

def F(a,b,t,s):
   
    return s**(-b)*(1+1.0/s)**(a-b)

def Hypergeometric1F1(a,b,t,N):
    
#   Initiate the stepsize
    h = 2*pi/N;  
    
    c1 = mpf('0.5017')
    c2 = mpf('0.6407')
    c3 = mpf('0.6122')
    c4 = mpc('0','0.2645')
    
#   The for loop is evaluating the Laplace inversion at each point theta
#   which is based on the trapezoidal rule
    ans = 0.0
    for k in range(N):
      theta = -pi + (k+0.5)*h
      z    = N/t*(c1*theta/tan(c2*theta) - c3 + c4*theta)
      dz   = N/t*(-c1*c2*theta/sin(c2*theta)**2 + c1/tan(c2*theta)+c4)
      ans += exp(z*t)*F(a,b,t,z)*dz
          
    return gamma(b)*t**(1-b)*exp(t)*((h/(2j*pi))*ans)
