'''Module for accessing MWR.

This module provides an advanced, easy-to-use API for
accessing and mutating the Microsoft Windows Registry.'''

__version__ = 1.2

################################################################################

import _winreg
import os
import random
import sys
import time

class HKEY:
    'Hive Constants'
    CLASSES_ROOT = -2147483648
    CURRENT_USER = -2147483647
    LOCAL_MACHINE = -2147483646
    USERS = -2147483645
    CURRENT_CONFIG = -2147483643

class KEY:
    'SAM Constants'
    QUERY_VALUE = 1
    SET_VALUE = 2
    CREATE_SUB_KEY = 4
    ENUMERATE_SUB_KEYS = 8
    NOTIFY = 16
    CREATE_LINK = 32
    WRITE = 131078
    EXECUTE = 131097
    READ = 131097
    ALL_ACCESS = 983103

class REG:
    'Type Constants'
    NONE = 0
    SZ = 1
    EXPAND_SZ = 2
    BINARY = 3
    DWORD = 4
    DWORD_BIG_ENDIAN = 5
    LINK = 6
    MULTI_SZ = 7
    RESOURCE_LIST = 8
    FULL_RESOURCE_DESCRIPTOR = 9
    RESOURCE_REQUIREMENTS_LIST = 10
    QWORD = 11

################################################################################

class Value(object):

    'Value(value) -> Value'

    def __init__(self, value):
        'Initialize the Value object.'
        self.__value = value

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%r)' % (self.__class__.__name__, self.__value)

    def __get_value(self):
        'Private class method.'
        return self.__value

    value = property(__get_value, doc='Value of this object.')

class REG_NONE(Value): pass
class REG_SZ(Value): pass
class REG_EXPAND_SZ(Value): pass
class REG_BINARY(Value): pass
class REG_DWORD(Value): pass
class REG_DWORD_BIG_ENDIAN(Value): pass
class REG_LINK(Value): pass
class REG_MULTI_SZ(Value): pass
class REG_RESOURCE_LIST(Value): pass
class REG_FULL_RESOURCE_DESCRIPTOR(Value): pass
class REG_RESOURCE_REQUIREMENTS_LIST(Value): pass
class REG_QWORD(Value): pass

################################################################################

class Registry(object):

    'Registry([computer_name]) -> Registry'

    def __init__(self, computer_name=None):
        'Initialize the Registry object.'
        self.__computer_name = computer_name

    def __repr__(self):
        'Return the object\'s representation.'
        if self.__computer_name is None:
            return '%s()' % self.__class__.__name__
        return '%s(%r)' % (self.__class__.__name__, self.__computer_name)

    def __iter__(self):
        'Iterate over hives defined in HKEY.'
        for key in HKEY.__dict__:
            if not key.startswith('_'):
                yield self.__hive(HKEY.__dict__[key])

    def __hive(self, key):
        'Private class method.'
        if self.__computer_name is None:
            return Key(key=key)
        return Key(key=key, computer_name=self.__computer_name)

    def __HKEY_CLASSES_ROOT(self):
        'Private class method.'
        return self.__hive(HKEY.CLASSES_ROOT)

    def __HKEY_CURRENT_USER(self):
        'Private class method.'
        return self.__hive(HKEY.CURRENT_USER)

    def __HKEY_LOCAL_MACHINE(self):
        'Private class method.'
        return self.__hive(HKEY.LOCAL_MACHINE)

    def __HKEY_USERS(self):
        'Private class method.'
        return self.__hive(HKEY.USERS)

    def __HKEY_CURRENT_CONFIG(self):
        'Private class method.'
        return self.__hive(HKEY.CURRENT_CONFIG)

    HKEY_CLASSES_ROOT = property(__HKEY_CLASSES_ROOT, doc='The CLASSES_ROOT hive.')
    HKEY_CURRENT_USER = property(__HKEY_CURRENT_USER, doc='The CURRENT_USER hive.')
    HKEY_LOCAL_MACHINE = property(__HKEY_LOCAL_MACHINE, doc='The LOCAL_MACHINE hive.')
    HKEY_USERS = property(__HKEY_USERS, doc='The USERS hive.')
    HKEY_CURRENT_CONFIG = property(__HKEY_CURRENT_CONFIG, doc='The CURRENT_CONFIG hive.')

