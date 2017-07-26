"""Provide an implementation of Markov Encryption for simplified use.

This module exposes primitives useful for executing Markov Encryption
processes. ME was inspired by a combination of Markov chains with the
puzzles of Sudoku. This implementation has undergone numerous changes
and optimizations since its original design. Please see documentation."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '5 September 2012'
__version__ = 2, 0, 7

################################################################################

# Import several functions needed later in the code.

from random import SystemRandom
from sys import _getframe
from collections import deque

################################################################################

# Create some tools to use in the classes down below.

_CHAOS = SystemRandom()

def slots(names=''):
    """Set the __slots__ variable in the calling context with private names.

    This function allows a convenient syntax when specifying the slots
    used in a class. Simply call it in a class definition context with
    the needed names. Locals are modified with private slot names."""
    _getframe(1).f_locals['__slots__'] = \
        tuple('__' + name for name in names.replace(',', ' ').split())

################################################################################

# Implement a Key primitive data type for Markov Encryption.

class Key:

    """Key(data) -> Key instance

    This class represents a Markov Encryption Key primitive. It allows for
    easy key creation, checks for proper data construction, and helps with
    encoding and decoding indexes based on cached internal tables."""

    slots('data dimensions base size encoder axes order decoder')

    @classmethod
    def new(cls, bytes_used, chain_size):
        """Return a Key instance created from bytes_used and chain_size.

        Creating a new key is easy with this method. Call this class method
        with the bytes you want the key to recognize along with the size of
        the chains you want the encryption/decryption processes to use."""
        selection, blocks = list(set(bytes_used)), []
        for _ in range(chain_size):
            _CHAOS.shuffle(selection)
            blocks.append(bytes(selection))
        return cls(tuple(blocks))

    def __init__(self, data):
        """Initialize the Key instance's variables after testing the data.

        Keys are created with tuples of carefully constructed bytes arrays.
        This method tests the given data before going on to build internal
        tables for efficient encoding and decoding methods later on."""
        self.__test_data(data)
        self.__make_vars(data)

    @staticmethod
    def __test_data(data):
        """Test the data for correctness in its construction.

        The data must be a tuple of at least two byte arrays. Each byte
        array must have at least two bytes, all of which must be unique.
        Furthermore, all arrays should share the exact same byte set."""
        if not isinstance(data, tuple):
            raise TypeError('Data must be a tuple object!')
        if len(data) < 2:
            raise ValueError('Data must contain at least two items!')
        item = data[0]
        if not isinstance(item, bytes):
            raise TypeError('Data items must be bytes objects!')
        length = len(item)
        if length < 2:
            raise ValueError('Data items must contain at least two bytes!')
        unique = set(item)
        if len(unique) != length:
            raise ValueError('Data items must contain unique byte sets!')
        for item in data[1:]:
            if not isinstance(item, bytes):
                raise TypeError('Data items must be bytes objects!')
            next_length = len(item)
            if next_length != length:
                raise ValueError('All data items must have the same size!')
            next_unique = set(item)
            if len(next_unique) != next_length:
                raise ValueError('Data items must contain unique byte sets!')
            if next_unique ^ unique:
                raise ValueError('All data items must use the same byte set!')

    def __make_vars(self, data):
        """Build various internal tables for optimized calculations.

        Encoding and decoding rely on complex relationships with the given
        data. This method caches several of these key relationships for use
        when the encryption and decryption processes are being executed."""
        self.__data = data
        self.__dimensions = len(data)
        base, *mutations = data
        self.__base = base = tuple(base)
        self.__size = size = len(base)
        offset = -sum(base.index(block[0]) for block in mutations[:-1]) % size
        self.__encoder = base[offset:] + base[:offset]
        self.__axes = tuple(reversed([tuple(base.index(byte) for byte in block)
                                      for block in mutations]))
        self.__order = key = tuple(sorted(base))
        grid = []
        for rotation in range(size):
            block, row = base[rotation:] + base[:rotation], [None] * size
            for byte, value in zip(block, key):
                row[key.index(byte)] = value
            grid.append(tuple(row))
        self.__decoder = tuple(grid[offset:] + grid[:offset])

    def test_primer(self, primer):
        """Raise an error if the primer is not compatible with this key.

        Key and primers have a certain relationship that must be maintained
        in order for them to work together. Since the primer understands
        the requirements, it is asked to check this key for compatibility."""
        primer.test_key(self)

    def encode(self, index):
        """Encode index based on internal tables and return byte code.

        An index probes into the various axes of the multidimensional,
        virtual grid that a key represents. The index is evaluated, and
        the value at its coordinates is returned by running this method."""
        assert len(index) == self.__dimensions, \
               'Index size is not compatible with key dimensions!'
        *probes, current = index
        return self.__encoder[(sum(table[probe] for table, probe in
            zip(self.__axes, probes)) + current) % self.__size]

    def decode(self, index):
        """Decode index based on internal tables and return byte code.

        Decoding does the exact same thing as encoding, but it indexes
        into a virtual grid that represents the inverse of the encoding
        grid. Tables are used to make the process fast and efficient."""
        assert len(index) == self.__dimensions, \
               'Index size is not compatible with key dimensions!'
        *probes, current = index
        return self.__decoder[sum(table[probe] for table, probe in
            zip(self.__axes, probes)) % self.__size][current]

    @property
    def data(self):
        """Data that the instance was initialized with.

        This is the tuple of byte arrays used to create this key and can
        be used to create an exact copy of this key at some later time."""
        return self.__data

    @property
    def dimensions(self):
        """Dimensions that the internal, virtual grid contains.

        The virtual grid has a number of axes that can be referenced when
        indexing into it, and this number is the count of its dimensions."""
        return self.__dimensions

    @property
    def base(self):
        """Base value that the internal grid is built from.

        The Sudoku nature of the grid comes from rotating this value by
        offsets, keeping values unique along any axis while traveling."""
        return self.__base

    @property
    def order(self):
        """Order of base after its values have been sorted.

        A sorted base is important when constructing inverse rows and when
        encoding raw bytes for use in updating an encode/decode index."""
        return self.__order

################################################################################

# Implement a Primer primitive data type for Markov Encryption.

class Primer:

    """Primer(data) -> Primer instance

    This class represents a Markov Encryption Primer primitive. It is very
    important for starting both the encryption and decryption processes. A
    method is provided for their easy creation with a related key."""

    slots('data')

    @classmethod
    def new(cls, key):
        """Return a Primer instance from a parent Key.

        Primers must be compatible with the keys they are used with. This
        method takes a key and constructs a cryptographically sound primer
        that is ready to use in the beginning stages of encryption."""
        base = key.base
        return cls(bytes(_CHAOS.choice(base)
                         for _ in range(key.dimensions - 1)))

    def __init__(self, data):
        """Initialize the Primer instance after testing validity of data.

        Though not as complicated in its requirements as keys, primers do
        need some simple structure in the data they are given. A checking
        method is run before saving the data to the instance's attribute."""
        self.__test_data(data)
        self.__data = data

    @staticmethod
    def __test_data(data):
        """Test the data for correctness and test the data.

        In order for the primer to be compatible with the nature of the
        Markov Encryption processes, the data must be an array of bytes;
        and to act as a primer, it must contain at least some information."""
        if not isinstance(data, bytes):
            raise TypeError('Data must be a bytes object!')
        if not data:
            raise ValueError('Data must contain at least one byte!')

    def test_key(self, key):
        """Raise an error if the key is not compatible with this primer.

        Primers provide needed data to start encryption and decryption. For
        it be compatible with a key, it must contain one byte less than the
        key's dimensions and must be a subset of the base in the key."""
        if len(self.__data) != key.dimensions - 1:
            raise ValueError('Key size must be one more than the primer size!')
        if not set(self.__data).issubset(key.base):
            raise ValueError('Key data must be a superset of primer data!')

    @property
    def data(self):
        """Data that the instance was initialized with.

        This is the byte array used to create this primer and can be used
        if desired to create an copy of this primer at some later time."""
        return self.__data

