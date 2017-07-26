## Evaluates string embedded expressions (rubstr module) (v 0.91)  
Originally published: 2013-03-09 11:55:44  
Last updated: 2013-03-09 12:22:00  
Author: SnarkTurne   
  
This recipe allow you to write :

>>> a,b=5,6
>>> rstr("If you add #{a} and #{b}, you'll get #{a+b}.")
If you add 5 and 6, you'll get 11.

This is more readble, from my point of view, than :

    "If you add {} and {}, you'll get {}.".format(a,b,a+b)

This recipe is inspired from the way Ruby evaluates strings :

    irb> a,b=5,6
    irb> "If you add #{a} and #{b}, you'll get #{a+b}."
    ==> If you add 5 and 6, you'll get 11. 