###The Auxiliary-Dictionary idiom for sequences with frequent 'in' tests

Originally published: 2001-03-26 06:27:10
Last updated: 2001-04-08 20:45:56
Author: Alex Martelli

Python's "in" operator is extremely handy, but O(N) when applied to an N-item sequence; if a sequence is subject to frequent "in" tests, an auxiliary dictionary at its side can boost performance A LOT if the values are hashable.