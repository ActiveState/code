## Simple creation, configuration and installation of logging handlers  
Originally published: 2011-06-01 11:06:50  
Last updated: 2011-06-01 19:05:40  
Author: Hank   
  
A helper class and function to make it easy to configure logging, and an example of using it to send `INFO` to `sys.stdout` and `WARNING` or above to `sys.stderr`.\n\nThis is a simple port to Python 2 (I tested on 2.7) of [Nick Coghlan's Python 3 recipe](http://code.activestate.com/recipes/577496-simple-creation-configuration-and-installation-of-/) for doing the same thing.