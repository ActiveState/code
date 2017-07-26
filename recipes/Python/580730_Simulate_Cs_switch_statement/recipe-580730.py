from __future__ import print_function

'''
simulate_c_switch.py
A program to demonstrate how to partially simulate 
the C switch statement in Python. The fall-through 
behavior of the C switch statement is not supported,
but the "default" case is.
Author: Vasudev Ram
Copyright 2016 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
Twitter: https://mobile.twitter.com/vasudevram
'''

def one_func():
    print('one_func called')

def two_func():
    print('two_func called')

def default_func():
    print('default_func called')

d = {1: one_func, 2: two_func}

for a in (1, 2, 3, None):
    print("a = {}: ".format(a), end="")
    d.get(a, default_func)()
