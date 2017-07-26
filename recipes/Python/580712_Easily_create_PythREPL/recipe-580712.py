from __future__ import print_function
#--------------------------------------------------------------
# Reference:
# https://docs.python.org/2.7/library/code.html
# https://docs.python.org/3.6/library/code.html
# code_interact.py
# Copyright 2016 Vasudev Ram
# Web site: https://vasudevram.github.io
# Blog: http://jugad2.blogspot.com
# Product store: https://gumroad.com/vasudevram
#--------------------------------------------------------------

import code

a = 1
b = "hello"
print("Before code.interact, a = {}, b = {}".format(a, b))

banner="code.interact session, type Ctrl-Z to exit."
code.interact( banner=banner, local=locals())

print("After code.interact, a = {}, b = {}".format(a, b))

'''
Run the program with the command:

$ python code_interact.py

and then interact with it, including printing or changing or using the values of variables defined in the program.
'''
