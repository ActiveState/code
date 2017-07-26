import functools
import threading

################################################################################

class _DDChecker(type):

    def __new__(cls, name, bases, classdict):
        for key, value in classdict.items():
            if key not in {'__new__', '__slots__', '_DoubleDict__dict_view'}:
                classdict[key] = cls._wrap(value)
        return super().__new__(cls, name, bases, classdict)

    @staticmethod
    def _wrap(function):
        @functools.wraps(function)
        def check(self, *args, **kwargs):
            value = function(self, *args, **kwargs)
            if self._DoubleDict__forward != \
               dict(map(reversed, self._DoubleDict__reverse.items())):
                raise RuntimeError('Forward & Reverse are not equivalent!')
            return value
        return check

################################################################################

class _DDAtomic(_DDChecker):

    def __new__(cls, name, bases, classdict):
        if not bases:
            classdict['__slots__'] += ('_DDAtomic__mutex',)
            classdict['__new__'] = cls._atomic_new
        return super().__new__(cls, name, bases, classdict)

    @staticmethod
    def _atomic_new(cls, iterable=(), **pairs):
        instance = object.__new__(cls, iterable, **pairs)
        instance.__mutex = threading.RLock()
        instance.clear()
        return instance

    @staticmethod
    def _wrap(function):
        @functools.wraps(function)
        def atomic(self, *args, **kwargs):
            with self.__mutex:
                return function(self, *args, **kwargs)
        return atomic

################################################################################

class _DDAtomicChecker(_DDAtomic):

    @staticmethod
    def _wrap(function):
        return _DDAtomic._wrap(_DDChecker._wrap(function))

################################################################################

class DoubleDict(metaclass=_DDAtomicChecker):

    __slots__ = '__forward', '__reverse'

    def __new__(cls, iterable=(), **pairs):
        instance = super().__new__(cls, iterable, **pairs)
        instance.clear()
        return instance

    def __init__(self, iterable=(), **pairs):
        self.update(iterable, **pairs)

    ########################################################################

    def __repr__(self):
        return repr(self.__forward)

    def __lt__(self, other):
        return self.__forward < other

    def __le__(self, other):
        return self.__forward <= other

    def __eq__(self, other):
        return self.__forward == other

    def __ne__(self, other):
        return self.__forward != other

    def __gt__(self, other):
        return self.__forward > other

    def __ge__(self, other):
        return self.__forward >= other

    def __len__(self):
        return len(self.__forward)

    def __getitem__(self, key):
        if key in self:
            return self.__forward[key]
        return self.__missing_key(key)

    def __setitem__(self, key, value):
        if self.in_values(value):
            del self[self.get_key(value)]
        self.__set_key_value(key, value)
        return value

    def __delitem__(self, key):
        self.pop(key)

    def __iter__(self):
        return iter(self.__forward)

    def __contains__(self, key):
        return key in self.__forward

    ########################################################################

    def clear(self):
        self.__forward = {}
        self.__reverse = {}

    def copy(self):
        return self.__class__(self.items())

    def del_value(self, value):
        self.pop_key(value)

    def get(self, key, default=None):
        return self[key] if key in self else default

    def get_key(self, value):
        if self.in_values(value):
            return self.__reverse[value]
        return self.__missing_value(value)

    def get_key_default(self, value, default=None):
        return self.get_key(value) if self.in_values(value) else default

    def in_values(self, value):
        return value in self.__reverse

    def items(self):
        return self.__dict_view('items', ((key, self[key]) for key in self))

    def iter_values(self):
        return iter(self.__reverse)

    def keys(self):
        return self.__dict_view('keys', self.__forward)

    def pop(self, key, *default):
        if len(default) > 1:
            raise TypeError('too many arguments')
        if key in self:
            value = self[key]
            self.__del_key_value(key, value)
            return value
        if default:
            return default[0]
        raise KeyError(key)

    def pop_key(self, value, *default):
        if len(default) > 1:
            raise TypeError('too many arguments')
        if self.in_values(value):
            key = self.get_key(value)
            self.__del_key_value(key, value)
            return key
        if default:
            return default[0]
        raise KeyError(value)

    def popitem(self):
        try:
            key = next(iter(self))
        except StopIteration:
            raise KeyError('popitem(): dictionary is empty')
        return key, self.pop(key)

    def set_key(self, value, key):
        if key in self:
            self.del_value(self[key])
        self.__set_key_value(key, value)
        return key

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def setdefault_key(self, value, default=None):
        if not self.in_values(value):
            self.set_key(value, default)
        return self.get_key(value)

    def update(self, iterable=(), **pairs):
        for key, value in (((key, iterable[key]) for key in iterable.keys())
                           if hasattr(iterable, 'keys') else iterable):
            self[key] = value
        for key, value in pairs.items():
            self[key] = value

    def values(self):
        return self.__dict_view('values', self.__reverse)

    ########################################################################

    def __missing_key(self, key):
        if hasattr(self.__class__, '__missing__'):
            return self.__missing__(key)
        if not hasattr(self, 'default_factory') \
           or self.default_factory is None:
            raise KeyError(key)
        return self.__setitem__(key, self.default_factory())

    def __missing_value(self, value):
        if hasattr(self.__class__, '__missing_value__'):
            return self.__missing_value__(value)
        if not hasattr(self, 'default_key_factory') \
           or self.default_key_factory is None:
            raise KeyError(value)
        return self.set_key(value, self.default_key_factory())

    def __set_key_value(self, key, value):
        self.__forward[key] = value
        self.__reverse[value] = key

    def __del_key_value(self, key, value):
        del self.__forward[key]
        del self.__reverse[value]

    ########################################################################

    class __dict_view(frozenset):

        __slots__ = '__name'

        def __new__(cls, name, iterable=()):
            instance = super().__new__(cls, iterable)
            instance.__name = name
            return instance

        def __repr__(self):
            return 'dict_{}({})'.format(self.__name, list(self))
