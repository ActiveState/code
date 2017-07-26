# Name : Alexander Baker
# Date : 2nd December 2008
# Description : based on Newton Raphson method of root finding, based on 
#   x_{n+1} = x_{n} - f(x_{n})/df(x_{n})/dx
# http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html#scipy.optimize.newton
# http://pathfinder.scar.utoronto.ca/~dyer/csca57/book_P/node35.html

import scipy.optimize
from scipy import optimize

def q(x):
    return (3.0-x)*scipy.exp(x) - 3.0
    
def qprime(x):
    return (2.0-x)*scipy.exp(x)    

print scipy.optimize.newton(q, 5, qprime, maxiter=500)
