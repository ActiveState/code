class PseudoStructure(object):
    """A fast, small-footprint, structure-like type suitable for use as
    a data transfer or parameter object.

    This class is not intended to be used directly. Subclasses should
    define the fields they care about as slots and (optionally) define
    an initializer for those fields.

    This class is compatible with both Python2 and Python3 (tested on
    2.4-3.3).

    """

    __slots__ = []

    @classmethod
    def define(cls, class_name, *field_names):
        r"""Dynamically create a class definition for a subclass of
        ``PseudoStructure``.

        Note that objects of a dynamically created class cannot be
        pickled. If pickling support is needed, the subclass must have
        a static definition.

        >>> X = PseudoStructure.define('Attribute', 'name', 'value')
        >>> X.__name__
        'Attribute'
        >>> issubclass(X, PseudoStructure)
        True
        >>> X.__slots__
        ('name', 'value')

        """
        return type(class_name, (cls,), {"__slots__": field_names})

    def __getattr__(self, name):
        r"""Lazily initialize the value for *name*.

        >>> class Attribute(PseudoStructure):
        ...     __slots__ = ['name', 'value']
        ...
        >>> attr = Attribute()
        >>> attr.name is None
        True
        >>> attr.description is None
        Traceback (most recent call last):
        ...
        AttributeError: 'Attribute' object has no attribute 'description'

        """
        # only called once, if a value has not yet been assigned to the slot;
        # returns None as a reasonable default; if the name is not a slot,
        # raises AttributeError as expected
        setattr(self, name, None)

    def __getstate__(self):
        r"""Build the state object for pickling this object.

        >>> class Attribute(PseudoStructure):
        ...     __slots__ = ['name', 'value']
        ...
        >>> attr = Attribute()
        >>> attr.name = 'test'
        >>> sorted(attr.__getstate__().items())
        [('name', 'test'), ('value', None)]

        """
        state = {}
        for cls in self.__class__.__mro__:
            slots = getattr(cls, "__slots__", [])
            if (isinstance(slots, str)):
                slots = [slots]
            for slot in slots:
                state[slot] = getattr(self, slot)
        return state

    def __setstate__(self, state):
        r"""Initialize this object from a pickling state object.

        >>> class Attribute(PseudoStructure):
        ...     __slots__ = ['name', 'value']
        ...
        >>> attr = Attribute()
        >>> attr.name = 'test'
        >>> state = attr.__getstate__()
        >>> attr2 = Attribute()
        >>> attr2.__setstate__(state)
        >>> attr2.name == 'test'
        True
        >>> attr2.value is None
        True

        """
        for (name, value) in state.items():
            setattr(self, name, value)

    def __eq__(self, other):
        r"""Return True if the internal states of *other* and self are
        equal.

        >>> class Sample(PseudoStructure):
        ...     __slots__ = ['value']
        ...
        >>> sample1 = Sample()
        >>> sample2 = Sample()
        >>> sample1 == sample2
        True
        >>> sample2.value = 'test'
        >>> sample1 == sample2
        False

        """
        return (self.__getstate__() == other.__getstate__())

    def __hash__(self):
        r"""Return the hash of this pseudo-structure's internal state.

        >>> class Sample(PseudoStructure):
        ...     __slots__ = ['value']
        ...
        >>> sample1 = Sample()
        >>> sample2 = Sample()
        >>> hash(sample1) == hash(sample2)
        True
        >>> sample2.value = 'test'
        >>> hash(sample1) == hash(sample2)
        False

        """
        return hash(tuple(sorted(self.__getstate__().items())))

    def __repr__(self):
        r"""Return an unambiguous description of this object.

        >>> class Sample(PseudoStructure):
        ...     __slots__ = ['value']
        ...
        >>> sample = Sample()
        >>> repr(sample)
        "<Sample {'value': None}>"

        """
        return "<%s %r>" % (self.__class__.__name__, self.__getstate__())


if (__name__ == "__main__"):
    import doctest
    import pickle

    doctest.testmod()

    class Test(PseudoStructure):
        __slots__ = ["name"]

    x = Test()
    x.name = "pickle test"
    y = pickle.loads(pickle.dumps(x))
    assert x == y
