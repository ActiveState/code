## Numbers as Ranges - iterable integers

Originally published: 2014-10-02 00:23:52
Last updated: 2014-10-02 12:13:52
Author: elazar 

This header file makes simple integers iterable.\nNote that it works only on C++11 or above.\n\nUsage:\n\n    #include "num_range.h"\n    for (int i : 3) cout << i << endl;\n\nOutput:\n   0\n   1\n   2\n\nImplementation note: \nThis code is far too generic. We only need `DerefableInt`.\nThe templates are there for no practical reason.\n\nCons:\n   pollutes namespace std;\n   nonstandard idiom;