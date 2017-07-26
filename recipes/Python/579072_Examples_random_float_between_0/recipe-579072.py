import os
import struct

def random_1():
    return (int.from_bytes(os.urandom(7), 'big') >> 3) * 2 ** -53

def random_2():
    return (int.from_bytes(os.urandom(7), 'big') >> 3) / (1 << 53)

def random_3():
    array = bytearray(b'\x3F' + os.urandom(7))
    array[1] |= 0xF0
    return struct.unpack('>d', array)[0] - 1
