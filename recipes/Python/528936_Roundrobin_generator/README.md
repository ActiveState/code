## Roundrobin generator 
Originally published: 2007-09-07 19:09:36 
Last updated: 2007-09-07 19:09:36 
Author: George Sakkis 
 
This recipe implements a round-robin generator, a generator that cycles through N iterables until all of them are exhausted:\n\n>>> list(roundrobin('abc', [], range(4),  (True,False)))\n['a', 0, True, 'b', 1, False, 'c', 2, 3]