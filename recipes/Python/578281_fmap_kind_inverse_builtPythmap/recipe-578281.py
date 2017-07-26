# fmap.py

# Author: Vasudev Ram - http://www.dancingbison.com

# fmap() is a Python function which is a kind of inverse of the 
# built-in Python map() function.
# The map() function is documented in the Python interpreter as
# follows:

"""
>>> print map.__doc__
map(function, sequence[, sequence, ...]) -> list

Return a list of the results of applying the function to the items of
the argument sequence(s).  If more than one sequence is given, the
function is called with an argument list consisting of the corresponding
item of each sequence, substituting None for missing values when not all
sequences have the same length.  If the function is None, return a list of
the items of the sequence (or a list of tuples if more than one sequence).
"""

# The fmap() function does the inverse, in a sense.
# It returns the result of applying a list of functions to a 
# given argument.
# TODO: Later extend the function to also work on a sequence of 
# arguments like map() does.

import string

def fmap(function_list, argument):
 result = argument
 for function in function_list:
  #print "calling " + function.__name__ + "(" + repr(result) + ")"
  result = function(result)
 return result

def times_two(arg):
 return arg * 2

def square(arg):
 return arg * arg

def upcase(s):
 return string.upper(s)

def delspace(s):
 return string.replace(s, ' ', '')

def main():

 print

 function_list = [ times_two, square ]
 for argument in range(5):
  fmap_result = fmap(function_list, argument)
  print "argument:", argument, ": fmap result:", fmap_result

 print

 function_list = [ upcase, delspace ]
 for argument in [ "the quick brown fox", "the lazy dog" ]:
  fmap_result = fmap(function_list, argument)
  print "argument:", argument, ": fmap result:", fmap_result

if __name__ == "__main__":
 main()

# EOF: fmap.py

"""
Output of running a test program for fmap():
$> python fmap.py

argument: 0 : fmap result: 0
argument: 1 : fmap result: 4
argument: 2 : fmap result: 16
argument: 3 : fmap result: 36
argument: 4 : fmap result: 64

argument: the quick brown fox : fmap result: THEQUICKBROWNFOX
argument: the lazy dog : fmap result: THELAZYDOG
"""
