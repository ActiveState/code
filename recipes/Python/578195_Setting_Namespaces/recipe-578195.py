"""Provides a simple way to deal with program variable versioning.

This module defines two classes to store application settings so that
multiple file versions can coexist with each other. Loading and saving
is designed to preserve all data among the different versions. Errors
are generated to protect the data when type or value violations occur."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '4 July 2012'
__version__ = 1, 0, 0

################################################################################

import pickle
import pickletools
import zlib

################################################################################

class _Settings:

    "_Settings(*args, **kwargs) -> NotImplementedError exception"

    def __init__(self, *args, **kwargs):
        "Notify the instantiator that this class is abstract."
        raise NotImplementedError('This is an abstract class!')

    @staticmethod
    def _save(path, obj):
        "Save an object to the specified path."
        data = zlib.compress(pickletools.optimize(pickle.dumps(obj)), 9)
        with open(path, 'wb') as file:
            file.write(data)

    @staticmethod
    def _load(path):
        "Load an object from the specified path."
        with open(path, 'rb') as file:
            data = file.read()
        return pickle.loads(zlib.decompress(data))

################################################################################

class Namespace(_Settings):

    "Namespace(**schema) -> Namespace instance"

    def __init__(self, **schema):
        "Initialize the Namespace instance with a schema definition."
        self.__original, self.__dynamic, self.__static, self.__owner = \
            {}, {}, {}, None
        for name, value in schema.items():
            if isinstance(value, _Settings):
                if isinstance(value, Namespace):
                    if value.__owner is not None:
                        raise ValueError(repr(name) + 'has an owner!')
                    value.__owner = self
                self.__original[name] = value
            else:
                raise TypeError(repr(name) + ' has bad type!')

    def __setattr__(self, name, value):
        "Set a named Parameter with a given value to be validated."
        if name in {'_Namespace__original',
                    '_Namespace__dynamic',
                    '_Namespace__static',
                    '_Namespace__owner',
                    'state'}:
            super().__setattr__(name, value)
        elif '.' in name:
            head, tail = name.split('.', 1)
            self[head][tail] = value
        else:
            attr = self.__original.get(name)
            if not isinstance(attr, Parameter):
                raise AttributeError(name)
            attr.validate(value)
            if value == attr.value:
                self.__dynamic.pop(name, None)
            else:
                self.__dynamic[name] = value

    def __getattr__(self, name):
        "Get a Namespace or Parameter value by its original name."
        if '.' in name:
            head, tail = name.split('.', 1)
            return self[head][tail]
        if name in self.__dynamic:
            return self.__dynamic[name]
        attr = self.__original.get(name)
        if isinstance(attr, Namespace):
            return attr
        if isinstance(attr, Parameter):
            return attr.value
        raise AttributeError(name)

    __setitem__ = __setattr__
    __getitem__ = __getattr__

    def save(self, path):
        "Save the state of the entire Namespace tree structure."
        if isinstance(self.__owner, Namespace):
            self.__owner.save(path)
        else:
            self._save(path, {Namespace: self.state})

    def load(self, path):
        "Load the state of the entire Namespace tree structure."
        if isinstance(self.__owner, Namespace):
            self.__owner.load(path)
        else:
            self.state = self._load(path)[Namespace]

    def __get_state(self):
        "Get the state of this Namespace and any child Namespaces."
        state = {}
        for name, types in self.__static.items():
            box = state.setdefault(name, {})
            for type_, value in types.items():
                box[type_] = value.state if type_ is Namespace else value
        for name, value in self.__original.items():
            box = state.setdefault(name, {})
            if name in self.__dynamic:
                value = self.__dynamic[name]
            elif isinstance(value, Parameter):
                value = value.value
            else:
                box[Namespace] = value.state
                continue
            box.setdefault(Parameter, {})[type(value)] = value
        return state

    def __set_state(self, state):
        "Set the state of this Namespace and any child Namespaces."
        dispatch = {Namespace: self.__set_namespace,
                    Parameter: self.__set_parameter}
        for name, box in state.items():
            for type_, value in box.items():
                dispatch[type_](name, value)

    def __set_namespace(self, name, state):
        "Set the state of a child Namespace."
        attr = self.__original.get(name)
        if not isinstance(attr, Namespace):
            attr = self.__static.setdefault(name, {})[Namespace] = Namespace()
        attr.state = state

    def __set_parameter(self, name, state):
        "Set the state of a child Parameter."
        attr = self.__original.get(name)
        for type_, value in state.items():
            if isinstance(attr, Parameter):
                try:
                    attr.validate(value)
                except TypeError:
                    pass
                else:
                    if value == attr.value:
                        self.__dynamic.pop(name, None)
                    else:
                        self.__dynamic[name] = value
                    continue
            if not isinstance(value, type_):
                raise TypeError(repr(name) + ' has bad type!')
            self.__static.setdefault(name, {}).setdefault(Parameter, {}) \
                [type_] = value

    state = property(__get_state, __set_state, doc='Namespace state property.')

################################################################################

class Parameter(_Settings):

    "Parameter(value, validator=lambda value: True) -> Parameter instance"

    def __init__(self, value, validator=lambda value: True):
        "Initialize the Parameter instance with a value to validate."
        self.__value, self.__validator = value, validator
        self.validate(value)

    def validate(self, value):
        "Check that value has same type and passes validator."
        if not isinstance(value, type(self.value)):
            raise TypeError('Value has a different type!')
        if not self.__validator(value):
            raise ValueError('Validator failed the value!')

    @property
    def value(self):
        "Parameter value property."
        return self.__value
