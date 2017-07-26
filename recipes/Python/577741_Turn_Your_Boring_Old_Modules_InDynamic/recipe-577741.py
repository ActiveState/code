"""moduleclass module"""

import modulehacker # from ActiveState recipe #577740

class Module:
    def __init__(self, module):
        attrs = dict(self.__dict__)
        for attr in module.__dict__:
            if attr in attrs:
                continue
            setattr(self, attr, getattr(module, attr))

_moduleclasses = {}
def register(cls):
    _moduleclasses[cls.__name__] = cls
    return cls

class Hacker(modulehacker.Hacker):
    def hack(self, module):
        name = getattr(module, "__moduleclass__", None)
        if not name:
            return module # untouched
        cls = _moduleclasses.get(name)
        if not cls:
            raise ImportError("Cannot use an unregistered module class")
        newmodule = cls(module)
        newmodule.__moduleclass__ = cls
        return newmodule

modulehacker.register(Hacker())
