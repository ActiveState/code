'''
N_sim: number of simulations
T: horizon
dt: step length in years
sigma: volatility per year
mu: drift terms (moving average or long-term mean for stock returns)
S0: initial stock price
'''

from numpy.random import standard_normal
from numpy import array, zeros, sqrt, shape
from pylab import *

S0 = 10.222

T =1
dt =0.0002
sigma = 0.4
mu = 1
N_Sim = 10

Steps=round(T/dt); #Steps in years
S = zeros([N_Sim, Steps], dtype=float)
x = range(0, int(Steps), 1)

for j in range(0, N_Sim, 1):
        S[j,0]= S0
        for i in x[:-1]:
                S[j,i+1]=S[j,i]+S[j,i]*(mu-0.5*pow(sigma,2))*dt+sigma*S[j,i]*sqrt(dt)*standard_normal();
        plot(x, S[j])

title('Simulations %d Steps %d Sigma %.6f Mu %.6f S0 %.6f' % (int(N_Sim), int(Steps), sigma, mu, S0))
xlabel('steps')
ylabel('stock price')
show()
