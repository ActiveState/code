## curry -- associating parameters with a function  
Originally published: 2001-04-05 00:39:28  
Last updated: 2001-04-18 03:32:32  
Author: Scott David Daniels  
  
In functional programming, currying is a way to bind arguments with
a function and wait for the rest of the arguments to show up later.
You "curry in" the first few parameters to a function, giving
you a function that takes subsequent parameters as input and
calls the original with all of those parameters.  This recipe uses
a class instance to hold the parameters before their first use.
For example:

    double = curry(operator.mul, 2)
    triple = curry(operator.mul, 3)