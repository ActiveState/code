## Rabin-Miller probabilistic prime test

Originally published: 2005-04-24 17:49:05
Last updated: 2005-04-25 02:49:23
Author: Josiah Carlson

Included is a recipe for performing the Rabin-Miller probabilistic test for a composite witness.  As provided by Paul Miller in the comments (not the Miller in Rabin-Miller), Rabin-Miller can only tell us if a value is definitely composite.  In the case where a test value is not a witness for the compositeness of a potential prime, it can only lie with a probability of at most 1/4.\n\nWith this, we can attempt to catch a liar over some number of trials, and the probability of us not catching at least one liar after k trials (if the number is not actually prime) is at most 4**-k.\n\nIncluded is an algorithm for generating a number of b bits for which no composite witness was found after k trials.  Removing mathematical rigor will suggest that the probability of the value being prime after k trials is at least 1-1/4**k.