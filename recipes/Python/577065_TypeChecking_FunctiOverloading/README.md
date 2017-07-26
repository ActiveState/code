## Type-Checking Function Overloading Decorator 
Originally published: 2010-02-23 15:17:36 
Last updated: 2010-04-11 11:16:48 
Author: Ryan Lie 
 
The recipe presents a function overloading decorator in python that do type check. The type signature is marked with the @takes and @returns  decorator, which causes the function to raise an InputParameterError exception if called with inappropriate arguments. The @overloaded function searches for the first overloads that doesn't raise TypeError or InputParameterError when called. Alternative overloads are added to the overloads list by using the @func.overload_with decorator. The order of function definition determines which function gets tried first and once it founds a compatible function, it skips the rest of the overloads list.