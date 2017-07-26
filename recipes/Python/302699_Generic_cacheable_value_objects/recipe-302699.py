class Cacheable(object):
    """Generic cacheable value object superclass."""

    def __new__(cls, *args, **kwargs):
        attr = "_%s__cache" % cls.__name__
        cache = getattr(cls, attr, None)
        if cache is None:
            cache = {}
            setattr(cls, attr, cache)
        key = (args, tuple(kwargs.iteritems()))
        obj = cache.get(key, None)
        if obj is None:
            obj = super(Cacheable, cls).__new__(cls, *args, **kwargs)
            cache[key] = obj
        return obj


class Date(Cacheable):
    """Example cacheable date class.

    >>> d = Date(2004, 1, 1)

    >>> d.day, d.month, d.year
    (1, 1, 2004)

    >>> str(d)
    '2004-01-01'

    >>> d is Date(2004, 1, 1)
    True
    """

    __slots__ = ("__year", "__month", "__day")

    def __init__(self, year, month, day):
        self.__day = day
        self.__month = month
        self.__year = year

    day = property(lambda self: self.__day)
    month = property(lambda self: self.__month)
    year = property(lambda self: self.__year)

    def __str__(self):
        return "%04d-%02d-%02d" % (self.__year, self.__month, self.__day)
