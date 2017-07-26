'''code_module.py

The purpose of this module
is to provide functions
for the coding of strings.

This is a level 1 module.'''

#==================================
# Level 1 Functions: String To Code
#==================================

def string_to_number(string):
    '''string_to_number(string)

    Create a starting number.
    Tranlate the string into the number.
    Return the number.'''
    number = 1
    for character in string:
        number *= 256
        number += ord(character)
    return number

def number_to_code(number):
    '''number_to_code(long)

    Create a starting string.
    Translate the number into the code.
    Return the string.'''
    code = str()
    while number != 0:
        code = chr(number % 255 + 1) + code
        number /= 255
    return code

#==================================
# Level 1 Functions: Code To String
#==================================

def code_to_number(code):
    '''code_to_number(string)

    Create a starting number.
    Tranlate the code into the number.
    Return the number.'''
    number = 0
    for character in code:
        number *= 255
        number += ord(character) - 1
    return number

def number_to_string(number):
    '''number_to_string(long)

    Create a starting string.
    Translate the number into the string.
    Return the string.'''
    string = str()
    while number > 1:
        string = chr(number % 256) + string
        number /= 256
    return string

#===============================
# Level 2 Functions: To And From
#===============================

def string_to_code(string):
    '''string_to_code(string)

    Returns a string converted to code.'''
    return number_to_code(string_to_number(string))

def code_to_string(code):
    '''code_to_string(string)

    Returns code converted to a string.'''
    return number_to_string(code_to_number(code))

#================
# CGI: Print File
#================

if __name__ == '__main__': 
    from sys import argv
    print 'Content-type: text/plain'
    print
    print file(argv[0]).read()
