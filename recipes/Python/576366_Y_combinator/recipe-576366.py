'''
Implementation of the fixed point combinator Y. 
-----------------------------------------------

The Y combinator is a higher order function that suffices following relation:

      Y(F) = F(Y(F))

From the fixed point property we can get an idea on how to implement a recursive 
anonymous function.

The function F passed to Y has to be a function that takes a single function argument 
f and produces another function g ( i.e. Y(F) ). 

Suppose g calls f again. In a simple case where g takes also only one argument we 
can write:

     g = lambda n: ... f( ... n )

A concrete example of g we use to proceed the discussion is:

     g = lambda n: (1 if n<2 else n*f(n-1))

If g is returned by F(f) we can write:

     F = lambda f: lambda n: (1 if n<2 else n*f(n-1))

Now we call F passing Y(F):

     Y(F) = F(Y(F)) = lambda n: (1 if n<2 else n*Y(F)(n-1))
     
Finally we state:

     Y(F)(k) = (1 if k<2 else k*Y(F)(k-1))           
'''

Y = lambda g: (lambda f: g(lambda arg: f(f)(arg))) (lambda f: g(lambda arg: f(f)(arg)))

#
# Examples
#

# 1. factorial

fac = lambda f: lambda n: (1 if n<2 else n*f(n-1))
assert Y(fac)(7) == 5040

# 2. quicksort

qsort = lambda h: lambda lst: (lst if len(lst)<=1 else ( 
                             h([item for item in lst if item<lst[0]]) + \
                               [lst[0]]*lst.count(lst[0]) + \
                             h([item for item in lst if item>lst[0]])))

assert Y(qsort)([2,4,2,7,1,8]) == [1, 2, 2, 4, 7, 8]