class Key(object):

    '''Key(**kwargs) -> Key

    Key(key=int) -> Key
    Key(key=PyHKEY) -> Key
    Key(key=Key) -> Key
    Key(key=int, sub_key=str) -> Key
    Key(key=PyHKEY, sub_key=str) -> Key
    Key(key=Key, sub_key=str) -> Key
    Key(key=int, sam=int) -> Key
    Key(key=PyHKEY, sam=int) -> Key
    Key(key=Key, sam=int) -> Key
    Key(key=int, sub_key=str, sam=int) -> Key
    Key(key=PyHKEY, sub_key=str, sam=int) -> Key
    Key(key=Key, sub_key=str, sam=int) -> Key
    Key(key=int, computer_name=str) -> Key
    Key(key=int, sub_key=str, computer_name=str) -> Key
    Key(key=int, sam=int, computer_name=str) -> Key
    Key(key=int, sub_key=str, sam=int, computer_name=str) -> Key'''

    def __init__(self, **kwargs):
        'Initialize the Key object.'
        assert kwargs, 'No Keyword Arguments Were Found'
        self.__repr, key, sub_key, sam, computer_name = '%s(%s)' % (self.__class__.__name__, ', '.join(['%s=%r' % (key, kwargs[key]) for key in kwargs])), kwargs.pop('key', None), kwargs.pop('sub_key', None), kwargs.pop('sam', None), kwargs.pop('computer_name', None)
        assert not kwargs, 'Invalid Keyword Arguments Were Found'
        if isinstance(key, (int, _winreg.HKEYType)) and sub_key is None and sam is None and computer_name is None:
            self.__self = _winreg.OpenKey(key, '')
        elif isinstance(key, Key) and sub_key is None and sam is None and computer_name is None:
            self.__self = _winreg.OpenKey(key.__self, '')
        elif isinstance(key, (int, _winreg.HKEYType)) and isinstance(sub_key, str) and sam is None and computer_name is None:
            self.__self = _winreg.OpenKey(key, sub_key)
        elif isinstance(key, Key) and isinstance(sub_key, str) and sam is None and computer_name is None:
            self.__self = _winreg.OpenKey(key.__self, sub_key)
        elif isinstance(key, (int, _winreg.HKEYType)) and sub_key is None and isinstance(sam, int) and computer_name is None:
            self.__self = _winreg.OpenKey(key, '', 0, sam)
        elif isinstance(key, Key) and sub_key is None and isinstance(sam, int) and computer_name is None:
            self.__self = _winreg.OpenKey(key.__self, '', 0, sam)
        elif isinstance(key, (int, _winreg.HKEYType)) and isinstance(sub_key, str) and isinstance(sam, int) and computer_name is None:
            self.__self = _winreg.OpenKey(key, sub_key, 0, sam)
        elif isinstance(key, Key) and isinstance(sub_key, str) and isinstance(sam, int) and computer_name is None:
            self.__self = _winreg.OpenKey(key.__self, sub_key, 0, sam)
        elif isinstance(key, int) and sub_key is None and sam is None and isinstance(computer_name, str):
            self.__self = _winreg.ConnectRegistry(computer_name, key)
        elif isinstance(key, int) and isinstance(sub_key, str) and sam is None and isinstance(computer_name, str):
            self.__self = _winreg.OpenKey(_winreg.ConnectRegistry(computer_name, key), sub_key)
        elif isinstance(key, int) and sub_key is None and isinstance(sam, int) and isinstance(computer_name, str):
            self.__self = _winreg.OpenKey(_winreg.ConnectRegistry(computer_name, key), '', 0, sam)
        elif isinstance(key, int) and isinstance(sub_key, str) and isinstance(sam, int) and isinstance(computer_name, str):
            self.__self = _winreg.OpenKey(_winreg.ConnectRegistry(computer_name, key), sub_key, 0, sam)
        else:
            raise TypeError, 'Key Could Not Be Initialized'

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def save(self, file_name):
        'Save this key to file.'
        _winreg.SaveKey(self.__self, file_name)

    def load(self, sub_key, file_name):
        'Load subkey from file.'
        _winreg.LoadKey(self.__self, sub_key, file_name)

    def __get_keys(self):
        'Private class method.'
        return Keys(self.__self)

    def __set_keys(self, keys):
        'Private class method.'
        if isinstance(keys, str):
            _winreg.CreateKey(self.__self, keys)
        elif isinstance(keys, (list, tuple)):
            for key in keys:
                self.keys = key
        else:
            raise TypeError, 'Key Could Not Be Created'

    def __del_keys(self):
        'Private class method.'
        try:
            while True:
                _winreg.DeleteKey(self.__self, _winreg.EnumKey(self.__self, 0))
        except EnvironmentError:
            pass

    def __get_values(self):
        'Private class method.'
        return Values(self.__self)

    def __set_values(self, values):
        'Private class method.'
        if isinstance(values, str):
            _winreg.SetValueEx(self.__self, values, 0, REG.SZ, _winreg.QueryValue(self.__self, ''))
        elif isinstance(values, (list, tuple)):
            for value in values:
                self.values = value
        else:
            raise TypeError, 'Value Could Not Be Created'

    def __del_values(self):
        'Private class method.'
        try:
            while True:
                _winreg.DeleteValue(self.__self, _winreg.EnumValue(self.__self, 0)[0])
        except EnvironmentError:
            pass

    def __get_value(self):
        'Private class method.'
        return _winreg.QueryValue(self.__self, '')

    def __set_value(self, value):
        'Private class method.'
        _winreg.SetValue(self.__self, '', REG.SZ, value)

    def __del_value(self):
        'Private class method.'
        _winreg.DeleteValue(self.__self, '')

    def __get_info(self):
        'Private class method.'
        return Info(*_winreg.QueryInfoKey(self.__self))

    keys = property(__get_keys, __set_keys, __del_keys, 'Keys of this key.')
    values = property(__get_values, __set_values, __del_values, 'Values of this key.')
    value = property(__get_value, __set_value, __del_value, 'Value of this key.')
    info = property(__get_info, doc='Information about this key.')

