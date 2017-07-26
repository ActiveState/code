'''Module for string manipulation.

This module provides several functions that
can encode, decode, and convert strings.'''

__version__ = 1.3

################################################################################

def string_code(string):
    'Convert from string to code.'
    return number_code(string_number(string))

def code_string(code):
    'Convert from code to string.'
    return number_string(code_number(code))

def string_number(string):
    'Convert from string to number.'
    number = 1L
    for character in string:
        number <<= 8
        number += ord(character)
    return number

def number_code(number):
    'Convert from number to code.'
    code = ''
    while number:
        code = chr(number % 255 + 1) + code
        number /= 255
    return code

def code_number(code):
    'Convert from code to number.'
    number = 0L
    for character in code:
        number *= 255
        number += ord(character) - 1
    return number

def number_string(number):
    'Convert from number to string.'
    string = ''
    while number > 1:
        string = chr(number & 0xFF) + string
        number >>= 8
    return string

def partition(string, size):
    'Partitions a string into substrings.'
    for index in range(0, len(string), size):
        yield string[index:index+size]

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
