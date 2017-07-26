## Type checking using Python 3.x annotations  
Originally published: 2013-05-23 22:36:18  
Last updated: 2013-05-23 22:46:19  
Author: David Mertz  
  
Some other recipes have been suggested to allow type checking by various means.  Some of these require the use of type specification in a decorator itself.  Others try to be much more elaborate in processing a large variety of annotations (but hence require much more and more convoluted code).

The recipe provided below is very short, and simply provides actual **type** checking of arguments and return values.  It utilizes an unadorned decorator, rather than manufacture one that is parameterized by types or other arguments.