###Automatic delegation as an alternative to inheritance

Originally published: 2001-03-22 16:15:16
Last updated: 2001-04-08 21:03:15
Author: Alex Martelli

Python classes cannot inherit from any type, just from other classes. However, automatic delegation (via __getattr__ and __setattr__) can provide pretty much the same functionality as inheritance (without such limits, and with finer-grained control).