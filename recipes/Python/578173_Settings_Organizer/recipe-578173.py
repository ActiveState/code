"""Provide an easy method to manage program options among multiple versions.

This module contains two classes used to store application settings in such a
way that multiple file versions can possibly coexist with each other. Loading
and saving settings is designed to preserve as much data between versions. An
error is generated on loading if saving would lead to any data being lost."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '4 July 2012'
__version__ = 1, 0, 2

################################################################################

import pickle
import pickletools
import zlib

################################################################################

class Namespace:

    "Namespace(**defaults) -> Namespace instance"

    def __init__(self, **defaults):
        "Initializes instance varaibles and checks defaults while loading."
        self.__defaults, self.__changes, self.__master = {}, {}, None
        for key, value in defaults.items():
            if isinstance(value, Namespace):
                if value.__master is not None:
                    raise ValueError(repr(key) + ' may not have a master!')
                value.__master = self
                self.__defaults[key] = value
            elif isinstance(value, Parameter):
                self.__defaults[key] = value
            else:
                raise TypeError(repr(key) + ' has unacceptable type!')

    def __setattr__(self, name, value):
        "Sets attributes after validating that they are allowed."
        if name in {'_Namespace__defaults',
                    '_Namespace__changes',
                    '_Namespace__master'}:
            super().__setattr__(name, value)
        elif '.' in name:
            head, tail = name.split('.', 1)
            self[head][tail] = value
        else:
            if name not in self.__defaults:
                raise AttributeError(name)
            attr = self.__defaults[name]
            if not isinstance(attr, Parameter):
                raise TypeError(name)
            attr.validate(value)
            self.__update_change(name, value, attr)

    def __getattr__(self, name):
        "Gets current value of attributes and unpacks if necessary."
        if '.' in name:
            head, tail = name.split('.', 1)
            return self[head][tail]
        if name not in self.__defaults:
            raise AttributeError(name)
        if name in self.__changes:
            return self.__changes[name].value
        attr = self.__defaults[name]
        if isinstance(attr, Parameter):
            return attr.value
        return attr

    __setitem__ = __setattr__
    __getitem__ = __getattr__

    def save(self, path):
        "Saves complete namespace tree to file given by path."
        if self.__master is None:
            state = self.__get_state()
            data = zlib.compress(pickletools.optimize(pickle.dumps(state)), 9)
            with open(path, 'wb') as file:
                file.write(data)
        else:
            self.__master.save(path)

    def load(self, path):
        "Loads complete namespace tree from file given by path."
        if self.__master is None:
            with open(path, 'rb') as file:
                data = file.read()
            klass, state = pickle.loads(zlib.decompress(data))
            if klass is Namespace:
                self.__set_state(state)
        else:
            self.__master.load(path)

    def __get_state(self):
        "Gets state of instance while takings changes into account."
        state, changes = {}, self.__changes.copy()
        for database in self.__defaults, changes:
            for key, value in database.items():
                if database is not changes:
                    value = changes.pop(key, value)
                if isinstance(value, Namespace):
                    state[key] = value.__get_state()
                else:
                    state[key] = Parameter, value.value
        return Namespace, state

    def __set_state(self, state):
        "Sets state of instance while validating incoming state."
        for key, (klass, value) in state.items():
            if klass is Namespace:
                self.__set_namespace(key, value)
            elif klass is Parameter:
                self.__set_parameter(key, value)

    def __set_namespace(self, key, value):
        "Takes namespace and attempts to update internal state."
        if key in self.__defaults:
            attr = self.__defaults[key]
            if isinstance(attr, Namespace):
                attr.__set_state(value)
            else:
                raise ResourceWarning(repr(key) + ' is not a Namespace!')
        else:
            attr = self.__changes[key] = Namespace()
            attr.__master = self
            attt.__set_state(value)

    def __set_parameter(self, key, value):
        "Takes parameter and attempts to update internal state."
        if key in self.__defaults:
            attr = self.__defaults[key]
            if isinstance(attr, Parameter):
                try:
                    attr.validate(value)
                except (TypeError, ValueError):
                    raise ResourceWarning(repr(key) + ' value failed tests!')
                else:
                    self.__update_change(key, value, attr)
            else:
                raise ResourceWarning(repr(key) + ' is not a Parameter!')
        else:
            self.__changes[key] = Parameter(value)

    def __update_change(self, key, value, attr):
        "Takes key/value pair and updates change database as needed."
        if value != attr.value:
            self.__changes[key] = Parameter(value)
        elif key in self.__changes:
            del self.__changes[key]

################################################################################

class Parameter:

    "Parameter(value, validator=lambda value: True) -> Parameter instance"

    def __init__(self, value, validator=lambda value: True):
        "Initializes instance variables and validates the value."
        self.__value, self.__validator = value, validator
        self.validate(value)

    def validate(self, value):
        "Verifies that the value has the same type and is considered valid."
        if not isinstance(value, type(self.value)):
            raise TypeError('Value has a different type!')
        if not self.__validator(value):
            raise ValueError('Validator failed the value!')

    @property
    def value(self):
        "Returns the value that is associated with this Parameter instance."
        return self.__value
