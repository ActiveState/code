## Cached Class  
Originally published: 2011-12-29 22:52:23  
Last updated: 2012-01-06 02:24:08  
Author: Peter Donis  
  
A class decorator that ensures that only one instance of\nthe class exists for each distinct set of constructor\narguments.\n\nNote that if a decorated class is subclassed, each subclass is cached separately. (This is because each cached subclass is a different ``cls`` argument to the ``__new__`` method.)\n