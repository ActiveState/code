"""
    Prime number generator

I found it quite simple to implement this generator with the 'any' function
It is certainly not the most optimized algorithm.
Primes list will only grow in the function though.

"""
import itertools

def primes():
    """Simple prime numbers generator

    >>> [prime for prime, index in zip(primes(), range(10))]
    [1, 2, 3, 5, 7, 11, 13, 17, 19, 23]
    """
    yield 1
    primes = []
    for n in itertools.count(2):
        if not any(n % p == 0 for p in primes):
            # No divisor found among previous primes
            yield n
            primes.append(n)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
