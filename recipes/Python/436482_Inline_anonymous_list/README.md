## In-line anonymous list comprehension functions  
Originally published: 2005-07-12 15:05:24  
Last updated: 2005-07-12 15:05:24  
Author: Frank P Mora  
  
List comprehensions, like functions, return values. They can even initialize and accumulate variables.

Initialization in these comprehension takes the form j for j in (n,) where n is any value and is equivalent to the j = n statement. Initialization happens only once at the top level of these comprehensions. Accumulation has the form of [j for j in (j*i,)] which is equivalent to j *= i where * can be any associative operator and i any value.