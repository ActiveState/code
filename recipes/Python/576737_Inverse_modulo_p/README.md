###Inverse modulo p

Originally published: 2009-05-03 13:05:06
Last updated: 2013-01-31 23:41:21
Author: Justin Shaw

Very rarely it is necessary to find the multiplicative inverse of a number in the ring of integers modulo p.  Thie recipe handles those rare cases.  That is, given x, an integer, and p the modulus, we seek a integer x^-1 such that x * x^-1 = 1 mod p.  For example 38 is the inverse of 8 modulo 101 since 38 * 8 = 304 = 1 mod 101.  The inverse only exists when a and p are relatively prime.