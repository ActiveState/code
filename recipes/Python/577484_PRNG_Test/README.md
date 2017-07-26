## PRNG Test  
Originally published: 2010-12-04 05:38:52  
Last updated: 2010-12-04 18:51:04  
Author: FB36   
  
This is a pseudo-random number generator test.

(There are many known tests for pseudo-random generators
but I came up w/ this one on my own. I don't know
if it is an already known method or not.)

Idea is this:
Imagine if you generate a 1000-bit binary number using any
PRNG (as 1-bit at a time) what is the probability that
all bits will be 0 in the number?

If you had a true number generator then there is a real
probability (=1/(2**1000)) but if you use a PRNG then I would say the 
probability is really 0!

If you had generated 2**1000 1000-bit numbers using a hypothetical 
True-Random Number Generator, assuming perfectly uniform probability
distribution, then TRNG would generate 1 number that contains 1000 zeros.
That is C(1000, 1000) = 1

Assuming perfectly uniform probability distribution,
C(n,k) gives you how many n-digit binary numbers would contain k zeros.

This code generates 2**n n-bit binary numbers (one bit at a time)
using the given PRNG and compares the actual distribution to the perfect 
distribution of a hypothetical True-Random Number Generator.

(I used n=20 in the code because the calculation takes too long.)
