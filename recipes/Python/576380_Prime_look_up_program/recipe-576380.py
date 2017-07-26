#!/usr/bin/python
""" nth prime """

import cPickle, math, sys,  os

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
fn = 'myPrimes'
interval = 123456

def fmt_n(n):
    """
    formats an integer
    input: integer
    return: string
    """
    nstr = '%d' % (n)
    nlist = list(nstr)
    for pos in range(len(nstr) - 3, 0, -3):
        nlist.insert(pos, ',')
    return ''.join(nlist)


def isprime(n):
    """
    tells if n is prime
    input: number
    return boolean
    """
    global primes
    limit = int(math.sqrt(n))
    for prime in primes:
        if prime > limit:
            return True
        if n % prime == 0:
            return False
    raise ValueError, "Not enough primes"


def ith_prime(i):
    """
    gets prime(i)
    input: number
    return: number
    """
    global primes, interval
    while i >= len(primes):
        a = ((primes[-1] + 2) // 6) * 6 - 1
        b = a + interval
        c = a + 2
        d = b + 2
        try:
            primes.extend(filter(isprime, xrange(a, b, 6)))
            primes.extend(filter(isprime, xrange(c, d, 6)))
            primes = sorted(list(set(primes)))
            mpp = open(fn, 'w')
            cPickle.dump(primes, mpp, protocol = -1)
            mpp.close()
            print 'Prime[%s] = %s' % (fmt_n(len(primes)), fmt_n(primes[-1]))
        except ValueError:
            interval = interval // 2
    return primes[i]


def do_input(s):
    try:
        i = int(s)

    except ValueError:
        i = len(primes) + 1

    print 'Prime[%s] = %s.' % (fmt_n(i), fmt_n(ith_prime(i)))


if __name__ == '__main__':
    try:
        mpp = open(fn, 'rb')
        primes = cPickle.load(mpp)
        mpp.close()

    except IOError, e:
        print '* ERROR * Could not open %s for load.%se = %s' % (fn, os.linesep,  e)

    print 'Prime(%s) = %s' % (fmt_n(len(primes)), fmt_n(primes[-1]))
    for s in sys.argv[1:]:
        do_input(s)
