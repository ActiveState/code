## curry -- associating parameters with a function  
Originally published: 2001-04-05 00:39:28  
Last updated: 2001-04-18 03:32:32  
Author: Scott David Daniels  
  
In functional programming, currying is a way to bind arguments with\na function and wait for the rest of the arguments to show up later.\nYou "curry in" the first few parameters to a function, giving\nyou a function that takes subsequent parameters as input and\ncalls the original with all of those parameters.  This recipe uses\na class instance to hold the parameters before their first use.\nFor example:\n\n    double = curry(operator.mul, 2)\n    triple = curry(operator.mul, 3)