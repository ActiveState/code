'''
Created on 16 Apr 2013

@author: bakera

'''

import unittest

import numpy as np
from math import pow
from scipy import special
from scipy.linalg import eig


class HartreeFock(object):
    '''
       simple HF SCF algorithm
    '''
    
    def iterate_basis_functions(self,j=0):
        for i in np.arange(j,self.basis_function_count,1):
            yield i
            
    def iterate_primitives_functions(self):
        for i in np.arange(0,self.primitive_count,1):
            yield i
    
    def F0(self, t):
        '''    
            error function
        '''
        if t < 1e-6 :
            return 1.0-t/3
        else:            
            return (1.0/2.0)*np.sqrt(np.pi/t)*special.erf(np.sqrt(t))
    
    def __init__(self, R=1.4632):
    
        # counters, 2 is basis functions
        self.basis_function_count = 2
        # made from each , 3 contacted gaussian functions
        self.primitive_count = 3        
    
        #
        # gaussian a.e^-((x-b)^2)/c), a height, b center, c std 
        #
    
        # zeta is know as the width of the function, or c?
    
        # 3 primitive gaussians, two fitted values exponent d and contraction coefficient
        # a
        self.d = np.array([0.444635, 0.535328, 0.1543329])
        self.a = np.array([0.109818, 0.405771, 2.22766])
        
        self.zeta_he = 2.0925
        self.zeta_h = 1.24
        
        self.a_he = pow(self.zeta_he,2.0)*self.a
        self.a_h = pow(self.zeta_h,2.0)*self.a
        
        self.R = R        
        self.a_prime = np.array([self.a_he, self.a_h]).ravel()        
        self.r_prime = np.array([0,0,0,self.R,self.R,self.R])
        
        # nuclear charge he, h
        self.Z = np.array([2.0,1.0])

        self.S = np.zeros((self.basis_function_count,self.basis_function_count), dtype=float)
        self.T = np.zeros((self.basis_function_count,self.basis_function_count), dtype=float)
        self.V1 = np.zeros((self.basis_function_count,self.basis_function_count), dtype=float)
        self.V2 = np.zeros((self.basis_function_count,self.basis_function_count), dtype=float)
        self.H = np.zeros((self.basis_function_count,self.basis_function_count), dtype=float)    
    
        self.I = np.zeros((self.basis_function_count,self.basis_function_count,self.basis_function_count,self.basis_function_count), dtype=float)
    
        # convergence criteria
        self.dP = 1e-4
        self.maximum_iterations = 20
    
    def generate(self,i,j,p,q):
        a1 = self.a_prime[self.primitive_count*(i)+p] 
        a2 = self.a_prime[self.primitive_count*(j)+q] 
        r1 = self.r_prime[self.primitive_count*(i)+p] 
        r2 = self.r_prime[self.primitive_count*(j)+q] 
        return a1, a2, r1, r2
    
    def product_two_gaussians(self, a1, a2, r1, r2):
        '''
            a1 : float
            
                denotes the contraction coefficient of each gaussian or exponent.
        
            r1 : float
            
                denotes the center location of one of the gaussians
                
            r2 : float
            
                denotes the ceter location of second gaussion
                
            return : 
            
                as : float
                
                    sum of the two centers
                    
                ap : float
                
                    product of the two centers
                    
                disp : float
                
                    displacement of two gaussian centers
        '''                
        asum = a1+a2
        aproduct = a1*a2
        dist = r1-r2        
        rp = (a1*r1+a2*r2)/(a1+a2)
        return asum, aproduct, dist, rp
    
    def orthogonalize(self):
        '''
        
        '''
        x = np.zeros((2,2), dtype=float)
        s_invroot = np.zeros((2,2), dtype=float)
        
        s,U = eig(self.S)    
        U = np.matrix([[2**-0.5,2**-0.5],[2**-0.5,-1*2**-0.5]])
                
        #for i in self.iterate_basis_functions():
        #    s_invroot[i,i] = pow(s[i]+0j,-0.5)
        
        s_invroot[0,0] = pow(s[1]+0j,-0.5)
        s_invroot[1,1] = pow(s[0]+0j,-0.5)
        
        #print 's_invroot', s_invroot                
        x = U*s_invroot
        
        return U,s,x
    
    def scf(self):
                
        U,s,X = self.orthogonalize()
        #print 'U:',U
        #print 's',s
        #print 'X',X        
        
        P = np.zeros((2,2), dtype=float)
        
        #
        # enter the SCF loop
        #
        
        F = np.zeros((2,2), dtype=float)
        count = 0
        sigma = 1
        
        while sigma > self.dP:
            
            P_prev = P
            count += 1
            
            #
            # build G matrix
            #
            G = np.zeros((2,2), dtype=float)
            for i in self.iterate_basis_functions():
                for j in self.iterate_basis_functions():
                    for p in self.iterate_basis_functions():
                        for q in self.iterate_basis_functions():
                            G[i,j] += P[p,q]*(self.I[i,q,j,p]-0.5*self.I[i,q,p,j])
            
            
            F = np.matrix(self.H + G)
            
            #print 'Fock Matrix',F
            
            Fp = np.matrix(X.T)*np.matrix(F)*np.matrix(X)
            
            #print 'F prime', Fp
            
            eps, Cp = eig(Fp)
            C = np.matrix(X)*np.matrix(Cp)
            
            P = np.zeros((2,2), dtype=float)
            for i in self.iterate_basis_functions():
                for j in self.iterate_basis_functions():
                    P[i,j] += 2*C[i,0]*C[j,0]
            
            sigma = 0
            for i in self.iterate_basis_functions():
                for j in self.iterate_basis_functions():
                    sigma += (P[i,j]-P_prev[i,j])**2
        
            sigma = ((1.0/4.0)*sigma)**(0.5)
            
            if sigma >= self.maximum_iterations:
                sigma = 0
                
            E = 0
            for i in self.iterate_basis_functions():
                for j in self.iterate_basis_functions():
                    E += 0.5*P_prev[i,j]*(self.H[j,i]+F[j,i])            
            
            Etot = E + max(np.cumprod(self.Z))/self.R
            yield count, P, E, Etot, F, Fp, P*np.matrix(self.S)
                  
                
    def compute_integrals(self):
        
        #
        #    simple method to evaluate the overlap matrix
        #    

        #
        # iterate the basis functions
        #
        
        for i in self.iterate_basis_functions():
            for j in self.iterate_basis_functions(i):
                for p in self.iterate_primitives_functions():
                    for q in self.iterate_primitives_functions():
                        
                        a1, a2, r1, r2 = self.generate(i, j, p, q)                        
                        asum, aproduct, dist, rp = self.product_two_gaussians(a1, a2, r1, r2)                                                                                    
                        rat = (aproduct/asum)
                        
                        #print 'asum, aproduct, dist, rp,rat ', asum, aproduct, dist, rp , rat
                        
                        #
                        # overlap matrix S[i,j]
                        #
                        s_pq = pow(2,1.5)*pow(rat/asum, 0.75)*pow(np.e, (-1.0*rat*pow(dist,2.0)))                                   
                        self.S[i,j] += self.d[p]*self.d[q]* s_pq
                                                                        
                        #
                        # kinetic energy matrix T[i,j]
                        #
                        self.T[i,j] += self.d[p] * self.d[q] * rat * (self.primitive_count-2*rat*pow(dist,2))*s_pq
                        
                        #
                        # Nuclear potential of He
                        #
                        self.V1[i,j] += self.d[p] * self.d[q] * pow((2.0/np.pi), 3.0/2.0)*pow((aproduct), 3.0/4.0)*-2.0*(np.pi/asum)*self.Z[0]*pow(np.e, -1*(aproduct/asum)*dist**2)*self.F0(asum*rp**2)
                        
                        #
                        # Nuclear potentail of H 
                        #
                        self.V2[i,j] += self.d[p] * self.d[q] * pow((2.0/np.pi), 3.0/2.0)*pow((aproduct), 3.0/4.0)*-2.0*(np.pi/asum)*self.Z[1]*pow(np.e, -1*(aproduct/asum)*dist**2)*self.F0(asum*(rp-self.R)**2)
                       
                        
                # reflection in the trace diagonal                        
                self.S[j,i] = self.S[i,j]
                self.T[j,i] = self.T[i,j]        
                self.V1[j,i] = self.V1[i,j] 
                self.V2[j,i] = self.V2[i,j]        

        #4 build the Hamiltonian
        self.H = self.T + self.V1 + self.V2

        #
        # calculate the 2 electron integrals
        #

        for i in self.iterate_basis_functions():
            for j in self.iterate_basis_functions(i):
                for k in self.iterate_basis_functions(i):
                    for l in self.iterate_basis_functions(k):
                        
                        self.I[i,j,k,l] = 0.0
                        
                        for p in self.iterate_primitives_functions():
                            for q in self.iterate_primitives_functions():
                                for r in self.iterate_primitives_functions():
                                    for s in self.iterate_primitives_functions():
                                        
                                        a1, a2, r1, r2 = self.generate(i, j, p, q)                        
                                        a3, a4, r3, r4 = self.generate(k, l, r, s)
                                        
                                        asum1 = a1+a3
                                        asum2 = a2+a4
                                        asum = asum1 + asum2
                                        aproduct = a1 * a2 * a3 * a4                                        
                                        rat1 = (a1*a3)/asum1
                                        rat2 = (a2*a4)/asum2
                                        rp = (a1*r1 + a3*r3)/asum1                                                
                                        rq = (a2*r2+a4*r4)/asum2
                                        
                                        dist1 = r1-r3
                                        dist2 = r2-r4
                                        dist = rp-rq
                                        
                                        #print i,j,k,l, p,q,r,s , a1, a2, r1, r2, a3, a4, r3, r4                                                                            
                        
                                        self.I[i,j,k,l] +=  self.d[p]*self.d[q]*self.d[s]*self.d[r] * 16.0/(np.sqrt(np.pi))*(pow(aproduct,3.0/4.0)/(asum1*asum2*np.sqrt(asum)))*pow(np.e,-1*rat1*dist1**2-rat2*dist2**2)*self.F0(asum1*asum2/asum*dist**2)
                        
                        #
                        # figure out why this set of parameters...todo
                        #
                        
                        self.I[i,l,k,j] = self.I[i,j,k,l]
                        self.I[j,i,l,k] = self.I[i,j,k,l]
                        self.I[j,k,l,i] = self.I[i,j,k,l]
                        self.I[k,j,i,l] = self.I[i,j,k,l]
                        self.I[k,l,i,j] = self.I[i,j,k,l]
                        self.I[l,i,j,k] = self.I[i,j,k,l]
                        self.I[l,k,j,i] = self.I[i,j,k,l]

