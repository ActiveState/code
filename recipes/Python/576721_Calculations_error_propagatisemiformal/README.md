## Calculations with error propagation, and semi-formal expressions  
Originally published: 2009-04-18 02:29:00  
Last updated: 2010-01-15 06:08:56  
Author: Eric-Olivier LE BIGOT  
  
**Do not use this module**, but use instead the more powerful [uncertainties.py module](http://pypi.python.org/pypi/uncertainties/).

Module for performing calculations with error propagation, such as (1 +- 0.1) * 2 = 2 +- 0.2.  Mathematical operations (addition, etc.), operations defined in the math module (sin, atan,...) and logical operations (<, >, etc.) can be used.

Correlations between parts of an expression are correctly taken into account (for instance, the error on "x-x" is strictly zero).

Code written for floats should directly work with the numbers with uncertainty defined here, without much need for modifications.

The module also contains a class that represents non-evaluated mathematical expressions.  This class is used for performing the differentiation required by the error propagation calculation, but can be used on its own, for manipulating "semi-formal" expressions whose variables can be accessed.