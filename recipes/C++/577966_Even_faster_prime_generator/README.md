###Even faster prime generator

Originally published: 2011-11-27 21:48:24
Last updated: 2011-11-27 21:48:25
Author: Sumudu Fernando

A very quick (segmented) sieve of Eratosthenes.\n\nTakes ~6s on a midrange machine to hit all 50 847 534 primes less than 1 billion, ending with 999999937\n\nIf you want to actually *do* anything with every prime (beyond counting them), there are three places to add a statement doing whatever is necessary with "lastP" -- one at the top (handles the special case '2'), one in the middle (handles "small" primes which are actually used to sieve), and one at the bottom (handles "large" primes which merely survive sieving).\n\nIn principle one can use a function object as parameter to allow generic operations on the primes, so add that if you want more general-purpose code (perhaps I'll do that later)\n\nFor higher limits you need to switch to wider types and follow the commented guidelines for the constants.  For a fixed limit, changing `B_SIZE` may affect performance so if needed tune it (profile as you go, of course!).  But this will get quite slow if you go to much higher numbers.