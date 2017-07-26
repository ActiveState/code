###Simple Function Overloading with Decorator

Originally published: 2010-02-23 14:50:33
Last updated: 2010-04-06 00:59:52
Author: Ryan Lie

The recipe presents a simple decorator for function overloading in python. The @overloaded function searches for the first overloads that doesn't raise TypeError when called. Overloads are added to the overloads list by using the @func.overload_with decorator. The order of function definition determines which function gets tried first and once it founds a compatible function, it skips the rest of the overloads list.