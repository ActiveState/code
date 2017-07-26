###Generator for permutations, combinations, selections of a sequence

Originally published: 2003-03-20 10:54:20
Last updated: 2003-03-20 10:54:20
Author: Ulrich Hoffmann

Permutations and combinations are often required in algorithms that do a complete search of the solution space. They are typically rather large so it's best not to  compute them entirely but better to lazily generate them.\nThis recipe uses Python 2.2 generators to create appropriate generator objects,\nthat can be use for example as ranges in for loops.