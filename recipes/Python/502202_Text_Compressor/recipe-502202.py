'''Module for string compression.

This module provides two functions for
compressing and decompressing strings.'''

__version__ = '1.0'

import sys as _sys

################################################################################

def encode(string, divide=1024):
    'Compress a string.'
    def encode(s, k, b):
        i = 0
        for c in s:
            i *= b
            i += k.index(c) + 1
        s = ''
        while i:
            s = chr(i % 255 + 1) + s
            i /= 255
        return s
    key = ''.join(byte for byte in map(chr, xrange(256)) if byte in string)
    divide = divide * 256 / len(key)
    base = len(key) + 1
    return '\0'.join(encode(string[index:index+divide], key, base) for index in xrange(0, len(string), divide)), key

def decode(string, key):
    'Decompress a string.'
    def decode(s, k, b):
        i = 0
        for c in s:
            i *= 255
            i += ord(c) - 1
        s = ''
        while i:
            s = k[i % b - 1] + s
            i /= b
        return s
    base = len(key) + 1
    return ''.join(decode(string, key, base) for string in string.split('\0'))

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