################################################################################

# Create an abstract processing class for use in encryption and decryption.

class _Processor:

    """_Processor(key, primer) -> NotImplementedError exception

    This class acts as a base for the encryption and decryption processes.
    The given key is saved, and several tables are created along with an
    index. Since it is abstract, calling the class will raise an exception."""

    slots('key into index from')

    def __init__(self, key, primer):
        """Initialize the _Processor instance if it is from a child class.

        After passing several tests for creating a valid processing object,
        the key is saved, and the primer is used to start an index. Tables
        are also formed for converting byte values between systems."""
        if self.__class__ is _Processor:
            raise NotImplementedError('This is an abstract class!')
        key.test_primer(primer)
        self.__key = key
        self.__into = table = dict(map(reversed, enumerate(key.order)))
        self.__index = deque(map(table.__getitem__, primer.data),
                             key.dimensions)
        self.__from = dict(map(reversed, table.items()))

    def process(self, data):
        """Process the data and return its transformed state.

        A cache for the data transformation is created and an internal
        method is run to quickly encode or decode the given bytes. The
        cache is finally converted to immutable bytes when returned."""
        cache = bytearray()
        self._run(data, cache.append, self.__key, self.__into, self.__index)
        return bytes(cache)

    @staticmethod
    def _run(data, cache_append, key, table, index):
        """Run the processing algorithm in an overloaded method.

        Since this is only an abstract base class for encoding/decoding,
        this method will raise an exception when run. Inheriting classes
        should implement whatever is appropriate for the intended function."""
        raise NotImplementedError('This is an abstract method!')

    @property
    def primer(self):
        """Primer representing the state of the internal index.

        The index can be retrieved as a primer, useful for initializing
        another processor in the same starting state as the current one."""
        index = self.__index
        index.append(None)
        index.pop()
        return Primer(bytes(map(self.__from.__getitem__, index)))

