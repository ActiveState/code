def primes(n):    
    if n <= 1:
        print('No primes.')        
        return False    
    n = int(n)       
    p = list(range(1,n+1,2)) # in Python 3, range can't be assigned;
    q = len(p)
    p[0] = 2
    for i in range(3,int(n**.5)+1,2):
        if p[(i-1)//2]:            
            p[(i*i-1)//2:q:i] = [0]*((q-(i*i+1)//2)//i+1)           
    return [x for x in p if x]
