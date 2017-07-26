from __future__ import print_function

class SomeImplicitBase(object):
    """
    A special base class that is an implicit base of all singletons
    created with this pattern.  Not necessary, but included to show
    how this sort of thing would be done if needed.
    """
    pass

class SingletonMeta(type):
    """
    Needed to override the mro() to include implicit base classes
    at the end of the method resolution order, but before any of
    the bases of these implicit base classes that may appear in
    the mro of the explicit bases
    """
    def __new__(mcs, name, all_bases, cls_dict):
        return type.__new__(mcs, name, all_bases, cls_dict)
    def mro(cls):
        # Get what the __mro__ would be without special bases
        new_mro_bases = list(type("___unused_class_name_1",
            cls.__dict__['__explicit_bases__'], dict(cls.__dict__)).__mro__)
        # Omit __unused_class_name_1
        new_mro_bases = new_mro_bases[1:]
        # start with the mro that excludes the implicit bases
        for ibase in cls.__dict__["__implicit_bases__"]:
            # Iterate until we find an entry in the MRO that is a base
            # of ibase, and insert just before that.  MRO on a list like
            # this should be well-defined if the MRO is well-defined on
            # the explicit base list.
            spot = len(new_mro_bases)
            for i, bcls in enumerate(new_mro_bases):
                if bcls in ibase.__mro__:
                    spot = i
                    break
            new_mro_bases.insert(spot, ibase)
        # Now call type.mro() with this new, combined base list
        #   again omitting ___unused_class_name_2
        return tuple(
            [cls] + list(
                type("___unused_class_name_2",
                    tuple(new_mro_bases), dict(cls.__dict__)).__mro__[1:]
            )
        )
def as_singleton_instance(cls):
    """
    This is where the magic happens.  This defines a
    class decorator that returns an *instance* of a class
    with the name "_<original_name>__class" that has
    the same member functions, etc as the cls argument.
    The type of the returned value is not accessible to the
    user (except via the __class__ attribute of the returned
    instance), and therefore no other instances of the class
    can "accidentally" be created.
    """
    new_name = "_{0}__class".format(cls.__name__)
    new_dict = dict(cls.__dict__)
    implicit_bases = (SomeImplicitBase,)
    new_dict['__explicit_bases__'] = cls.__bases__
    new_dict['__implicit_bases__'] = implicit_bases
    all_bases = list(cls.__bases__) + list(implicit_bases)
    rv_type = SingletonMeta(
        new_name,
        tuple(all_bases),
        new_dict
    )
    rv = rv_type()
    return rv

class SomeOtherBaseClass(object):
    _some_property = 25

@as_singleton_instance
class this_is_an_instance(SomeOtherBaseClass):
    """
    this_is_an_instance will be an *instance* of a class
    named _this_is_an_instance__class, which will have the
    base classes SomeOtherBaseClass and SomeImplicitBase.
    All of the methods below will work as expected.
    """
    def __call__(self, *args):
        print("In instance __call__()")
    def some_function(self, *args):
        print("called some_function({0})".format(
            ", ".join(repr(a) for a in args)
        ))
    @property
    def some_property(self):
        print("getting some_property")
        return self._some_property
    @some_property.setter
    def some_property(self, new_value):
        print("setting some_property to {0}".format(new_value))
        self._some_property = new_value


if __name__ == "__main__":
    this_is_an_instance() # => prints "In instance __call__()"

    this_is_an_instance.some_function(
        "hello", "world"
    ) # => prints "called some_function("hello", "world")

    print(this_is_an_instance.some_property) # => prints "getting some_property", then "25"
    this_is_an_instance.some_property = 55 # => prints "setting some_property to 55"
    print(this_is_an_instance.some_property) # => prints "getting some_property", then "55"
