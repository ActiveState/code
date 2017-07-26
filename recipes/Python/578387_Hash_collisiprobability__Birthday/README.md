## Hash collision probability / Birthday problem

Originally published: 2012-12-19 14:38:21
Last updated: 2012-12-21 09:32:54
Author: Sander Evers

Calculates the probability that, when making *k* random selections out of *n* possibilities, at least two of the selections are the same.\nSee: http://en.wikipedia.org/wiki/Birthday_problem\n\nWhat is the probability that (at least) two people in a class of 30 share their birthday?\n\n    >>> collide(30,365)\n    0.7063162427192688\n\nWhat is the probability that ORA_HASH generates the same hash when hashing 25000 values?\n\n    >>> collide(25000,int(4.3e9))\n    0.07009388771353198\n