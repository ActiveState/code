"""
 Topic: prime algorithms.
 Here is an example output of this script:

 Totally free. No warranty.

Python 3.1.2 (r312:79149, Mar 21 2010, 00:41:52) [MSC v.1500 32 bit (Intel)]

 [calc_slower]
 seeking primes between (0..100000) ...
 ...profiling of 'create_primes_1': tooks 6.974707 seconds
 ...profiling of 'create_primes_2': tooks 0.195253 seconds
 ...profiling of 'create_primes_3': tooks 0.090312 seconds
 ...profiling of 'create_primes_4': tooks 0.062241 seconds
 ...profiling of 'create_primes_5': tooks 0.046717 seconds
 ...profiling of 'create_primes_6': tooks 0.024859 seconds
 done - 9592 primes found.

 [calc_medium]
 seeking primes between (0..1000000) ...
 ...profiling of 'create_primes_2': tooks 4.662721 seconds
 ...profiling of 'create_primes_3': tooks 1.133545 seconds
 done - 78498 primes found.

 [calc_faster]
 seeking primes between (0..10000000) ...
 ...profiling of 'create_primes_3': tooks 13.872371 seconds
 ...profiling of 'create_primes_4': tooks 7.766646 seconds
 ...profiling of 'create_primes_5': tooks 6.069688 seconds
 done - 664579 primes found.

Are there no better solutions? ... smile ... Of course there are many!
But unfortunately some of them require a much better understanding in
math and I'm afraid (for myself) that some explanations are not simple
enough so I can present them here.
"""
import sys
import time
import math

def profile(function):
    """ intended to be used as decorator for a function or a method to check
        the execution time """

    def decorate(args):
        """ concrete decorator measuring the execution time of
            given function or method """
        start = time.clock()
        result = function(args)
        print("...profiling of '%s': tooks %f seconds" \
              % (function.__name__, time.clock()-start))
        #print("  -> %s" % (function.__doc__))
        return result
    return decorate


def is_prime(val):
    """ simple check for a prime value.
        Note: as a function called several time it is expensive. """
    if val <= 1:
        return False
    if val == 2:
        return True
    if val % 2 == 0:
        return False

    for divisor in range(3, int(math.sqrt(val))+1, 2):
        if val % divisor == 0:
            return False

    return True


@profile
def create_primes_1(max_n):
    """ creating primes up to a maximum value. The even numbers are not
        touched. The primes itself are used to check for possible division. """
    primes = []
    for val in range(3, max_n+1, 2):
        found = False
        for divisor in primes:
            if val % divisor == 0:
                found = True
                break

        if not found:
            primes.append(val)
    return [2] + primes


@profile
def create_primes_2(max_n):
    """ creating primes up to a max. value calling 'is_prime' for each value. """
    primes = [2]+[val for val in range(3, max_n+1, 2) if is_prime(val)]
    return primes

@profile
def create_primes_3(max_n):
    """ using sieve of sundaram:
        http://en.wikipedia.org/wiki/Sieve_of_Sundaram
        The description was really understandable   """
    limit    = max_n + 1
    sieve    = [True] * (limit)
    sieve[1] = False

    for i in range(1, limit//2):
        f = 2 * i + 1
        for j in range(i, limit//2):
            k = i + j * f
            if k <= max_n:
                sieve[k] = False
            else:
                break

    return [2,3]+[2*k+1 for k in range(1, int(max_n/2)) if sieve[k]]

@profile
def create_primes_4(max_n):
    """ creating primes up to a maximum value using a sieve algorithm. All
        multiples of a prime are flagged as 'no prime'. In addition there
        is an optimization by ignoring values flagged as none prime when
        proceeding to next value."""
    sieve = [True] * (max_n+1) # default: all are primes
    sieve[0] = False           # init:    0 is not a prime
    sieve[1] = False           # init:    1 is not a prime

    val = 2
    while val <= max_n:
        factor = val
        # strike out values not being a prime
        noprime = val * factor
        while noprime <= max_n:
            sieve[noprime] = False
            factor += 1
            noprime = val * factor
        # next value
        val += 1
        while val <= max_n and sieve[val] == False:
            val += 1

    return [n for n in range(max_n) if sieve[n] == True]


@profile
def create_primes_5(max_n):
    """ creating primes up to a maximum value using a sieve algorithm. All
        multiples of a prime are flagged as 'no prime'. In addition there
        is an optimization by ignoring values flagged as none prime when
        proceeding to next value."""
    sieve  = [False, True] * (int(max_n / 2))
    sieve += [True]

    if not max_n % 2 == 0:
        sieve += [False]


    sieve[1] = False
    sieve[2] = True
    primes   = [2]

    val = 3
    while val <= max_n:
        # now we have one prime
        primes.append(val)
        # strike out values not being a prime
        noprime = val + val
        while noprime <= max_n:
            sieve[noprime] = False
            noprime += val
        # next value
        val += 1
        while val <= max_n and sieve[val] == False:
            val += 1

    return primes


@profile
def create_primes_6(max_n):
    """ creating primes up to a maximum value using a sieve algorithm. All
        multiples of a prime are flagged as 'no prime'. In addition there
        is an optimization by ignoring values flagged as none prime when
        proceeding to next value."""
    sieve  = [False, True] * (max_n // 2)
    sieve += [False]

    sieve[1] = False
    sieve[2] = True
    primes   = [2]

    val = 3
    while val <= max_n:
        # now we have one prime
        primes.append(val)
        # strike out values not being a prime
        offset  = val * 2
        noprime = val + offset
        while noprime <= max_n:
            sieve[noprime] = False
            noprime += offset
        # next value
        val += 2
        while val <= max_n:
            if not sieve[val]:
                val += 2
            else:
                break

    return primes


def calc_slower(max_n):
    """ scenario I - displaying relation and validate results """
    print("\n[%s]" % (sys._getframe().f_code.co_name))
    print("seeking primes between (0..%d) ..." % (max_n))
    primes1 = create_primes_1(max_n)
    primes2 = create_primes_2(max_n)
    primes3 = create_primes_3(max_n)
    primes4 = create_primes_4(max_n)
    primes5 = create_primes_5(max_n)
    primes6 = create_primes_6(max_n)

    assert primes1 == primes2 == primes3 == primes4 == primes5 == primes6
    print("done - %d primes found." % (len(primes4)))


def calc_medium(max_n):
    """ scenario II - testing 'is_prime' alone """
    print("\n[%s]" % (sys._getframe().f_code.co_name))
    print("seeking primes between (0..%d) ..." % (max_n))
    primes2 = create_primes_2(max_n)
    primes3 = create_primes_3(max_n)
    print("done - %d primes found." % (len(primes2)))


def calc_faster(max_n):
    """ scenario III - testing sieve alone """
    print("\n[%s]" % (sys._getframe().f_code.co_name))
    print("seeking primes between (0..%d) ..." % (max_n))
    primes3 = create_primes_3(max_n)
    primes4 = create_primes_4(max_n)
    primes5 = create_primes_5(max_n)
    print("done - %d primes found." % (len(primes4)))

if __name__ == "__main__":
    print("Python %s" % (sys.version))
    max_n = 100000
    calc_slower(max_n      )
    calc_medium(max_n *  10)
    calc_faster(max_n * 100)
