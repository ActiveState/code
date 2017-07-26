def namedlist(typename, field_names):
    """Returns a new subclass of list with named fields.

    >>> Point = namedlist('Point', ('x', 'y'))
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain list
    33
    >>> x, y = p                        # unpack like a regular list
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)
    """
    fields_len = len(field_names)
    fields_text = repr(tuple(field_names)).replace("'", "")[1:-1] # tuple repr without parens or quotes

    class ResultType(list):
        __slots__ = ()
        _fields = field_names

        def _fixed_length_error(*args, **kwargs):
            raise TypeError(u"Named list has fixed length")
        append = _fixed_length_error
        insert = _fixed_length_error
        pop = _fixed_length_error
        remove = _fixed_length_error

        def sort(self):
            raise TypeError(u"Sorting named list in place would corrupt field accessors. Use sorted(x)")

        def _replace(self, **kwargs):
            values = map(kwargs.pop, field_names, self)
            if kwargs:
                raise TypeError(u"Unexpected field names: {s!r}".format(kwargs.keys()))

            if len(values) != fields_len:
                raise TypeError(u"Expected {e} arguments, got {n}".format(
                    e=fields_len, n=len(values)))

            return ResultType(*values)

        def __repr__(self):
            items_repr=", ".join("{name}={value!r}".format(name=name, value=value)
                                 for name, value in zip(field_names, self))
            return "{typename}({items})".format(typename=typename, items=items_repr)

    ResultType.__init__ = eval("lambda self, {fields}: self.__setitem__(slice(None, None, None), [{fields}])".format(fields=fields_text))
    ResultType.__name__ = typename

    for i, name in enumerate(field_names):
        fget = eval("lambda self: self[{0:d}]".format(i))
        fset = eval("lambda self, value: self.__setitem__({0:d}, value)".format(i))
        setattr(ResultType, name, property(fget, fset))

    return ResultType
