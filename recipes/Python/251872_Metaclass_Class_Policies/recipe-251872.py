class PolicyClass(type):                      # All metaclasses inherit type.
    __dict = {}                               # Used to store created classes.
    def __new__(cls, name, bases, d):         # class, name, bases, dict
        def __make(*T):                       # Wrapper function for old class.
            try:                              #     T* = Bases of new class.
                this = cls.__dict[(name, T)]  # Make sure the class doesn't
            except KeyError:                  #     already exist.
                this = type(name,             # Construct new class using type.
                    tuple([C for C in         # type() only accepts tuples.
                    (bases + T)               # Add policies to original bases.
                    if C is not type]), d)    # Remove <type> from bases.
                cls.__dict[(name, T)] = this  # Store new class for later use.
            return this                       # Return resulting class.
        return __make                         # Replace original class.


# examples --

class Class(type):
    __metaclass__ = PolicyClass
    C = 'X'
    def __init__(self):                       # super(Class, self) won't work
        super(                                #     because Class has already
            self.__class__, self              #     been replaced with
        ).__init__()                          #     PolicyClass.__new__.__make.
        self.c = 'x'

class PolicyA(object):
    A = 'Y'
    def __init__(self):
        super(PolicyA, self).__init__()
        self.a = 'y'

class PolicyB(object):
    B = 'Z'
    def __init__(self):
        super(PolicyB, self).__init__()
        self.b = 'z'

ClassA = Class(PolicyA, PolicyB)
ClassB = Class(PolicyB, PolicyA)

assert ClassA is Class(PolicyA, PolicyB)      # PolicyClass.__dict allows this.
assert ClassA is not ClassB                   # These are NOT the same.

Instance = ClassA()

assert Instance.A.lower() == Instance.a       # Ensure original class works.
assert Instance.B.lower() == Instance.b       # Ensure inheritance works.
assert Instance.C.lower() == Instance.c       # Ensure MRO works.
