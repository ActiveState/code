'''

Rabin-Miller algorithm for testing the primality of a given number, and
an associated algorithm for generating a b-bit integer that is probably
prime.

Algorithm described in various texts, among them Algorithm Design by
Goodrich and Tamassia.

Copyleft 2005, Josiah Carlson
Use this recipe as you see fit.

'''

import random
import sys

DEBUG = False


def ipow(a,b,n):
    #calculates (a**b)%n via binary exponentiation, yielding itermediate
    #results as Rabin-Miller requires
    A = a = long(a%n)
    yield A
    t = 1L
    while t <= b:
        t <<= 1
    
    #t = 2**k, and t > b
    t >>= 2
    
    while t:
        A = (A * A)%n
        if t & b:
            A = (A * a) % n
        yield A
        t >>= 1

def RabinMillerWitness(test, possible):
    #Using Rabin-Miller witness test, will return True if possible is
    #definitely not prime (composite), False if it may be prime.
    
    return 1 not in ipow(test, possible-1, possible)

smallprimes = (3,5,7,11,13,17,19,23,29,31,37,41,43,
               47,53,59,61,67,71,73,79,83,89,97)

def generate_prime(b, k=None):
    #Will generate an integer of b bits that is probably prime.
    #Reasonably fast on current hardware for values of up to around 512 bits.
    
    bits = int(b)
    assert bits > 1
    if k is None:
        k = 2*bits
    k = int(k)
    if k < 64:
        k = 64
    if DEBUG: print "(b=%i, k=%i)"%(bits,k),
    good = 0
    while not good:
        possible = random.randrange(2**(bits-1)+1, 2**bits)|1
        good = 1
        if DEBUG: sys.stdout.write(';');sys.stdout.flush()
        for i in smallprimes:
            if possible%i == 0:
                good = 0
                break
        else:
            for i in xrange(k):
                test = random.randrange(2, possible)|1
                if RabinMillerWitness(test, possible):
                    good = 0
                    break
                if DEBUG: sys.stdout.write('.');sys.stdout.flush()
    if DEBUG: print
    return possible

if __name__ == '__main__':
    DEBUG = True
    print "; - trying new possible prime"
    print ". - failed to find a composite witness for this trial"
    print
    bits = 32
    while bits < 547:
        print hex(generate_prime(bits))
        bits = int(bits*1.5)
