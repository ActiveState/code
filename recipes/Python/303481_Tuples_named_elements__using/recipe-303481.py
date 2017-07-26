class NamedTupleMetaclass(type):
    """Metaclass for a tuple with elements named and indexed.
    
    NamedTupleMetaclass instances must set the 'names' class attribute
    with a list of strings of valid identifiers, being the names for the
    elements. The elements can then be obtained by looking up the name or the index.
    """

    def __init__(cls, classname, bases, classdict):
        super(NamedTupleMetaclass, cls).__init__(cls, classname, bases, classdict)

        # Must derive from tuple
        if not tuple in bases:
            raise ValueError, "'%s' must derive from tuple type." % classname
            
        # Create a dictionary to keep track of name->index correspondence
        cls._nameindices = dict(zip(classdict['names'], range(len(classdict['names']))))
        
        
        def instance_getattr(self, name):
            """Look up a named element."""
            try:
                return self[self.__class__._nameindices[name]]
            except KeyError:
                raise AttributeError, "object has no attribute named '%s'" % name

        cls.__getattr__ = instance_getattr

        
        def instance_setattr(self, name, value):
            raise TypeError, "'%s' object has only read-only attributes (assign to .%s)" % (self.__class__.__name__, name)

        cls.__setattr__ = instance_setattr

        
        def instance_new(cls, seq_or_dict):
            """Accept either a sequence of values or a dict as parameters."""
            if isinstance(seq_or_dict, dict):
                seq = []
                for name in cls.names:
                    try:
                        seq.append(seq_or_dict[name])
                    except KeyError:
                        raise KeyError, "'%s' element of '%s' not given" % (name, cls.__name__)
            else:
                seq = seq_or_dict
            return tuple.__new__(cls, seq)

        cls.__new__ = staticmethod(instance_new)


def NamedTuple(*namelist):
    """Class factory function for creating named tuples."""
    class _NamedTuple(tuple):
        __metaclass__ = NamedTupleMetaclass
        names = list(namelist)

    return _NamedTuple


# Example follows
if __name__ == "__main__":
    class PersonTuple(tuple):
        __metaclass__ = NamedTupleMetaclass
        names = ["name", "age", "height"]

    person1 = PersonTuple(["James", 26, 185])
    person2 = PersonTuple(["Sarah", 24, 170])
    person3 = PersonTuple(dict(name="Tony", age=53, height=192))
    
    print person1
    for i, name in enumerate(PersonTuple.names):
        print name, ":", person2[i]
    print "%s is %s years old and %s cm tall." % person3

    person3.name = "this will fail"
