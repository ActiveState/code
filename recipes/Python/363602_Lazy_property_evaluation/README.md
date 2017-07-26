###Lazy property evaluation

Originally published: 2005-01-18 13:59:28
Last updated: 2005-01-18 13:59:28
Author: Scott David Daniels

Lazy properties can be easily built in Python 2.4 -- properties whose value may require some effort to calculate, but whose values remain constant once calculated.  This recipe uses decorators to implements such properties.