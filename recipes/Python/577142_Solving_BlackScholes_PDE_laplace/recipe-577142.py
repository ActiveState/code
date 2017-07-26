## Laplace inversion of a European option
## Fernando Nieuwveldt
## email: fdnieuwveldt@gmail.com
## Example :
## >>> BSLaplace(8.0,10.0,1,0,0.03,0.3,50,1)
## mpf('0.4123752414202130413263844663926875')
## Referenece:
## A Survey of computational methods for pricing Asian options,masters thesis
## Fernando Nieuwveldt, University of Stellenbosch, South Africa

from mpmath import mp,mpf,mpc,pi,sin,tan,sqrt,exp,ln
mp.dps = 32
  
def bs(x,b1,b2,eps1,eps2,s,r,phi):
    """phi = 1 for a call -1 for a put"""    
    if x <= 0:
       return b1*exp(eps1*x) + (phi-1)/2*(exp(x)/s - 1/(s + r))
    else:
       return b2*exp(eps2*x) + (phi+1)/2*(exp(x)/s - 1/(s + r))

def BSLaplace(S,K,T,t,r,sig,N,phi): 
        """Solving the Black Scholes PDE in the Laplace domain"""
        x   = ln(S/K)     
        r = mpf(r);sig = mpf(sig);T = mpf(T);t=mpf(t)
        S = mpf(S);K = mpf(K);x=mpf(x)
        mu  = r - 0.5*(sig**2)
       
        tau = T - t   
        c1 = mpf('0.5017')
        c2 = mpf('0.6407')
        c3 = mpf('0.6122')
        c4 = mpc('0','0.2645')        
        
        ans = 0.0
        h = 2*pi/N
        h = mpf(h)
        for k in range(N/2): # Use symmetry
            theta = -pi + (k+0.5)*h
            z     =  N/tau*(c1*theta/tan(c2*theta) - c3 + c4*theta)
            dz    =  N/tau*(-c1*c2*theta/(sin(c2*theta)**2) + c1/tan(c2*theta)+c4)
            eps1  =  (-mu + sqrt(mu**2 + 2*(sig**2)*(z+r)))/(sig**2)
            eps2  =  (-mu - sqrt(mu**2 + 2*(sig**2)*(z+r)))/(sig**2)
            b1    =  1/(eps1-eps2)*(eps2/(z+r) + (1 - eps2)/z)
            b2    =  1/(eps1-eps2)*(eps1/(z+r) + (1 - eps1)/z)
            ans  +=  exp(z*tau)*bs(x,b1,b2,eps1,eps2,z,r,phi)*dz
            val = (K*(h/(2j*pi)*ans)).real
           
            
        return 2*val
