"""
A Fun Widget Class For Playing With Prime, Perfect and Fibonacci Numbers

"""

class PrimePerFib:
    
    def __init__(self):
        pass
        
  
    def Factor(self, n):
      yield 1  
      i = 2  
      limit = n**0.5  
      while i <= limit:  
        if n % i == 0:  
          yield i  
          n = n / i  
          limit = n**0.5  
        else:  
          i += 1  
      if n > 1:  
        yield n  
            
            
    def PrimeFactor(self, n):
        for x in self.Factor(n):
            if x != 1 and x != n:
                return False
        return True

    """
    A Hybrid Sieve of Atkin, without all the quadratics and keeping of sequences
    allows for generating blocks of primes
    """
    def PrimeGen(self, count, start):
        c     = 0
        base  = [2,3,5]
        start = int(round(start))
              
        n = (2,max(2,(start,start+1)[start % 2 == 0]))[start != 2]
        
        while c < count:
                  
            if n in base:
                yield n
                if n == 2: n+=1; c+=1; continue
                else: n+=2; c+=1; continue
                
            if not [m for m in base if (n%60) % m == 0 ]:
                if n % n**0.5 != 0:
                    if self.PrimeFactor(n):
                        c += 1
                        yield n
            n += 2
            
            
                    
    def PrimeGet(self, num):
        r = self.PrimeGen(1,num).next()
        return r
    
    
    def IsPrime(self, num):
        return (False,True)[self.PrimeGet(num)==num]
    
      
    def NextPrime(self, num):
        return (self.PrimeGet(num),self.PrimeGet(num+1))[self.IsPrime(num)]
        

    def PerfectGen(self, count, start=0):
        output = 0
        prime  = 0 
        while output < count:
            prime = self.NextPrime(prime)
            mPrime = 2**prime - 1

            if not self.IsPrime(mPrime):
                continue
            
            pN =(2**(prime-1))*(2**prime - 1)
            if pN >= start:
                output += 1
                yield pN
                
                    
    def PerfectGet(self, num):
        return self.PerfectGen(1,num).next()
    
    
    def IsPerfect(self, num):
        return (False,True)[self.PerfectGet(num)==num]
    
    
    def NextPerfect(self, num):
        return (self.PerfectGet(num),self.PerfectGet(num+1))[self.IsPerfect(num)]
                
    
    def FibonacciGen(self, count, start=0):
        output = 0
        fib    = [0,1]
        while output < count:
            fN = fib[len(fib)-1] + fib[len(fib)-2]
            fib.append(fN)
            fib.pop(0)
            if fN >= start:
                output += 1
                yield fN
             
        
    def FibonacciGet(self, num):
        return self.FibonacciGen(1,num).next()
    

    def IsFibonacci(self, num):
        return (False,True)[self.FibonacciGet(num)==num]

    
    def NextFibonacci(self, num):
        return (self.FibonacciGet(num),self.FibonacciGet(num+1))[self.IsFibonacci(num)]
       

if __name__ == '__main__':
    
    PPF = PrimePerFib()
    
    ##########################################################################
    #Prime Numbers
    
    print "What Prime Number Comes After 56? ",PPF.NextPrime(56)
    print "Is 333 A Prime Number? ",PPF.IsPrime(333)

    Primes = []
    for Prime in PPF.PrimeGen(10,42):
        Primes.append(Prime)
        
    print "Generated Primes: ",Primes,"\n\n"
    
    ##########################################################################
    #Perfect Numbers
    #Need Some Horsepower In Your Machine To Play With These
    
    print "What Perfect Number Comes After 9685 ",PPF.NextPerfect(9685)
    print "Is 8128 A Perfect Number ",PPF.IsPerfect(8128)
    
    Perfects = []
    for Perfect in PPF.PerfectGen(8, 0):
        Perfects.append(Perfect)
        
    print "Generated Perfect Numbers ",Perfects,"\n\n"
    
    ##########################################################################
    #Fibonacci Numbers
    
    print "What is the Next Fibonacci Number After 5 ? ",PPF.NextFibonacci(5)
    print "Is 16 A Fibonacci Number? ",PPF.IsFibonacci(16)
    
    Fibonaccis = []
    for Fibonacci in PPF.FibonacciGen(42, 10):
        Fibonaccis.append(Fibonacci)
        
    print "Generated Fibonacci Numbers ",Fibonaccis
        
    
