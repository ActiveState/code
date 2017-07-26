'''
function_arity.py
Purpose: To find the arity of a Python function.
Author: Vasudev Ram
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
'''

import inspect

# Define a few functions with increasing arity:

def f0():
    pass

def f1(a1):
    pass

def f2(a1, a2):
    pass

def f3(a1, a2, a3):
    pass

def f4(a1, a2, a3, a4):
    pass

def main():

    # Define a few non-function objects:
    int1 = 0
    float1 = 0.0 
    str1 = ''
    tup1 = ()
    lis1 = []

    # Test the function arity-finding code with both the functions 
    # and the non-function objects:
    for o in (f0, f1, f2, f3, f4, int1, float1, str1, tup1, lis1):
        if not inspect.isfunction(o):
            print repr(o), 'is not a function'
            continue
        n_args = len(inspect.getargspec(o)[0])
        if n_args == 0:
            num_suffix = '(no) args'
        elif n_args == 1:
            num_suffix = 'arg'
        else:
            num_suffix = 'args'
        print o.__name__, 'is a function that takes', \
            n_args, num_suffix
    
if __name__ == '__main__':
    main()
