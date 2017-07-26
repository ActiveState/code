import collections as co
import abc

class ImmutableMeta(abc.ABCMeta):

    _classes = {}

    def __new__(meta, clsname, bases, clsdict):
        attributes = clsdict.pop('_attributes_')

        if bases[0] is object:
            # We're creating a class 'from scratch'
            methods = clsdict
        else:
            # we're 'inheriting' from an existing class.
            # Pull the base class's attributes and methods from the registry and
            # combine them with the new class's attributes and methods.
            base = bases[0]
            attributes = meta._classes[base]['attributes'] + ' ' + attributes
            base_methods = meta._classes[base]['methods'].copy()
            base_methods.update(clsdict)
            methods = base_methods

        # construct the actual base class and create the return class
        new_base = co.namedtuple(clsname + 'Base', attributes)
        cls = super(ImmutableMeta, meta).__new__(meta, clsname, (new_base,),
                                                 methods)

        # register the data necessary to 'inherit' from the class
        # and make sure that it passes typechecking
        meta._classes[cls] = {'attributes': attributes,
                              'methods': methods}
        if bases[0] is not object:
            base.register(cls)
        return cls

# Demo

class Foo(object):
    __metaclass__ = ImmutableMeta
    _attributes_ = 'a b'

    def sayhi(self):
        print "Hello from {0}".format(type(self).__name__)

class Bar(Foo):
    _attributes_ = 'c'

    def saybye(self):
        print "Goodbye from {0}".format(type(self).__name__)

a = Foo(1, 2)
a.sayhi()

b = Bar(1, 2, 3)
b.sayhi()  # 'inherited' from class Foo
b.saybye()

try:
    b.c = 1         # will raise an AttributeError
except AttributeError:
    print "Immutable"

print "issubclass(Bar, Foo): {0}".format(issubclass(Bar, Foo))
# We get this for free with abc

try:
   d =  {b: 1}        # No problems
except TypeError:
    print "Cant put it in a dict"
else:
    print "Can put it in a dict"
