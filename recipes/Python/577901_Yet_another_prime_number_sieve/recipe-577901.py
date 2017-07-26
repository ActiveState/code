primes = lambda n: filter(lambda x, m=set(): not (x in m or m.update(range(x,n,x))), range(2,n))

>>> primes(13)
[2, 3, 5, 7, 11]
