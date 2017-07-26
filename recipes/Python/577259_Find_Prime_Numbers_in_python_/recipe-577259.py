    def filterout(L1,L2):
        """ inplace substraction of two lists"""
        for i in L1:
            if i in L2:
                L2.remove(i)


    def is_prime(n):
        """ check if n is prime"""
        i = 2
        if n <=1:
            return False
        Sqrt_Of_n = n**0.5
        while i <= Sqrt_Of_n:
            if n % i == 0:
                return False
            i += 1
        else:
            return True


    def primeGen(n):
        """
        After the first 5 primes the next prime number is the sum of  the last 2
        minus the three prime numbers back
        if it is not a prime number we go for the next one
        
        """
        primes= [2,3,5,7,11]
        if n in xrange(1,len(primes)+1):
            return primes[:n]
        else:
            banlist=[]
            count = 6
            while count <= n :
                Next = (primes[-2] + primes[-1]) - primes[-3]
                if not is_prime(Next):
                    count -=1
                    banlist.append(Next)
                count +=1
                primes.append(Next)
            filterout(banlist,primes)
            return primes


    if __name__ == '__main__':
        print primeGen(1000)
