## Swapping two variables without using a third (temporary) variable  
Originally published: 2015-09-19 19:51:21  
Last updated: 2015-09-19 19:51:22  
Author: Vasudev Ram  
  
This recipe shows how to swap the values of two variables without making use of a third, temporary variable. The traditional method of swapping two variables is using a temp variable.

The first method shown here, swaps two variables an and b without using a temp variable. The variables a and b are integers:

a = 1, b = 2
# Prints original values of a and b, i.e. 1 and 2:
print a, b
a = a + b
b = a - b
a = a - b
# Prints swapped values of a and b, i.e. 2 and 1:
print a, b

The above swap method, using arithmetic expressions, will not work for non-numeric data types, and may also not work (at least in some cases) for floats. But the method below should work for any type of Python variable:

It even works for function objects. If you have:

def foo(): print "This is foo()."
def bar(): print "This is bar()."

and then:

foo(), bar()

and then:

foo, bar = bar, foo

then see what happens to values foo and bar, when you do:

foo()
bar()




