## Caching object creation 
Originally published: 2005-05-09 23:57:45 
Last updated: 2005-05-09 23:57:45 
Author: Michele Simionato 
 
This cookbook contains many recipes to memoize functions, however a recipe to\nmemoize classes was missing. Using this recipe you can cache object\ncreation, i.e. __new__ and __init__ methods are called only when needed.\nFor a good use case, see the discussion around http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/413609