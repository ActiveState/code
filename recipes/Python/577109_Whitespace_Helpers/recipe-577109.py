#! /usr/bin/env python
"""Helpers.py

Includes a function to encode Python strings into my WSA format.
Has a "PRINT_LINE" function that can be copied to a WSA program.
Contains a "PRINT" function and documentation as an explanation."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '14 March 2010'
__version__ = '$Revision: 1 $'

################################################################################

def encode_string(string, addr):
    print('     push', addr)
    print('     push', len(string))
    print('     set')
    addr += 1
    for offset, character in enumerate(string):
        print('     push', addr + offset)
        print('     push', ord(character))
        print('     set')

################################################################################

# Prints a string with newline.
# push addr
# call "PRINT_LINE"

"""
part "PRINT_LINE"
     call "PRINT"
     push 10
     ochr
     back
"""

################################################################################

# def print(array):
#     if len(array) <= 0:
#         return
#     offset = 1
#     while len(array) - offset >= 0:
#          ptr = array.ptr + offset
#          putch(array[ptr])
#          offset += 1

"""
part "PRINT"
# Line 1-2
     copy
     get
     less "__PRINT_RET_1"
     copy
     get
     zero "__PRINT_RET_1"
# Line 3
     push 1
# Line 4
part "__PRINT_LOOP"
     copy
     copy 2
     get
     swap
     sub
     less "__PRINT_RET_2"
# Line 5
     copy 1
     copy 1
     add
# Line 6
     get
     ochr
# Line 7
     push 1
     add
     goto "__PRINT_LOOP"
part "__PRINT_RET_2"
     away
part "__PRINT_RET_1"
     away
     back
"""
