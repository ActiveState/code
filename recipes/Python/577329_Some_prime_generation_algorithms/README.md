###Some prime generation algorithms.

Originally published: 2010-07-23 19:10:57
Last updated: 2010-08-06 11:20:34
Author: Thomas Lehmann

Basic idea was to see the difference between different prime algorithms in time. Also they are not perfect the output shows that really higher numbers let grow the difference why I have separated this into functions to make it visible. I add this here because I have been missing this very often when I have been searching for algorithms.\n\n * The 'is_prime' is a well known way of checkin for a number being prime or not.\n * The sieve of Erastothenes is simply to strike out multiples of a given value; the primes will remain.\n * the function 'profile' is a decorator for functions measuring the execution time\n * Some information are in the comments of the code