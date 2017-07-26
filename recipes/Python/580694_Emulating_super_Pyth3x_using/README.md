## Emulating super() in Python 3.x using Python 2.7Originally published: 2016-07-31 04:03:28 
Last updated: 2016-07-31 04:03:29 
Author: sunqingyao  
 
Depending on the name of the first argument, `self.__sup` or `cls.__sup` behaves like `super()` in Python 3, while this code is written in Python 2.7.\n\nIt works for both ordinary methods and class methods(static methods don't use `super()`). See my code for detailed examples: