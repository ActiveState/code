"""enum.py

This module provides a simple enum type, Enum, which may be subclassed
to create a new enum type:

>>> class Breakfast(Enum):
...     SPAM, HAM, EGGS
...     BACON, SAUSAGE
>>> Breakfast.SPAM
EnumValue(<Breakfast.SPAM>)

Enum values implement the bitwise operators:

>>> Breakfast.SPAM | Breakfast.HAM
EnumValue(<Breakfast.(SPAM|HAM)>)

The idea of using __prepare__() to make this work came from Michael Foord:

http://mail.python.org/pipermail/python-ideas/2013-January/019108.html

"""
__all__ = ['Enum']


class EnumValue:
    """An enum value, associated with an Enum.

    EnumValue instances behave much like frozen sets, particularly with
    regard to bitwise operations (&, ^, |) as well implementing
    subtraction and inversion (~).

    """

    def __init__(self, enum, name, values=None):
        # XXX restrict name to all caps?
        self._enum = enum
        self._name = name
        self._values = values

    def __repr__(self):
        if self._name is not None:
            values = self._name
        else:
            values = "({})".format("|".join(v._name for v in self.values))
        return "{}(<{}.{}>)".format(self.__class__.__name__,
                                    self._enum.__name__, values)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(self._name or self.values)

    def _merge(self, op, other):
        try:
            if self._enum != other._enum:
                return NotImplemented
            values = op(other.values)
        except AttributeError:
            return NotImplemented
        else:
            if not values:
                raise TypeError("An EnumValue must not be empty")
            return self._enum._join(values)

    def __and__(self, other):
        return self._merge(self.values.__and__, other)

    def __xor__(self, other):
        return self._merge(self.values.__xor__, other)

    def __or__(self, other):
        return self._merge(self.values.__or__, other)

    def __sub__(self, other):
        return self._merge(self.values.__sub__, other)

    def __invert__(self):
        inverted = self._enum.values - self.values
        return self._enum.join(inverted)

    @property
    def values(self):
        if self._name is not None:
            return frozenset([self])
        else:
            return self._values


class _EnumNamespace(dict):
    def __init__(self):
        self._names = set()
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if key.startswith("_"):
                raise
            self._names.add(key)
    def __setitem__(self, key, value):
        if key.startswith("_"):
            dict.__setitem__(self, key, value)
        else:
            raise KeyError(key)
    def __delitem__(self, key):
        raise KeyError(key)


class _EnumMeta(type):

    @classmethod
    def make(meta, names, name='SimpleEnum'):
        """Return a new Enum subclass based on the passed names."""
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        else:
            names = list(map(str, names))

        ns = _EnumNamespace()
        ns._names = names
        return meta(name, (Enum,), ns)

    @classmethod
    def __prepare__(meta, name, bases):
        return _EnumNamespace()

    def __init__(cls, name, bases, namespace):
        # validation
        if len(bases) > 1:
            raise TypeError("expected 1 base class, got {}".format(len(bases)))
        elif not bases or bases == (object,):
            pass
        elif not issubclass(bases[0], Enum):
            raise TypeError("enums can only inherit from Enum")
        else:
            for value in bases[0].values:
                namespace._names.add(value._name)


        # set the values
        values = frozenset(EnumValue(cls, name) for name in namespace._names)
        super().__setattr__('values', values)
        for value in values:
            super().__setattr__(value._name, value)

        super().__setattr__('_joined_values', {})

    def __setattr__(cls, name, value):
        raise TypeError("enums are immutable")

    def __delattr__(cls, name):
        raise TypeError("enums are immutable")

    def __len__(cls):
        return len(cls._values)

    def __contains__(cls, value):
        return value in cls._values

    def __iter__(cls):
        return iter(cls._values)

    def _join(cls, values):
        # XXX make sure the values are in the enum?
        if values in cls._joined_values:
            return cls._joined_values[values]
        elif len(values) == 1:
            value = next(iter(values))
            cls._joined_values[values] = value
            return value
        else:
            joined = EnumValue(cls, None, values)
            cls._joined_values[values] = joined
            return joined

    def export(cls, namespace):
        """Copy the enums values into the namespace."""
        namespace.update((v._name, v) for v in cls.values)


class Enum(metaclass=_EnumMeta):
    """A base enum type, strictly for inheriting."""
    def __new__(cls, *args, **kwargs):
        raise TypeError("enums do not have instances")
