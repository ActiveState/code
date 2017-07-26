# unless.py v1

# A simple program to partially simulate the unless statement 
# (a sort of reverse if statement) available in languages like Perl.
# The simulation is done by a function, not by a statement.

# Author: Vasudev Ram
# Web site: https://vasudevram.github.io
# Blog: https://jugad2.blogspot.com
# Product store: https://gumroad.com

# Define the unless function.
def unless(cond, func_if_false, func_if_true):
    if not cond:
        func_if_false()
    else:
        func_if_true()

# Test it.
def foo(): print "this is foo"
def bar(): print "this is bar"

a = 1
# Read the call below as:
# Unless a % 2 == 0, call foo, else call bar
unless (a % 2 == 0, foo, bar)
# Results in foo() being called.

a = 2
# Read the call below as:
# Unless a % 2 == 0, call foo, else call bar
unless (a % 2 == 0, foo, bar)
# Results in bar() being called.

'''
Here is the output:
$ python unless.py
this is foo
this is bar
'''
