from itertools import tee, izip, imap, chain, islice, groupby                                                                                                                       
from heapq import merge                                                                                                                                                             
                                                                                                                                                                                    
class DeferredIterator(object):                                                                                                                                                     
    def __iter__(self):                                                                                                                                                             
        for v in self.iterator:                                                                                                                                                     
            yield v                                                                                                                                                                 
                                                                                                                                                                                    
    def setIterator(self, i):                                                                                                                                                       
        self.iterator = i                                                                                                                                                           
                                                                                                                                                                                    
class InfiniteSequence:                                                                                                                                                             
                                                                                                                                                                                    
    def __getitem__(self, idx):                                                                                                                                                     
        if isinstance(idx, slice):                                                                                                                                                  
            return islice(self, idx.start, idx.stop, idx.step)                                                                                                                      
        else:                                                                                                                                                                       
            return next(islice(self, idx, idx+1))                                                                                                                                   
                                                                                                                                                                                    
class Fibonacci(InfiniteSequence):                                                                                                                                                  
    def __iter__(self):                                                                                                                                                             
        R = DeferredIterator()                                                                                                                                                      
        all, p1, p2 = tee(R, 3)                                                                                                                                                     
        results = chain ( [0], all )                                                                                                                                                
        zipped = izip(p1, chain([0], p2))                                                                                                                                           
        mapped = imap( lambda x:  x[0]+x[1], zipped )                                                                                                                               
        R.setIterator ( chain ( [1], (v for v in mapped) ) )                                                                                                                        
        return results                                                                                                                                                              
                                                                                                                                                                                    
class RegularNumbers(InfiniteSequence):             
    #Solutions to 2**i * 3**j * 5**k for some integers i, j and k                                                                                                                
    def __iter__(self):                                                                                                                                                             
        R = DeferredIterator()                                                                                                                                                      
        result, p2, p3, p5 = tee (R, 4)                                                                                                                                             
        m2 = (2*x for x in p2)                                                                                                                                                      
        m3 = (3*x for x in p3)                                                                                                                                                      
        m5 = (5*x for x in p5)                                                                                                                                                      
        merged = merge(m2,m3,m5)                                                                                                                                                    
        combined = chain([1], merged)                                                                                                                                               
        R.setIterator( (k for k,v in groupby(combined)) )                                                                                                                           
                                                                                                                                                                                    
        return result                                                                                                                                                               
                                                                                                                                                                                    
                                                                                                                                                                                    
fib = Fibonacci()                                                                                                                                                                   
for f in fib[0:15]:                                                                                                                                                                 
    print f                                                                                                                                                                         
                                                                                                                                                                                    
reg = RegularNumbers()                                                                                                                                                              
for r in reg[0:15]:                                                                                                                                                                 
    print r  
