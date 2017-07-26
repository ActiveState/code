###Assign and test

Originally published: 2001-07-16 08:14:17
Last updated: 2001-07-16 08:14:17
Author: Alex Martelli

When transliterating C, Perl &c to Python, one often misses idioms such as "if((x=foo())" or "while((x=foo())" -- but, it's easy to get them back, with one small utility class!