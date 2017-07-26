###Roman numeral class with overloaded int methods

Originally published: 2011-04-06 14:52:05
Last updated: 2011-04-06 14:52:06
Author: thom neale

This Roman class is a subclass of int and supports the same methods int does, but any special methods that would normally return ints are return a new instance of Roman. You can use instances of this class in math expressions and a Roman instance will be returned, for example. \n\nThe class decorator used to achieve this was suggested by Alex Martelli '[here](http://stackoverflow.com/questions/1242589/subclassing-int-to-attain-a-hex-representation/1243045#1243045) on stackoverlow.com.