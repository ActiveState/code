#! /usr/bin/env python

import random
import sys

################################################################################

def compress(string):
    # Get the unique characters and numeric base.
    unique = set(string)
    base = len(unique)
    # Create a key that will encode data properly.
    key = random.sample(unique, base)
    mapping = dict(map(reversed, enumerate(key)))
    while not mapping[string[-1]]:
        key = random.sample(unique, base)
        mapping = dict(map(reversed, enumerate(key)))
    # Create a compressed numeric representation.
    value = 0
    for place, char in enumerate(string):
        value += mapping[char] * base ** place
    # Return the number as a string with the table.
    return decode(value), bytes(key)

def decode(value):
    # Change a number into a string.
    array = bytearray()
    while value:
        value, byte = divmod(value, 256)
        array.append(byte)
    return bytes(array)

################################################################################

def decompress(string, mapping):
    # Get the numeric value of the string.
    value = encode(string)
    # Find the numeric base and prepare storage.
    base = len(mapping)
    data = bytearray()
    # Decode the value into the original string.
    while value:
        value, key = divmod(value, base)
        data.append(mapping[key])
    # Return the "string" as a bytes object.
    return bytes(data)

def encode(array):
    # Change a string into a number.
    assert array and array[-1], 'Array has ambiguous value!'
    value = 0
    for shift, byte in enumerate(array):
        value += byte << 8 * shift
    return value

################################################################################

def test():
    # Get this program's source.
    txt = open(sys.argv[0], 'r').read().encode()
    
    print('Length of data:', len(txt))

    # Compress the source numerically.
    data, table = compress(txt)
    
    print('Length after compression:', len(data))
    print('Length of the table:', len(table))
    print('Total compressed size:', len(data + table))
    print('Compression ratio: {:%}'.format(len(data + table) / len(txt)))

    # Decompress the data using the table.
    new = decompress(data, table)
    
    print('Decompression was {}successful.'.format(('not ', '')[txt == new]))
    print('Showing the decompressed data:')
    print('==============================')
    print(new.decode())

# Test this program if run directly.
if __name__ == '__main__':
    test()
