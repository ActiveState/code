## Numbers as Ranges - iterable integers  
Originally published: 2014-10-02 00:23:52  
Last updated: 2014-10-02 12:13:52  
Author: elazar   
  
This header file makes simple integers iterable.
Note that it works only on C++11 or above.

Usage:

    #include "num_range.h"
    for (int i : 3) cout << i << endl;

Output:
   0
   1
   2

Implementation note: 
This code is far too generic. We only need `DerefableInt`.
The templates are there for no practical reason.

Cons:
   pollutes namespace std;
   nonstandard idiom;