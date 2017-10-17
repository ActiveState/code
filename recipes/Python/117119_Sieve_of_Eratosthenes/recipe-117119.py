# Sieve of Eratosthenes
# Originaly made by : David Eppstein, UC Irvine, 28 Feb 2002
# Performance improvements : Gabriel Freitas, 7 Oct 2017

from itertools import count

def eratosthenes():
    """Yields the sequence of prime numbers via the Sieve of Eratosthenes"""
    yield 2 # force yield the first prime number

    D = {}  # map composite integers to primes witnessing their compositeness
    for q in count(start=3, step=2):
        if q not in D:
            yield q        # not marked composite, must be prime
            D[q*q] = [q]   # first multiple of q not already marked
        else:
            for p in D[q]: # move each witness to its next odd multiple
                D.setdefault(2*p+q,[]).append(p)
            del D[q]       # no longer need D[q], free memory
