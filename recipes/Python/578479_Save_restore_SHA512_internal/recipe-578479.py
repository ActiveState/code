#!/usr/bin/python
""" save and restore sha512 inner state
    supports 32-bit and 64-bit architectures
    tested on CPython 2.6 and 2.7
    TODO does not take endian into account
    TODO assumes Python compiled with OpenSSL
"""
from hashlib import sha512
import ctypes
import binascii

POFFSET = 6
STATESIZE = 216


def save(obj):
    """return inner state of sha512 `obj` as raw string"""
    #assert isinstance(obj, sha512)
    datap = ctypes.cast(ctypes.cast(id(obj),
                                    ctypes.POINTER(ctypes.c_voidp))[POFFSET],
                        ctypes.POINTER(ctypes.c_char))
    assert datap

    return datap[:STATESIZE]


def restore(data):
    """create new sha512 object with inner state from `data`, str/bytes or iterable"""
    new = sha512()
    datap = ctypes.cast(ctypes.cast(id(new),
                                    ctypes.POINTER(ctypes.c_voidp))[POFFSET],
                        ctypes.POINTER(ctypes.c_char))
    assert datap
    assert datap[:8] == '\x08\xc9\xbc\xf3g\xe6\tj'  # first sha512 word

    for i, byte in enumerate(data):
        assert i < STATESIZE
        datap[i] = byte
    assert i + 1 == STATESIZE

    return new


savehex = lambda o: binascii.b2a_hex(save(o))
restorehex = lambda d: restore(binascii.a2b_hex(d))


if __name__ == "__main__":
    # different data lengths
    testdata = ["", "abcd" * 256, "o" * 13, "y" * 256]
    real = sha512()
    for test in testdata:
        real.update(test)
        # invariant x == restore(save(x))
        assert real.digest() == restore(save(real)).digest()
        assert real.hexdigest() == restorehex(savehex(real)).hexdigest()
