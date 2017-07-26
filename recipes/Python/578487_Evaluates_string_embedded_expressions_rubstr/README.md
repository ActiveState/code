## Evaluates string embedded expressions (rubstr module) (v 0.91)

Originally published: 2013-03-09 11:55:44
Last updated: 2013-03-09 12:22:00
Author: SnarkTurne 

This recipe allow you to write :\n\n>>> a,b=5,6\n>>> rstr("If you add #{a} and #{b}, you'll get #{a+b}.")\nIf you add 5 and 6, you'll get 11.\n\nThis is more readble, from my point of view, than :\n\n    "If you add {} and {}, you'll get {}.".format(a,b,a+b)\n\nThis recipe is inspired from the way Ruby evaluates strings :\n\n    irb> a,b=5,6\n    irb> "If you add #{a} and #{b}, you'll get #{a+b}."\n    ==> If you add 5 and 6, you'll get 11. 