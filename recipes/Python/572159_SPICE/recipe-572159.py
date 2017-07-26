'''Module that implements SPICE.

This module provides access to a standardized implementation
of SPICE (Stephen's Power-Inspired, Computerized Encryption).'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'April 19, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
T. Parker, for testing code that led to this module.
A. Baddeley, for contributing to the random module.
R. Hettinger, for adding support for two core generators.'''

################################################################################

import random as _random
import sys as _sys

################################################################################

def crypt_major():
    'Create a new Major Key.'
    return ''.join(map(chr, _crypt.sample(xrange(256), 256)))

def crypt_minor():
    'Create a new Minor Key.'
    sample = _crypt.sample(range(4) * 64, 256)
    array = []
    for index in xrange(64):
        bits_12 = sample[index * 4] << 6
        bits_34 = sample[index * 4 + 1] << 4
        bits_56 = sample[index * 4 + 2] << 2
        bits_78 = sample[index * 4 + 3]
        array.append(bits_12 + bits_34 + bits_56 + bits_78)
    return ''.join(map(chr, array))

################################################################################

def named_major(name):
    'Create a named Major Key.'
    _namer.seed(name)
    return ''.join(map(chr, _namer.sample(xrange(256), 256)))

def named_minor(name):
    'Create a named Minor Key.'
    _namer.seed(name)
    sample = _namer.sample(range(4) * 64, 256)
    array = []
    for index in xrange(64):
        bits_12 = sample[index * 4] << 6
        bits_34 = sample[index * 4 + 1] << 4
        bits_56 = sample[index * 4 + 2] << 2
        bits_78 = sample[index * 4 + 3]
        array.append(bits_12 + bits_34 + bits_56 + bits_78)
    return ''.join(map(chr, array))

################################################################################
    
def encode_string(string, major, minor):
    'Return an encrypted string.'
    assert isinstance(string, str)
    _check_major(major)
    _check_minor(minor)
    map_1 = _encode_map_1(major)
    map_2 = _encode_map_2(minor)
    return _encode(string, map_1, map_2)

def decode_string(string, major, minor):
    'Return a decrypted string.'
    assert isinstance(string, str) and len(string) % 4 == 0
    _check_major(major)
    _check_minor(minor)
    map_1 = _decode_map_1(minor)
    map_2 = _decode_map_2(major)
    return _decode(string, map_1, map_2)

################################################################################

def encode_file(source, destination, major, minor):
    'Encrypt a file from source to destination.'
    _check_major(major)
    _check_minor(minor)
    map_1 = _encode_map_1(major)
    map_2 = _encode_map_2(minor)
    string = source.read(2 ** 20 / 5)
    while string:
        destination.write(_encode(string, map_1, map_2))
        string = source.read(2 ** 20 / 5)

def decode_file(source, destination, major, minor):
    'Decrypt a file from source to destination.'
    _check_major(major)
    _check_minor(minor)
    map_1 = _decode_map_1(minor)
    map_2 = _decode_map_2(major)
    string = source.read(2 ** 20 / 5 * 4)
    while string:
        tail_len = len(string) % 4
        if tail_len == 0:
            destination.write(_decode(string, map_1, map_2))
            string = source.read(2 ** 20 / 5 * 4)
        else:
            destination.write(_decode(string[:-tail_len], map_1, map_2))
            return string[-tail_len:]
    return ''

################################################################################

class File_Crypt:

    'File_Crypt(major, minor, name, mode) -> File_Crypt'
    
    def __init__(self,  major, minor, name, mode):
        'Initialize the File_Crypt object.'
        _check_major(major)
        _check_minor(minor)
        self.__em1 = _encode_map_1(major)
        self.__em2 = _encode_map_2(minor)
        self.__dm1 = _decode_map_1(minor)
        self.__dm2 = _decode_map_2(major)
        assert len(mode) == 1 and mode in 'raw'
        self.__file = open(name, mode + 'b', 0)
        self.tail = ''

    def read(self, size=-1):
        'Read and decrypt from file.'
        string = self.__file.read(size * 4)
        tail_len = len(string) % 4
        if tail_len:
            self.tail = string[-tail_len:]
            return _decode(string[:-tail_len], self.__dm1, self.__dm2)
        else:
            return _decode(string, self.__dm1, self.__dm2)

    def write(self, string):
        'Encrypt and write to file.'
        self.__file.write(_encode(string, self.__em1, self.__em2))

    def seek(self, offset, whence=0):
        'Seek to virtual positon in file.'
        self.__file.seek(offset * 4, whence)
        offset = self.__file.tell() / 4
        self.__file.seek(offset * 4)

    def tell(self):
        'Return the virtual position in file.'
        return self.__file.tell() / 4

    def close(self):
        'Close the File_Crypt object.'
        self.__file.close()

################################################################################

