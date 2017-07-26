###Curried functions

Originally published: 2001-04-09 14:56:35
Last updated: 2001-04-09 14:56:35
Author: Ben Wolfson

A class to allow programmers to curry functions, so that arguments can be supplied one at a time instead of all at once.\nE.g., if F = Curry(lambda a,b: a+b), then\nF(1,2) == F(1)(2)