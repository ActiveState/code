from ctypes import *

class EnumerationType(type(c_uint)):
    def __new__(metacls, name, bases, dict):
        if not "_members_" in dict:
            _members_ = {}
            for key,value in dict.items():
                if not key.startswith("_"):
                    _members_[key] = value
            dict["_members_"] = _members_
        cls = type(c_uint).__new__(metacls, name, bases, dict)
        for key,value in cls._members_.items():
            globals()[key] = value
        return cls

    def __contains__(self, value):
        return value in self._members_.values()

    def __repr__(self):
        return "<Enumeration %s>" % self.__name__

class Enumeration(c_uint):
    __metaclass__ = EnumerationType
    _members_ = {}
    def __init__(self, value):
        for k,v in self._members_.items():
            if v == value:
                self.name = k
                break
        else:
            raise ValueError("No enumeration member with value %r" % value)
        c_uint.__init__(self, value)
        

    @classmethod
    def from_param(cls, param):
        if isinstance(param, Enumeration):
            if param.__class__ != cls:
                raise ValueError("Cannot mix enumeration members")
            else:
                return param
        else:
            return cls(param)

    def __repr__(self):
        return "<member %s=%d of %r>" % (self.name, self.value, self.__class__)
