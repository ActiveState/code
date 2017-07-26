## reduce as a generator  
Originally published: 2006-11-15 03:32:12  
Last updated: 2007-03-25 03:23:31  
Author: kay schluehr  
  
In this recipe the builtin function reduce is generalized to a Python 2.5 style generator called greduce. The generator never stops and can be used to create an infinite stream of values by means of the generators send() method.