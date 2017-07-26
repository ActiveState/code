'''translator_module.py

The purpose of this module
is to provide functions
for translating strings.

This is a level 1 module.'''

#===================================
# Level 1 Functions: Core Algorithms
#===================================

def get_dictionary(name=None):
    '''get_dictionary(object)

    Import needed functions.
    Setup the random system.
    Create needed variables.
    Create the dictionary.
    Return the dictionary.'''
    from random import randint, seed
    seed(name)
    dictionary, list_one, list_two = list(), range(256), range(256)
    for index in range(256):
        index_one, index_two = randint(0, 255 - index), randint(0, 255 - index)
        dictionary.append((list_one[index_one], list_two[index_two]))
        del list_one[index_one], list_two[index_two]
    return dictionary

def get_key(dictionary, bit):
    '''get_key(list, bool)

    Create a key.
    Setup its values.
    Return the key.'''
    key = range(256)
    for item in dictionary:
        key[item[bit]] = item[not bit]
    return key

def translate(old_string, key):
    '''translate(string, list)

    Create a new string.
    Translate the old string into the new string.
    Return the new string.'''
    new_string = str()
    for character in old_string:
        new_string += chr(key[ord(character)])
    return new_string

#=======================================
# Level 2 Functions: Helpful Definitions
#=======================================

def encode(dictionary):
    '''encode(list)

    Return a key for encoding.'''
    return get_key(dictionary, True)

def decode(dictionary):
    '''decode(list)

    Return a key for decoding.'''
    return get_key(dictionary, False)

#==============================
# Level 2 Functions: Named Keys
#==============================

def get_encode(name):
    '''get_encode(object)

    Assert that the name is not None.
    Return a named encoding key.'''
    assert name is not None
    return get_key(get_dictionary(name), True)

def get_decode(name):
    '''get_decode(object)

    Assert that the name is not None.
    Return a named decoding key.'''
    assert name is not None
    return get_key(get_dictionary(name), False)

#================
# CGI: Print File
#================

if __name__ == '__main__':
    from sys import argv
    print 'Content-type: text/plain'
    print
    print file(argv[0]).read()