class Test(unittest.TestCase):


    def testOverlapMatrix(self):
        '''
            Longer bond length R=2.5, S(1,2) = S(2,1) gets smaller
            less chance of electrons being between atoms
        '''
        vv = HartreeFock()        
        vv.compute_integrals()
        print 'Overlap matrix S', np.round(vv.S,4)
        
        S = np.array([[1.00000615,0.4507713],[0.4507713, 1.00000615]])
        assert(np.round(vv.S,4) == np.round(S,4)).all()        

    def testKineticEnergyMatrix(self):
        vv = HartreeFock()
        vv.compute_integrals()
        print 'Kinertic Energy matrix T', np.round(vv.T,4)
        
        T = np.array([[2.16434304,0.16701271],[0.16701271, 0.76004365]])
        assert(np.round(vv.T,4) == np.round(T,4)).all()

    def testNuclearPotential(self):
        vv = HartreeFock()
        vv.compute_integrals()        
        
        print 'Nuclear Energy matrix (He) T', np.round(vv.V1,4)
        print 'Nuclear Energy matrix (H) T', np.round(vv.V2,4)
        print 'Hamiltonian(core) of single electron in field of the nuclear point charges', np.round(vv.H,4)
        
        print '2 electron integrals ', vv.I
        
        for count, P, E, F, Fp, Etot, PS in vv.scf():
            print 'iteration', count, 'Density Matrix', P[0,0], P[0,1], P[1,1], 'Energy',E, Etot, PS
        
    def testRadiusVary(self):
        
        test_results = {}
        
        for r in np.arange(0.1,3.5,0.01):
            print 'radius :',r
            vv = HartreeFock(R=r)
            vv.compute_integrals()            
            test_results[r] = max([(count, Etot) for count, P, E, Etot, F, Fp, PS in vv.scf()])
              
        radius = [k for k,v in test_results]  
        energy = [v[1] for k,v in test_results]  
        
        print radius, energy
        
        #
        # visualise data, comment back in.
        #
        
        #from pandas import DataFrame, Series
        #from pylab import show        
        #d = {'HeH' : Series(energy, index=radius)}
        #df = DataFrame(d)
        #df.plot(style='r-+')
        #df.to_csv('hehplus.csv')
        #show()                     
        
    def testHelperFunctionErf(self):
        print round(HelperFunctions.F0(t=0.01),2) == 0.75

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
