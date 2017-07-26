import inspect


#class metamethod:
class classonlymethod:
    """Like a classmethod but does not show up on instances.

    This is an alternative to putting the methods on a metaclass.  It
    is especially meaningful for alternate constructors.

    """

    def __init__(self, method):
        self.method = method
        self.descr = classmethod(method)

    def __get__(self, obj, cls):
        name = self.method.__name__
        getattr_static = inspect.getattr_static

        if obj is not None:
            # look up the attribute, but skip cls
            dummy = type(cls.__name__, cls.__bases__, {})
            attr = getattr_static(dummy(), name, None)
            getter = getattr_static(attr, '__get__', None)

            # try data descriptors
            if (getter and getattr_static(attr, '__set__', False)):
                return getter(attr, obj, cls)

            # try the instance
            try:
                instance_dict = object.__getattribute__(obj, "__dict__")
            except AttributeError:
                pass
            else:
                try:
                    return dict.__getitem__(instance_dict, name)
                except KeyError:
                    pass

            # try non-data descriptors
            if getter is not None:
                return getter(attr, obj, cls)

            raise AttributeError(name)
        else:
            descr = vars(self)['descr']
            return descr.__get__(obj, cls)


#################################################
# tests

import unittest


class ClassOnlyMethodTests(unittest.TestCase):

    def test_class(self):
        class Spam:
            @classonlymethod
            def from_nothing(cls):
                return Spam()
        spam = Spam.from_nothing()

        self.assertIsInstance(spam, Spam)

    def test_instance(self):
        class Spam:
            @classonlymethod
            def from_nothing(cls):
                return Spam()

        with self.assertRaises(AttributeError):
            Spam().from_nothing()


if __name__ == '__main__':
    unittest.main()