################################################################################

# Inherit from _Processor and implement the ME encoding algorithm.

class Encrypter(_Processor):

    """Encrypter(key, primer) -> Encrypter instance

    This class represents a state-aware encryption engine that can be fed
    data and will return a stream of coherent cipher-text. An index is
    maintained, and a state-continuation primer can be retrieved at will."""

    slots()

    @staticmethod
    def _run(data, cache_append, key, table, index):
        """Encrypt the data with the given arguments.

        To run the encryption process as fast as possible, methods are
        cached as names. As the algorithm operates, only recognized bytes
        are encoded while running through the selective processing loop."""
        encode, index_append = key.encode, index.append
        for byte in data:
            if byte in table:
                index_append(table[byte])
                cache_append(encode(index))
            else:
                cache_append(byte)

################################################################################

# Inherit from _Processor and implement the ME decoding algorithm.

class Decrypter(_Processor):

    """Decrypter(key, primer) -> Decrypter instance

    This class represents a state-aware decryption engine that can be fed
    data and will return a stream of coherent plain-text. An index is
    maintained, and a state-continuation primer can be retrieved at will."""

    slots()

    @staticmethod
    def _run(data, cache_append, key, table, index):
        """Decrypt the data with the given arguments.

        To run the decryption process as fast as possible, methods are
        cached as names. As the algorithm operates, only recognized bytes
        are decoded while running through the selective processing loop."""
        decode, index_append = key.decode, index.append
        for byte in data:
            if byte in table:
                index_append(table[byte])
                value = decode(index)
                cache_append(value)
                index[-1] = table[value]
            else:
                cache_append(byte)

################################################################################

# Provide functions to easily encrypt and decrypt both bytes and strings.

def encrypt_bytes(data, key, primer):
    """Return encoded data processed with the key and primer.

    This function is a shortcut for creating an Encrypter instance,
    processing the data with the encryption engine, and returning the
    cipher-text along with the primer representing the engine's state."""
    engine = Encrypter(key, primer)
    return engine.process(data), engine.primer

def decrypt_bytes(data, key, primer):
    """Return decoded data processed with the key and primer.

    This function is a shortcut for creating a Decrypter instance,
    processing the data with the decryption engine, and returning the
    plain-text along with the primer representing the engine's state."""
    engine = Decrypter(key, primer)
    return engine.process(data), engine.primer

def encrypt_str(string, key, primer, encoding='utf-8', errors='ignore'):
    """Encode string with key and primer through binary interface.

    This function does its best to encrypt a string with a key and primer,
    taking the string's encoding into account and handling errors as given
    in the keyword arguments following the standard byte-level arguments."""
    engine = Encrypter(key, primer)
    return engine.process(string.encode(encoding, errors))\
           .decode(encoding, errors), engine.primer

def decrypt_str(string, key, primer, encoding='utf-8', errors='ignore'):
    """Decode string with key and primer through binary interface.

    This function does its best to decrypt a string with a key and primer,
    taking the string's encoding into account and handling errors as given
    in the keyword arguments following the standard byte-level arguments."""
    engine = Decrypter(key, primer)
    return engine.process(string.encode(encoding, errors))\
           .decode(encoding, errors), engine.primer

################################################################################

# Allow immediate encryption with automatically generated keys and primers.

def auto_encrypt_bytes(data, chain_size, plain_text=b''):
    """Encrypt data with automatically generated key and primer.

    This function automates key and primer creation and encrypts the
    data with them. The two arguments following the data allow some
    simple customizations of the key and primer generation process."""
    key = Key.new(set(data) - set(plain_text), chain_size)
    primer = Primer.new(key)
    return Encrypter(key, primer).process(data), key, primer

def auto_encrypt_str(string, chain_size, plain_text='',
                     encoding='utf-8', errors='ignore'):
    """Encrypt string with automatically generated key and primer.

    This function automates key and primer creation and encrypts the
    string with them. The two arguments following the data allow some
    simple customizations of the key and primer generation process."""
    string, plain_text = string.encode(encoding, errors), \
                         plain_text.encode(encoding, errors)
    key = Key.new(set(string) - set(plain_text), chain_size)
    primer = Primer.new(key)
    return Encrypter(key, primer).process(string)\
           .decode(encoding, errors), key, primer
