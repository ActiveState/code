# Setup code.

from __future__ import print_function
import string
from random import random, randint, randrange, choice, shuffle

'''
1) Random characters from the range of 7-bit ASCII characters, i.e. the characters with ASCII codes 0 to 127. This expression generates a single ASCII character:
'''
chr(randint(0, 127))

'''
To generate only printable ASCII characters, use:
'''
choice(string.printable)

'''
Generate random uppercase letter.
'''
chr(randint(ord('A'), ord('Z')))

'''
Or, another way:
Generate random uppercase letter.
'''
choice(string.ascii_uppercase)

'''
Generate random lowercase letter.
'''
chr(randint(ord('a'), ord('z')))

'''
Or, another way:
Generate random lowercase letter.
'''
choice(string.ascii_lowercase)

'''
Generate strings with random character content but fixed length, e.g.: "tdczs", "ohybi", "qhmyf", "elazk"
'''
def rand_lcase_str(n):
    '''Return string of n random lowercase letters.'''
    assert n > 0
    rand_chars = [ choice(string.ascii_lowercase) for i in range(n) ]
    return ''.join(rand_chars)

[ rand_lcase_str(3) for i in range(1, 8) ]
# Output:
# ['xio', 'qsc', 'omt', 'fnn', 'ezz', 'get', 'frs']

[ rand_lcase_str(7) for i in range(1, 4) ]
# Output:
# ['hazrdwu', 'sfvvxno', 'djmhxri']

'''
Generate strings with fixed character content but random lengths, e.g.: "g", "gggg", "gg", "ggggg", "ggg"; all strings contain only letter g's, but are of different lengths.
'''
def rand_len_fixed_char_str(c, low_len=1, high_len=256):
    '''Return a string containing a number of characters c,
    varying randomly in length between low_len and high_len'''
    assert len(c) == 1
    assert 0 < low_len <= high_len
    rand_chars = c * randint(low_len, high_len)
    return rand_chars

[ rand_len_fixed_char_str('g', 3, 8) for i in range(10) ]
# Output:
'''
['gggg',
 'ggggggg',
 'ggg',
 'ggggggg',
 'ggggg',
 'ggggg',
 'gggggg',
 'gggggg',
 'gggggg',
 'ggggg']
'''