class Keys(object):

    'Keys(key) -> Keys'

    def __init__(self, key):
        'Initialize the Keys object.'
        self.__self = key

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%r)' % (self.__class__.__name__, self.__self)

    def __len__(self):
        'Return the number of keys.'
        return _winreg.QueryInfoKey(self.__self)[0]

    def __getitem__(self, key):
        'Return the specified key.'
        return Key(key=self.__self, sub_key=key)

    def __setitem__(self, key, value):
        'Assign the item to a key.'
        file_name = os.path.join(os.path.dirname(sys.argv[0]), ''.join(random.sample('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 8)))
        while os.path.exists(file_name):
            file_name = os.path.join(os.path.dirname(sys.argv[0]), ''.join(random.sample('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 8)))
        try:
            value.save(file_name)
            _winreg.LoadKey(self.__self, key, file_name)
        finally:
            os.remove(file_name)

    def __delitem__(self, key):
        'Delete the specified key.'
        _winreg.DeleteKey(self.__self, key)

    def __iter__(self):
        'Iterate over the key names.'
        keys, index = [], 0
        try:
            while True:
                keys.append(_winreg.EnumKey(self.__self, index))
                index += 1
        except EnvironmentError:
            for key in keys:
                yield key

    def __contains__(self, item):
        'Check for a key\'s existence.'
        item, index = item.lower(), 0
        try:
            while True:
                if _winreg.EnumKey(self.__self, index).lower() == item:
                    return True
                index += 1
        except EnvironmentError:
            return False

class Values(object):

    'Values(key) -> Values'

    TYPES = REG_NONE, REG_SZ, REG_EXPAND_SZ, REG_BINARY, REG_DWORD, REG_DWORD_BIG_ENDIAN, REG_LINK, REG_MULTI_SZ, REG_RESOURCE_LIST, REG_FULL_RESOURCE_DESCRIPTOR, REG_RESOURCE_REQUIREMENTS_LIST, REG_QWORD

    def __init__(self, key):
        'Initialize the Values object.'
        self.__self = key

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%r)' % (self.__class__.__name__, self.__self)

    def __len__(self):
        'Return the number of values.'
        return _winreg.QueryInfoKey(self.__self)[1]

    def __getitem__(self, key):
        'Return the specified value.'
        item_value, item_type = _winreg.QueryValueEx(self.__self, key)
        return self.TYPES[item_type](item_value)

    def __setitem__(self, key, value):
        'Assign the item to a value.'
        if isinstance(value, self.TYPES):
            _winreg.SetValueEx(self.__self, key, 0, list(self.TYPES).index(value.__class__), value.value)
        else:
            _winreg.SetValueEx(self.__self, key, 0, _winreg.QueryValueEx(self.__self, key)[1], value)

    def __delitem__(self, key):
        'Delete the specified value.'
        _winreg.DeleteValue(self.__self, key)

    def __iter__(self):
        'Iterate over the value names.'
        values, index = [], 0
        try:
            while True:
                values.append(_winreg.EnumValue(self.__self, index)[0])
                index += 1
        except EnvironmentError:
            for value in values:
                yield value

    def __contains__(self, item):
        'Check for a value\'s existence.'
        item, index = item.lower(), 0
        try:
            while True:
                if _winreg.EnumValue(self.__self, index)[0].lower() == item:
                    return True
                index += 1
        except EnvironmentError:
            return False

class Info(object):

    'Info(keys, values, modified) -> Info'

    def __init__(self, keys, values, modified):
        'Initialize the Info object.'
        self.__keys, self.__values, self.__modified = keys, values, modified

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self.__keys, self.__values, self.__modified)

    def __get_keys(self):
        'Private class method.'
        return self.__keys

    def __get_values(self):
        'Private class method.'
        return self.__values

    def __get_modified(self):
        'Private class method.'
        return self.__modified

    def __get_difference(self):
        'Private class method.'
        return time.time() + 11644473600.0 - self.__modified / 10000000.0

    keys = property(__get_keys, doc='Number of keys.')
    values = property(__get_values, doc='Number of values.')
    modified = property(__get_modified, doc='Time last modified.')
    difference = property(__get_difference, doc='Seconds since modified.')

################################################################################

if __name__ == '__main__':
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
