## naive natural sort  
Originally published: 2011-04-28 13:07:42  
Last updated: 2011-08-13 16:47:36  
Author: Romain Dartigues  
  
I wrote this after reading The Alphanum Algorithm (http://www.davekoelle.com/alphanum.html) by David Koelle a few years ago; my goal was to improve the performances of the Python version of his scripts.\n\nMy version is approximatly 10 times faster than it's `alphanum.py` and about 3 times faster than the `alphanum.py_v2.4` on my computer, yielding the same results (for non-unicode at least).\n\n**Note**: see the version of wizkid in the comments which is even faster.