###Rich iterator wrapper

Originally published: 2006-11-19 00:03:21
Last updated: 2006-11-19 00:03:21
Author: George Sakkis

This recipe may be of interest to those who make heavy use of the itertools module. It provides a wrapper class that exposes most itertools functions as methods, plus a few more. Moreover, two frequently used itertools functions, chain and islice, are conveniently exposed as addition and slicing operators, respectively.