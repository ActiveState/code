#!/usr/bin/env python

import struct
import unittest

#-----------------------------------------------------------------------------
#: enable verbose print statements.
DEBUG = True

#: struct format lookup for specific word sizes.
STRUCT_FMT = {
    8  : 'B',   # unsigned char
    16 : 'H',   # unsigned short
    32 : 'I',   # unsigned int
}

#-----------------------------------------------------------------------------
def int_to_words(int_val, num_words=4, word_size=32):
    """
    @param int_val: an arbitrary length Python integer to be split up.
        Network byte order is assumed. Raises an IndexError if width of
        integer (in bits) exceeds word_size * num_words.

    @param num_words: number of words expected in return value tuple.

    @param word_size: size/width of individual words (in bits).

    @return: a list of fixed width words based on provided parameters.
    """
    max_int = 2 ** (word_size*num_words) - 1
    max_word_size = 2 ** word_size - 1

    if not 0 <= int_val <= max_int:
        raise IndexError('integer %r is out of bounds!' % hex(int_val))

    words = []
    for _ in range(num_words):
        word = int_val & max_word_size
        words.append(int(word))
        int_val >>= word_size
    words.reverse()

    return words

#-----------------------------------------------------------------------------
def int_to_packed(int_val, width=128, word_size=32):
    """
    @param int_val: an arbitrary sized Python integer to be packed.

    @param width: expected maximum with of an integer. Can be any size but
        should be divide by word_size without a remainder.

    @param word_size: size/width of individual words (in bits).
        Valid sizes are 8, 16 and 32 bits.

    @return: a (network byte order) packed string equivalent to integer value.
    """
    num_words = width / word_size
    words = int_to_words(int_val, num_words, word_size)

    try:
        fmt = '>%d%s' % (num_words, STRUCT_FMT[word_size])
        #DEBUG: print 'format:', fmt
    except KeyError:
        raise ValueError('unsupported word size: %d!' % word_size)

    return struct.pack(fmt, *words)

#-----------------------------------------------------------------------------
def packed_to_int(packed_int, width=128, word_size=32):
    """
    @param packed_int: a packed string to be converted to an abritrary size
        Python integer. Network byte order is assumed.

    @param width: expected maximum width of return value integer. Can be any
        size but should divide by word_size equally without remainder.

    @param word_size: size/width of individual words (in bits).
        Valid sizes are 8, 16 and 32 bits.

    @return: an arbitrary sized Python integer.
    """
    num_words = width / word_size

    try:
        fmt = '>%d%s' % (num_words, STRUCT_FMT[word_size])
        #DEBUG: print 'format:', fmt
    except KeyError:
        raise ValueError('unsupported word size: %d!' % word_size)

    words = list(struct.unpack(fmt, packed_int))
    words.reverse()

    int_val = 0
    for i, num in enumerate(words):
        word = num
        word = word << word_size * i
        int_val = int_val | word

    return int_val

#-----------------------------------------------------------------------------
class NetworkAddressTests(unittest.TestCase):
    """Example test case using various network address types"""
    def debug(self, val, expect_val_packed, actual_val_packed, new_val):
        print 'original int          :', hex(val)
        print 'packed int (expected) : %r' % expect_val_packed
        print 'packed int (actual)   : %r' % actual_val_packed
        print 'unpacked int          :', hex(new_val)
        print

    def testIPv4(self):
        """IP version 4 address test"""
        val = 0xfffefffe
        expect_val_packed = '\xff\xfe\xff\xfe'
        actual_val_packed = int_to_packed(val, width=32, word_size=8)
        new_val = packed_to_int(actual_val_packed, width=32, word_size=8)
        self.assertEqual(val, new_val)
        self.assertEqual(expect_val_packed, actual_val_packed)

        if DEBUG:
            print 'IPv4'
            self.debug(val, expect_val_packed, actual_val_packed, new_val)

    def testMAC(self):
        """MAC address test"""
        val = 0xfffefffefffe
        expect_val_packed = '\xff\xfe\xff\xfe\xff\xfe'
        actual_val_packed = int_to_packed(val, width=48, word_size=8)
        new_val = packed_to_int(actual_val_packed, width=48, word_size=8)
        self.assertEqual(val, new_val)
        self.assertEqual(expect_val_packed, actual_val_packed)

        if DEBUG:
            print 'MAC'
            self.debug(val, expect_val_packed, actual_val_packed, new_val)

    def testIPv6(self):
        """IP version 6 address test"""
        val = 0xfffefffefffefffefffefffefffefffe
        expect_val_packed = '\xff\xfe\xff\xfe\xff\xfe\xff\xfe' \
                              '\xff\xfe\xff\xfe\xff\xfe\xff\xfe'
        actual_val_packed = int_to_packed(val, width=128, word_size=32)
        new_val = packed_to_int(actual_val_packed, width=128, word_size=32)
        self.assertEqual(val, new_val)
        self.assertEqual(expect_val_packed, actual_val_packed)

        if DEBUG:
            print 'IPv6'
            self.debug(val, expect_val_packed, actual_val_packed, new_val)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
