"""constants module

"""

import itertools


# some useful stepper functions for bind()

def step_lowercase(iterable):
    """A stepper function for lower-cased values."""
    for name in iterable:
        yield name, name.lower()

def step_echo(iterable):
    for name in iterable:
        yield name, name

def step_index_factory(start=0, step=1):
    def step_index(iterable):
        counter = itertools.count(start, step)
        for name in iterable:
            yield name, next(counter)
    return step_index

def step_binary_factory(start=0, step=1):
    def step_binary(iterable):
        """A stepper function for bitwise or-able values."""
        counter = itertools.count(start, step)
        for name in iterable:
            yield name, 2**next(counter)
    return step_binary


#######################

def build_mapping(iterable, stepper=None):
    """A generator for mapping the iterable to stepped values.

      iterable - the keys for the mapping.  It is also used by the
            stepper to generate the mapped values.
      stepper - the callable returning an iterator of the mapped
            values.  

    If a mapping is passed for the iterable, it is returned directly
    and the stepper is not used.  Otherwise, the stepper will be passed
    the iterable to generate the mapping.

    The stepper function should not change the iterable.  Neither
    should it produce keys other than those from the iterable.  A
    default stepper from step_count_factory() will be used if one is
    not passed.

    """

    try:
        for key in iterable:
            yield key, iterable[key]
    except TypeError:
        if stepper is None:
            stepper = step_index_factory(step=1)
        for key, value in stepper(iterable):
            yield key, value
        

def bind(obj, iterable, stepper=None):
    """Bind the iterable's values to the object.

      obj - where to bind the names.
      iterable - used to name the attributes and drive the mapper.
      stepper - the step function that generates the mapped values.
    
    Use this function to bind attribute names to any object.  It is
    used by the Constants class to that effect.  If the iterable is a
    mapping, it is used directly for the name/value pairs.  Otherwise
    the attribute values are built by the stepper.  See the
    build_mapping() function for more information.

    """

    for key, value in build_mapping(iterable, stepper):
        setattr(obj, key, value)
        

def bind_mapping(mapping, iterable, stepper=None):
    """Update the mapping with the generated values.

    This function is analogous to bind(), but updates a mapping rather
    than setting an object's attributes.

    """

    for key, value in build_mapping(iterable, stepper):
        mapping[key] = value


#######################

class Constants:
    """A simple namespace built around the passed iterable.

    The bind() function is used to build the namespace.  See it for
    more explanation of how the attributes are built and bound.

    The new attribute names are found in self.names and the
    corresponding values in self.values.  A reverse mapping from values
    to names is found at self.reversed.

    """

    def __init__(self, iterable, stepper=None):

        self._original = tuple(self.__dict__)
        self.names = tuple(iterable)
        bind(self, iterable, stepper)

    def __add__(self, obj):
        result = self.__class__.__new__(self.__class__)
        for name in self.names:
            setattr(result, name, getattr(self, name))
        for name in obj.names:
            setattr(result, name, getattr(obj, name))
        return result

    def __iadd__(self, obj):
        for name in obj.names:
            setattr(self, name, getattr(obj, name))

    def __contains__(self, obj):
        return obj in self.values

    @property
    def values(self):
        """The generated attribute values."""
        return tuple(val for name, val in self.__dict__.items()
                     if name not in self._original)

    @property
    def reversed(self):
        if not hasattr(self, "_reversed"):
            self._reversed = {}
            for name in self.names:
                value = getattr(self, name)
                if value not in self._reversed:
                    self._reversed[value] = []
                self._reversed[value].append(name)
        return self._reversed

    def get_reverse_lookup(self, value):
        return self.reversed[value]
