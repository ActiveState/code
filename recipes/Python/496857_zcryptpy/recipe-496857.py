'''Support module for translating strings.

This module provides several functions
for definitions, keys, and transforms.'''

__version__ = 1.3

################################################################################

import random

def definition(name=None):
    'Returns a valid definition.'
    random.seed(name)
    definition, list_one, list_two = str(), range(256), range(256)
    for index in range(256):
        index_one, index_two = random.randrange(256 - index), random.randrange(256 - index)
        definition += chr(list_one[index_one]) + chr(list_two[index_two])
        del list_one[index_one], list_two[index_two]
    return definition
    

def key(definition, select):
    'Returns a valid key.'
    key = range(256)
    for index in range(256):
        key[ord(definition[index * 2 + int(bool(select))])] = definition[index * 2 + int(not bool(select))]
    return ''.join(key)

def transform(key, string):
    'Returns a valid transformation.'
    return string.translate(key)

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
