## Windowing an iterable with itertoolsOriginally published: 2010-04-15 18:45:40 
Last updated: 2010-04-15 18:45:41 
Author: Daniel Cohn 
 
Oftentimes a programmer needs to peek into an iterator without advancing it, a task for which many good solutions already exist. But what if the intrepid coder needs a fast and pythonic way to 'window' the data?  This recipe demonstrates how to wrap any iterable with a class that adds two methods, prev and peek.