class Socket_Crypt:

    'Socket_Crypt(major, minor, socket) -> Socket_Crypt'

    def __init__(self, major, minor, socket):
        'Initialize the Socket_Crypt object.'
        _check_major(major)
        _check_minor(minor)
        self.__em1 = _encode_map_1(major)
        self.__em2 = _encode_map_2(minor)
        self.__dm1 = _decode_map_1(minor)
        self.__dm2 = _decode_map_2(major)
        self.__major = major
        self.__minor = minor
        self.__socket = socket
        self.__tail = ''
        self.__tails = {}

    def accept(self):
        'Return a new Socket_Crypt and address.'
        conn, address = self.__socket.accept()
        return Socket_Crypt(self.__major, self.__minor, conn), address

    def recv(self, size, flags=0):
        'Receive and decrypt off socket.'
        string = self.__tail + self.__socket.recv(size * 4, flags)
        tail_len = len(string) % 4
        if tail_len:
            self.__tail = string[-tail_len:]
            return _decode(string[:-tail_len], self.__dm1, self.__dm2)
        else:
            self.__tail = ''
            return _decode(string, self.__dm1, self.__dm2)

    def recvfrom(self, size, flags=0):
        'Receive datagram and decrypt off socket.'
        string, address = self.__socket.recvfrom(size * 4, flags)
        string = self.__tails.get(address, '') + string
        tail_len = len(string) % 4
        if tail_len:
            self.__tails[address] = string[-tail_len:]
            string = _decode(string[:-tail_len], self.__dm1, self.__dm2)
            return string, address
        else:
            if address in self.__tails:
                del self.__tails[address]
            string = _decode(string, self.__dm1, self.__dm2)
            return string, address

    def send(self, string, flags=0):
        'Encrypt and send on socket.'
        string = _encode(string, self.__em1, self.__em2)
        sent = self.__socket.send(string, flags)
        offset = sent % 4
        if offset:
            string = string[sent:][:4-offset]
            sent += len(string)
            while string:
                string = string[self.__socket.send(string, flags):]
        return sent / 4

    def sendall(self, string, flags=0):
        'Encrypt and send all on socket.'
        string = _encode(string, self.__em1, self.__em2)
        return self.__socket.sendall(string, flags)

    def sendto(self, string, address, flags=0):
        'Encrypt and send datagram on socket.'
        string = _encode(string, self.__em1, self.__em2)
        sent = self.__socket.sendto(string, flags, address)
        offset = sent % 4
        if offset:
            string = string[sent:][:4-offset]
            sent += len(string)
            while string:
                string = string[self.socket.sentto(string, flags, address):]
        return sent / 4

    def makefile(self, mode='r', bufsize=-1):
        'Return a file-like object.'
        return self

    def read(self, size=-1):
        'Read and decrypt from socket.'
        if size < 0:
            cache = ''
            while True:
                temp = self.recv(2 ** 10)
                if temp:
                    cache += temp
                else:
                    return cache
        else:
            return self.recv(size)

    def readline(self, size=-1):
        'Dummy attribute for cPickle.'
        raise NotImplementedError

    def write(self, string):
        'Encrypt and write to socket.'
        self.sendall(string)

################################################################################

class String_Crypt:

    'String_Crypt(major, minor) -> String_Crypt'

    def __init__(self, major, minor):
        'Initialize the String_Crypt object.'
        _check_major(major)
        _check_minor(minor)
        self.__em1 = _encode_map_1(major)
        self.__em2 = _encode_map_2(minor)
        self.__dm1 = _decode_map_1(minor)
        self.__dm2 = _decode_map_2(major)

    def encode(self, string):
        'Return an encrypted string.'
        assert isinstance(string, str)
        return _encode(string, self.__em1, self.__em2)

    def decode(self, string):
        'Return a decrypted string.'
        assert isinstance(string, str) and len(string) % 4 == 0
        return _decode(string, self.__dm1, self.__dm2)

################################################################################

_crypt = _random.SystemRandom()
_namer = _random.Random()

################################################################################

def _check_major(key):
    'Private module function.'
    assert isinstance(key, str) and len(key) == 256
    for character in map(chr, xrange(256)):
        assert character in key

def _check_minor(key):
    'Private module function.'
    assert isinstance(key, str) and len(key) == 64
    indexs = []
    for byte in map(ord, key):
        for shift in xrange(6, -2, -2):
            indexs.append((byte >> shift) & 3)
    for index in xrange(4):
        assert indexs.count(index) == 64

def _encode_map_1(major):
    'Private module function.'
    return map(ord, major)

def _encode_map_2(minor):
    'Private module function.'
    map_2 = [[], [], [], []]
    array = []
    for byte in map(ord, minor):
        for shift in xrange(6, -2, -2):
            array.append((byte >> shift) & 3)
    for byte, index in enumerate(array):
        map_2[index].append(chr(byte))
    return map_2

def _decode_map_1(minor):
    'Private module function.'
    map_1 = []
    for byte in map(ord, minor):
        for shift in xrange(6, -2, -2):
            map_1.append((byte >> shift) & 3)
    return map_1

def _decode_map_2(major):
    'Private module function.'
    map_2 = [None] * 256
    for byte, index in enumerate(map(ord, major)):
        map_2[index] = chr(byte)
    return map_2

def _encode(string, map_1, map_2):
    'Private module function.'
    cache = ''
    for character in string:
        byte = map_1[ord(character)]
        for shift in xrange(6, -2, -2):
            cache += map_2[(byte >> shift) & 3][_crypt.randrange(64)]
    return cache

def _decode(string, map_1, map_2):
    'Private module function.'
    cache = ''
    iterator = iter(string)
    for byte in iterator:
        bits_12 = map_1[ord(byte)] << 6
        bits_34 = map_1[ord(iterator.next())] << 4
        bits_56 = map_1[ord(iterator.next())] << 2
        bits_78 = map_1[ord(iterator.next())]
        cache += map_2[bits_12 + bits_34 + bits_56 + bits_78]
    return cache

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
