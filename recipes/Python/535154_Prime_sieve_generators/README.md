## Prime sieve generators 
Originally published: 2007-12-05 11:40:53 
Last updated: 2008-04-25 22:29:55 
Author: Aaron Gallagher 
 
Two simple generators for generating prime numbers using a prime sieve. gen_sieve(n) will produce all prime numbers <n, and gen_infsieve() will infinitely produce prime numbers.\n\nisprime is an example of how one could use gen_sieve: a quick function for testing primality by attempting modulo division with each potential prime factor of a number.