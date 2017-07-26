########## First define the interface checker and interfaces

from sets import Set
import UserDict

class InterfaceOmission(Exception): pass

class InterfaceChecker(type):
    "Validates the presence of required attributes"
    def __new__(cls, classname, bases, classdict):
        obj = type(classname, bases, classdict)
        if '__implements__' in classdict:
            defined = Set(dir(obj))
            for interface in classdict['__implements__']:
                required = Set(dir(interface))
                if not required.issubset(defined):
                    raise InterfaceOmission, list(required - defined)
        return obj

class MinimalMapping(object):
    "Interface specification"
    def __getitem__(self, key): pass
    def __setitem__(self, key, value): pass
    def __delitem__(self, key): pass
    def __contains__(self, key): pass

class FullMapping(MinimalMapping, UserDict.DictMixin):
    pass

class MinimalSequence(object):
    def __len__(self): pass
    def __getitem__(self, index): pass

class Callable(object):
    def __call__(self, *args): pass


########## The user code starts here

class MyClass(object):
    __metaclass__ = InterfaceChecker
    __implements__ = [MinimalMapping, Callable]
    def __getitem__(self, key): pass
    def __setitem__(self, key, value): pass
    #def __delitem__(self, key): pass    
    def __contains__(self, key): pass
    def __call__(self, *args): pass
    def setdefault(self, key, default):
        'Not required by the interface'


m = MyClass()
assert MinimalMapping in m.__implements__
