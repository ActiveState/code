class InitFromSlots(type):
    def __new__(meta, name, bases, bodydict):
        slots = bodydict['__slots__']
        if slots and '__init__' not in bodydict:
            parts = ['def __init__(self, %s):' % ', '.join(slots)]
            for slot in slots:
                parts.append('    self.%s = %s' % (slot, slot))
            exec '\n'.join(parts) in bodydict
        super_new =  super(InitFromSlots, meta).__new__
        return super_new(meta, name, bases, bodydict)

class Record(object):
    __metaclass__ = InitFromSlots
    __slots__ = ()
    def _items(self):
        for name in self.__slots__:
            yield name, getattr(self, name)
    def __repr__(self):
        args = ', '.join('%s=%r' % tup for tup in self._items())
        return '%s(%s)' % (type(self).__name__, args)
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)
    def __getstate__(self):
        return dict(self._items())
    def __setstate__(self, statedict):
        self.__init__(**statedict)

# =========================
# At the interactive prompt
# =========================

>>> class Point(Record):
...     __slots__ = 'x', 'y'
... 
>>> Point(3, 4)
Point(x=3, y=4)
>>> Point(y=5, x=2)
Point(x=2, y=5)
>>> point = Point(-1, 42)
>>> point.x, point.y
(-1, 42)
>>> x, y = point
>>> x, y
(-1, 42)

>>> class Badger(Record):
...     __slots__ = 'large', 'wooden'
...     
>>> badger = Badger('spam', 'eggs')
>>> import pickle
>>> pickle.loads(pickle.dumps(badger))
Badger(large='spam', wooden='eggs')

>>> class Answer(Record):
...     __slots__ = 'life', 'universe', 'everything'
...     
>>> eval(repr(Answer(42, 42, 42)))
Answer(life=42, universe=42, everything=42)
