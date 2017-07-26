'''
File: return_with_nested_cond_exprs.py 
Purpose: Demonstrate nested conditional expressions used in a return statement, 
to classify letters in a string as lowercase, uppercase or neither.
Also demonstrates doing the same task without a function and a return, 
using a lambda and map instead.
Author: Vasudev Ram
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
'''

from __future__ import print_function
from string import lowercase, uppercase

# Use return with nested conditional expressions inside a function, 
# to classify characters in a string as lowercase, uppercase or neither:
def classify_char(ch):
    return ch + ': ' + ('lowercase' if ch in lowercase else \
    'uppercase' if ch in uppercase else 'neither')

print("Classify using a function:")
for ch in 'AaBbCc12+-':
    print(classify_char(ch))

print()

# Do it using map and lambda instead of def and for:
print("Classify using map and lambda:")

print('\n'.join(map(lambda ch: ch + ': ' + ('lowercase' if ch in lowercase else 
'uppercase' if ch in uppercase else 'neither'), 'AaBbCc12+-')))
