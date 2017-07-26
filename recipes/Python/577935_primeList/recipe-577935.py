primeList = lambda n: set([i for i in range(2,n)]) ^ set([i for i in range(2,n) for x in range(2,int(i**0.5)+1) if i%x == 0])
