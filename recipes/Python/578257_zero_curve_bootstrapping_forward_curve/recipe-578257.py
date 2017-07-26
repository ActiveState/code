#
# Description: example of a bootstrapping and forward curve generation
# script, this can be used to build a set of curves for different currencies
# TODO: include some spline smoothing to the zero curve, from first principles!
#

from sympy.solvers import solve
from sympy import Symbol, abs, Real
x = Symbol('x', real=True)

import pylab as pylab

def g(yieldCurve, zeroRates,n, verbose):
    '''
        generates recursively the zero curve 
        expressions eval('(0.06/1.05)+(1.06/(1+x)**2)-1')
        solves these expressions to get the new rate
        for that period
    
    '''
    if len(zeroRates) >= len(yieldCurve):
        print "\n\n\t+zero curve boot strapped [%d iterations]" % (n)
        return
    else:
        legn = ''
        for i in range(0,len(zeroRates),1):
            if i == 0:
                legn = '%2.6f/(1+%2.6f)**%d'%(yieldCurve[n], zeroRates[i],i+1)
            else:
                legn = legn + ' +%2.6f/(1+%2.6f)**%d'%(yieldCurve[n], zeroRates[i],i+1)
        legn = legn + '+ (1+%2.6f)/(1+x)**%d-1'%(yieldCurve[n], n+1)
        # solve the expression for this iteration
        if verbose:
            print "-[%d] %s" % (n, legn.strip())
        rate1 = solve(eval(legn), x)
        # Abs here since some solutions can be complex
        rate1 = min([Real(abs(r)) for r in rate1])
        if verbose:
            print "-[%d] solution %2.6f" % (n, float(rate1))
        # stuff the new rate in the results, will be 
        # used by the next iteration
        zeroRates.append(rate1)
        g(yieldCurve, zeroRates,n+1, verbose)
        
verbose = True
tenors = [.1,.25,0.5,1,2,3,5,7,10,20,30]
#
# money market, futures, swap rates
#
yieldCurve = [0.07,	0.09,	0.15,	0.21,	0.37,	0.57,	1.13,	1.70,	2.31,	3.08	,3.41]

#yieldCurve = [0.05, 0.06, 0.07, 0.08 ,0.085 ,0.0857 ,0.0901,0.0915,0.0925,0.0926,0.0934,0.0937]
zeroRates = [yieldCurve[0]] # TODO: check that this is the correct rate

print "\n\n\tAlexander Baker, March 2012\n\tYield Curve Bootstrapper\n\tAlexander Baker\n\n"

# kick off the recursive code
g(yieldCurve, zeroRates, 1, verbose)
print "\tZeroRate Array",zeroRates

pylab.plot(tenors,yieldCurve)
pylab.plot(tenors,zeroRates)
pylab.show()
