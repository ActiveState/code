'Rough approximation of how slots work'

class Member(object):
    'Descriptor implementing slot lookup'
    def __init__(self, i):
        self.i = i
    def __get__(self, obj, type=None):
        return obj._slotvalues[self.i]
    def __set__(self, obj, value):
        obj._slotvalues[self.i] = value

class Type(type):
    'Metaclass that detects and implements _slots_'
    def __new__(self, name, bases, namespace):
        slots = namespace.get('_slots_')
        if slots:
            for i, slot in enumerate(slots):
                namespace[slot] = Member(i)
            original_init = namespace.get('__init__')                
            def __init__(self, *args, **kwds):
                'Create _slotvalues list and call the original __init__'                
                self._slotvalues = [None] * len(slots)
                if original_init is not None:
                    original_init(self, *args, **kwds)
            namespace['__init__'] = __init__
        return type.__new__(self, name, bases, namespace)

class Object(object):
    __metaclass__ = Type

class A(Object):
    _slots_ = 'x', 'y'

a = A()
a.x = 10
print a.x, a.y
