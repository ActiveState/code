###Yet Another Unique() Function

Originally published: 2007-02-27 15:20:19
Last updated: 2007-02-28 22:09:52
Author: Jordan Callicoat

Tim Peter's recipe (52560) and bearophile's version (438599) seem a bit too complex. There are speed an sorting issues with each. Not to mention that neither keeps the data type of the input object. Here is my take on a python unique() function for enumerables (list, tuple, str).