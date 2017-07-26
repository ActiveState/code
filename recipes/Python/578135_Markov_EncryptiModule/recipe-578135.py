import random
import sys
import collections

################################################################################

_CHAOS = random.SystemRandom()

def slots(names=''):
    sys._getframe(1).f_locals['__slots__'] = \
        tuple('__' + name for name in names.replace(',', ' ').split())

################################################################################

class Key(object):

    slots('data, prefix_len, base, size, encoder, axes, order, decoder')

    @classmethod
    def new(cls, chars_used, chain_size):
        selection, blocks = list(set(chars_used)), []
        for _ in range(chain_size):
            _CHAOS.shuffle(selection)
            blocks.append(''.join(selection))
        return cls(tuple(blocks))

    def __init__(self, data):
        self.__test_data(data)
        self.__make_vars(data)

    @staticmethod
    def __test_data(data):
        if not isinstance(data, tuple):
            raise TypeError('Data must be a tuple object!')
        if len(data) < 2:
            raise ValueError('Data must contain at least two items!')
        item = data[0]
        if not isinstance(item, str):
            raise TypeError('Data items must be str objects!')
        length = len(item)
        if length < 2:
            raise ValueError('Data items must contain at least two chars!')
        unique = set(item)
        if len(unique) != length:
            raise ValueError('Data items must contain unique char sets!')
        for item in data[1:]:
            if not isinstance(item, str):
                raise TypeError('Data items must be str objects!')
            next_length = len(item)
            if next_length != length:
                raise ValueError('All data items must have the same size!')
            next_unique = set(item)
            if len(next_unique) != next_length:
                raise ValueError('Data items must contain unique char sets!')
            if next_unique ^ unique:
                raise ValueError('All data items must use the same char set!')

    def __make_vars(self, data):
        self.__data = data
        self.__prefix_len = len(data) - 1
        self.__base = base = data[0]
        self.__size = size = len(base)
        offset = -sum(base.index(block[0]) for block in data[1:-1]) % size
        self.__encoder = base[offset:] + base[:offset]
        self.__axes = tuple(reversed([tuple(base.index(char) for char in block)
                                      for block in data[1:]]))
        self.__order = key = ''.join(sorted(base))
        grid = []
        for rotation in range(size):
            block, row = base[rotation:] + base[:rotation], [None] * size
            for char, value in zip(block, key):
                row[key.index(char)] = value
            grid.append(''.join(row))
        self.__decoder = tuple(grid[offset:] + grid[:offset])

    def test_primer(self, primer):
        primer.test_key(self)

    def encode(self, prefix, current):
        assert len(prefix) == self.__prefix_len, \
               'Prefix size is not compatible with key dimensions!'
        return self.__encoder[(sum(table[probe] for table, probe in
            zip(self.__axes, prefix)) + current) % self.__size]

    def decode(self, prefix, current):
        assert len(prefix) == self.__prefix_len, \
               'Prefix size is not compatible with key dimensions!'
        return self.__decoder[sum(table[probe] for table, probe in
            zip(self.__axes, prefix)) % self.__size][current]

    @property
    def data(self):
        return self.__data

    @property
    def prefix_len(self):
        return self.__prefix_len

    @property
    def base(self):
        return self.__base

    @property
    def order(self):
        return self.__order

################################################################################

class Primer(object):

    slots('data')

    @classmethod
    def new(cls, key):
        base = key.base
        return cls(''.join(_CHAOS.choice(base) for _ in range(key.prefix_len)))

    def __init__(self, data):
        self.__test_data(data)
        self.__data = data

    @staticmethod
    def __test_data(data):
        if not isinstance(data, str):
            raise TypeError('Data must be a str object!')
        if not data:
            raise ValueError('Data must contain at least one char!')

    def test_key(self, key):
        if len(self.__data) != key.prefix_len:
            raise ValueError('Key size must be one more than the primer size!')
        if not set(self.__data).issubset(key.base):
            raise ValueError('Key data must be a superset of primer data!')

    @property
    def data(self):
        return self.__data

################################################################################

class _Processor(object):

    slots('key, into, index, from')

    def __init__(self, key, primer):
        if self.__class__ is _Processor:
            raise NotImplementedError('This is an abstract class!')
        key.test_primer(primer)
        self.__key = key
        self.__into = table = dict(map(reversed, enumerate(key.order)))
        self.__index = collections.deque(map(table.__getitem__, primer.data))
        self.__index.appendleft(None)
        self.__from = dict(map(reversed, table.items()))

    def process(self, data):
        cache = []
        self._run(data, cache.append, self.__key, self.__into, self.__index)
        return ''.join(cache)

    @staticmethod
    def _run(data, cache_push, key, table, index):
        raise NotImplementedError('This is an abstract method!')

    @property
    def primer(self):
        self.__index.popleft()
        value = Primer(''.join(map(self.__from.__getitem__, self.__index)))
        self.__index.appendleft(None)
        return value

################################################################################

class Encrypter(_Processor):

    slots()

    @staticmethod
    def _run(data, cache_push, key, table, index):
        index_pop, encode, index_push = index.popleft, key.encode, index.append
        for char in data:
            if char in table:
                index_pop()
                code = table[char]
                cache_push(encode(index, code))
                index_push(code)
            else:
                cache_push(char)

################################################################################

class Decrypter(_Processor):

    slots()

    @staticmethod
    def _run(data, cache_push, key, table, index):
        index_pop, decode, index_push = index.popleft, key.decode, index.append
        for char in data:
            if char in table:
                index_pop()
                value = decode(index, table[char])
                cache_push(value)
                index_push(table[value])
            else:
                cache_push(char)

################################################################################

def encrypt(data, key, primer):
    engine = Encrypter(key, primer)
    return engine.process(data), engine.primer

def decrypt(data, key, primer):
    engine = Decrypter(key, primer)
    return engine.process(data), engine.primer

def auto_encrypt(data, chain_size, plain_text=''):
    key = Key.new(set(data) - set(plain_text), chain_size)
    primer = Primer.new(key)
    return Encrypter(key, primer).process(data), key, primer
