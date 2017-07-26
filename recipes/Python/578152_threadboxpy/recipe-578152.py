"""Provide a way to run instance methods on a single thread.

This module allows hierarchical classes to be cloned so that their instances
run on one thread. Method calls are automatically routed through a special
execution engine. This is helpful when building thread-safe GUI code."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '9 October 2012'
__version__ = 1, 0, 1

################################################################################

import functools
import affinity

################################################################################

class _object: __slots__ = '_MetaBox__exec', '__dict__'

################################################################################

class MetaBox(type):

    "MetaBox(name, bases, classdict, old=None) -> MetaBox instance"

    __REGISTRY = {object: _object}
    __SENTINEL = object()

    @classmethod
    def clone(cls, old, update=()):
        "Creates a class preferring thread affinity after update."
        classdict = dict(old.__dict__)
        classdict.update(update)
        return cls(old.__name__, old.__bases__, classdict, old)

    @classmethod
    def thread(cls, func):
        "Marks a function to be completely threaded when running."
        func.__thread = cls.__SENTINEL
        return func

    def __new__(cls, name, bases, classdict, old=None):
        "Allocates space for a new class after altering its data."
        assert '__new__' not in classdict, '__new__ must not be defined!'
        assert '__slots__' not in classdict, '__slots__ must not be defined!'
        assert '__module__' in classdict, '__module__ must be defined!'
        valid = []
        for base in bases:
            if base in cls.__REGISTRY:
                valid.append(cls.__REGISTRY[base])
            elif base in cls.__REGISTRY.values():
                valid.append(base)
            else:
                valid.append(cls.clone(base))
        for key, value in classdict.items():
            if callable(value) and (not hasattr(value, '_MetaBox__thread') or
                                    value.__thread is not cls.__SENTINEL):
                classdict[key] = cls.__wrap(value)
        classdict.update({'__new__': cls.__new, '__slots__': (), '__module__':
                          '{}.{}'.format(__name__, classdict['__module__'])})
        cls.__REGISTRY[object() if old is None else old] = new = \
            super().__new__(cls, name, tuple(valid), classdict)
        return new

    def __init__(self, name, bases, classdict, old=None):
        "Initializes class instance while ignoring the old class."
        return super().__init__(name, bases, classdict)

    @staticmethod
    def __wrap(func):
        "Wraps a method so execution runs via an affinity engine."
        @functools.wraps(func)
        def box(self, *args, **kwargs):
            return self.__exec(func, self, *args, **kwargs)
        return box

    @classmethod
    def __new(meta, cls, *args, **kwargs):
        "Allocates space for instance and finds __exec attribute."
        self = object.__new__(cls)
        if 'master' in kwargs:
            self.__exec = kwargs['master'].__exec
        else:
            valid = tuple(meta.__REGISTRY.values())
            for value in args:
                if isinstance(value, valid):
                    self.__exec = value.__exec
                    break
            else:
                self.__exec = affinity.Affinity()
        return self
