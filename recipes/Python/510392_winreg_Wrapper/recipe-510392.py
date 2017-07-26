'''Module for accessing MWR.

This module provides an advanced, easy-to-use API for
accessing and mutating the Microsoft Windows Registry.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'March 19, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
B. Gates, for creating the Windows Registry.
F. Drake, for enforcing good Python documentation.'''

################################################################################

import _winreg
import sys as _sys
import time as _time

################################################################################

class HKEY:
    'Hive Constants'
    CLASSES_ROOT = -2147483648
    CURRENT_USER = -2147483647
    LOCAL_MACHINE = -2147483646
    USERS = -2147483645
    CURRENT_CONFIG = -2147483643

class KEY:
    'Mode Constants'
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

class _Value(object):

    '_Value(value) -> _Value'

    def __init__(self, value):
        'Initialize the _Value object.'
        self.__value = value
        self.__repr = '%s(%r)' % (self.__class__.__name__, value)

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def __get_value(self):
        'Private class method.'
        return self.__value

    value = property(__get_value, doc='Value of this object.')

class REG_NONE(_Value): pass
class REG_SZ(_Value): pass
class REG_EXPAND_SZ(_Value): pass
class REG_BINARY(_Value): pass
class REG_DWORD(_Value): pass
class REG_DWORD_BIG_ENDIAN(_Value): pass
class REG_LINK(_Value): pass
class REG_MULTI_SZ(_Value): pass
class REG_RESOURCE_LIST(_Value): pass
class REG_FULL_RESOURCE_DESCRIPTOR(_Value): pass
class REG_RESOURCE_REQUIREMENTS_LIST(_Value): pass
class REG_QWORD(_Value): pass

################################################################################

class Registry(object):

    'Registry([computer]) -> Registry'

    def __init__(self, computer=None):
        'Initialize the Registry object.'
        self.__computer = computer
        self.__repr = 'Registry()' if computer is None else 'Registry(%r)' % computer

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def __iter__(self):
        'Iterate over hives defined in HKEY.'
        return (Key(key, computer=self.__computer) for key in map(HKEY.__dict__.__getitem__, filter(str.isupper, dir(HKEY))))

    def __HKEY_CLASSES_ROOT(self):
        'Private class method.'
        return Key(HKEY.CLASSES_ROOT, computer=self.__computer)

    def __HKEY_CURRENT_USER(self):
        'Private class method.'
        return Key(HKEY.CURRENT_USER, computer=self.__computer)

    def __HKEY_LOCAL_MACHINE(self):
        'Private class method.'
        return Key(HKEY.LOCAL_MACHINE, computer=self.__computer)

    def __HKEY_USERS(self):
        'Private class method.'
        return Key(HKEY.USERS, computer=self.__computer)

    def __HKEY_CURRENT_CONFIG(self):
        'Private class method.'
        return Key(HKEY.CURRENT_CONFIG, computer=self.__computer)

    HKEY_CLASSES_ROOT = property(__HKEY_CLASSES_ROOT, doc='The CLASSES_ROOT hive.')
    HKEY_CURRENT_USER = property(__HKEY_CURRENT_USER, doc='The CURRENT_USER hive.')
    HKEY_LOCAL_MACHINE = property(__HKEY_LOCAL_MACHINE, doc='The LOCAL_MACHINE hive.')
    HKEY_USERS = property(__HKEY_USERS, doc='The USERS hive.')
    HKEY_CURRENT_CONFIG = property(__HKEY_CURRENT_CONFIG, doc='The CURRENT_CONFIG hive.')

################################################################################

class Key(object):

    '''Key(key[, subkey][, mode][, computer]) -> Key

    Key(key) -> Key
    Key(key, subkey) -> Key
    Key(key, mode=value) -> Key
    Key(key, subkey, mode) -> Key
    Key(key, computer=value) -> Key
    Key(key, subkey, computer=value) -> Key
    Key(key, mode=value, computer=value) -> Key
    Key(key, subkey, mode, computer) -> Key'''

    def __init__(self, key, subkey=None, mode=None, computer=None):
        'Initialize the Key object.'
        if isinstance(key, (int, _winreg.HKEYType)) and subkey is None and mode is None and computer is None:
            self.__key = _winreg.OpenKey(key, '')
        elif isinstance(key, Key) and subkey is None and mode is None and computer is None:
            self.__key = _winreg.OpenKey(key.__key, '')
        elif isinstance(key, (int, _winreg.HKEYType)) and isinstance(subkey, str) and mode is None and computer is None:
            self.__key = _winreg.OpenKey(key, subkey)
        elif isinstance(key, Key) and isinstance(subkey, str) and mode is None and computer is None:
            self.__key = _winreg.OpenKey(key.__key, subkey)
        elif isinstance(key, (int, _winreg.HKEYType)) and subkey is None and isinstance(mode, int) and computer is None:
            self.__key = _winreg.OpenKey(key, '', 0, mode)
        elif isinstance(key, Key) and subkey is None and isinstance(mode, int) and computer is None:
            self.__key = _winreg.OpenKey(key.__key, '', 0, mode)
        elif isinstance(key, (int, _winreg.HKEYType)) and isinstance(subkey, str) and isinstance(mode, int) and computer is None:
            self.__key = _winreg.OpenKey(key, subkey, 0, mode)
        elif isinstance(key, Key) and isinstance(subkey, str) and isinstance(mode, int) and computer is None:
            self.__key = _winreg.OpenKey(key.__key, subkey, 0, mode)
        elif isinstance(key, int) and subkey is None and mode is None and isinstance(computer, str):
            self.__key = _winreg.ConnectRegistry(computer, key)
        elif isinstance(key, int) and isinstance(subkey, str) and mode is None and isinstance(computer, str):
            self.__key = _winreg.OpenKey(_winreg.ConnectRegistry(computer, key), subkey)
        elif isinstance(key, int) and subkey is None and isinstance(mode, int) and isinstance(computer, str):
            self.__key = _winreg.OpenKey(_winreg.ConnectRegistry(computer, key), '', 0, mode)
        elif isinstance(key, int) and isinstance(subkey, str) and isinstance(mode, int) and isinstance(computer, str):
            self.__key = _winreg.OpenKey(_winreg.ConnectRegistry(computer, key), subkey, 0, mode)
        else:
            raise TypeError, 'Please check documentation.'
        self.__keys = Keys(self.__key)
        self.__values = Values(self.__key)
        self.__repr = 'Key(%s)' % ', '.join([repr(key)] + ['%s=%r' % (key, value) for key, value in zip(('subkey', 'mode', 'computer'), (subkey, mode, computer)) if value is not None])

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def save(self, file_name):
        'Save this key to file.'
        _winreg.SaveKey(self.__key, file_name)

    def load(self, subkey, file_name):
        'Load subkey from file.'
        _winreg.LoadKey(self.__key, subkey, file_name)

    def __get_keys(self):
        'Private class method.'
        return self.__keys

    def __set_keys(self, keys):
        'Private class method.'
        if isinstance(keys, str):
            _winreg.CreateKey(self.__key, keys)
        elif isinstance(keys, (list, tuple)):
            for key in keys:
                self.keys = key
        else:
            raise TypeError, 'Key Could Not Be Created'

    def __del_keys(self):
        'Private class method.'
        try:
            while True:
                _winreg.DeleteKey(self.__key, _winreg.EnumKey(self.__key, 0))
        except EnvironmentError:
            pass

    def __get_values(self):
        'Private class method.'
        return self.__values

    def __set_values(self, values):
        'Private class method.'
        if isinstance(values, str):
            _winreg.SetValueEx(self.__key, values, 0, REG.SZ, _winreg.QueryValue(self.__key, ''))
        elif isinstance(values, (list, tuple)):
            for value in values:
                self.values = value
        else:
            raise TypeError, 'Value Could Not Be Created'

    def __del_values(self):
        'Private class method.'
        try:
            while True:
                _winreg.DeleteValue(self.__key, _winreg.EnumValue(self.__key, 0)[0])
        except EnvironmentError:
            pass

    def __get_value(self):
        'Private class method.'
        return _winreg.QueryValue(self.__key, '')

    def __set_value(self, value):
        'Private class method.'
        _winreg.SetValue(self.__key, '', REG.SZ, value)

    def __del_value(self):
        'Private class method.'
        _winreg.DeleteValue(self.__key, '')

    def __get_info(self):
        'Private class method.'
        return Info(*_winreg.QueryInfoKey(self.__key))

    keys = property(__get_keys, __set_keys, __del_keys, 'Keys of this key.')
    values = property(__get_values, __set_values, __del_values, 'Values of this key.')
    value = property(__get_value, __set_value, __del_value, 'Value of this key.')
    info = property(__get_info, doc='Information about this key.')

################################################################################

class Keys(object):

    'Keys(key) -> Keys'

    def __init__(self, key):
        'Initialize the Keys object.'
        self.__key = key
        self.__repr = 'Keys(%r)' % key

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def __len__(self):
        'Return the number of keys.'
        return _winreg.QueryInfoKey(self.__key)[0]

    def __getitem__(self, key):
        'Return the specified key.'
        return Key(self.__key, key)

    def __setitem__(self, key, value):
        'Assign the item to a key.'
        key = Key(_winreg.CreateKey(self.__key, key), mode=KEY.ALL_ACCESS)
        for name in value.values:
            key.values[name] = value.values[name]
        for name in value.keys:
            key.keys[name] = value.keys[name]

    def __delitem__(self, key):
        'Delete the specified key.'
        _winreg.DeleteKey(self.__key, key)

    def __iter__(self):
        'Iterate over the key names.'
        return iter(tuple(_winreg.EnumKey(self.__key, index) for index in xrange(_winreg.QueryInfoKey(self.__key)[0])))

    def __contains__(self, item):
        'Check for a key\'s existence.'
        item = item.lower()
        for index in xrange(_winreg.QueryInfoKey(self.__key)[0]):
            if _winreg.EnumKey(self.__key, index).lower() == item:
                return True
        return False

################################################################################

class Values(object):

    'Values(key) -> Values'

    TYPES = REG_NONE, REG_SZ, REG_EXPAND_SZ, REG_BINARY, REG_DWORD, REG_DWORD_BIG_ENDIAN, REG_LINK, REG_MULTI_SZ, REG_RESOURCE_LIST, REG_FULL_RESOURCE_DESCRIPTOR, REG_RESOURCE_REQUIREMENTS_LIST, REG_QWORD

    def __init__(self, key):
        'Initialize the Values object.'
        self.__key = key
        self.__repr = 'Values(%r)' % key

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def __len__(self):
        'Return the number of values.'
        return _winreg.QueryInfoKey(self.__key)[1]

    def __getitem__(self, key):
        'Return the specified value.'
        item_value, item_type = _winreg.QueryValueEx(self.__key, key)
        return self.TYPES[item_type](item_value)

    def __setitem__(self, key, value):
        'Assign the item to a value.'
        if isinstance(value, self.TYPES):
            _winreg.SetValueEx(self.__key, key, 0, list(self.TYPES).index(value.__class__), value.value)
        else:
            _winreg.SetValueEx(self.__key, key, 0, _winreg.QueryValueEx(self.__key, key)[1], value)

    def __delitem__(self, key):
        'Delete the specified value.'
        _winreg.DeleteValue(self.__key, key)

    def __iter__(self):
        'Iterate over the value names.'
        return iter(tuple(_winreg.EnumValue(self.__key, index)[0] for index in xrange(_winreg.QueryInfoKey(self.__key)[1])))

    def __contains__(self, item):
        'Check for a value\'s existence.'
        item = item.lower()
        for index in xrange(_winreg.QueryInfoKey(self.__key)[1]):
            if _winreg.EnumValue(self.__key, index)[0].lower() == item:
                return True
        return False

################################################################################

class Info(object):

    'Info(keys, values, modified) -> Info'

    def __init__(self, keys, values, modified):
        'Initialize the Info object.'
        self.__keys = keys
        self.__values = values
        self.__modified = modified
        self.__repr = 'Info(%r, %r, %r)' % (keys, values, modified)

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

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
        return _time.time() + 11644473600.0 - self.__modified / 10000000.0

    keys = property(__get_keys, doc='Number of keys.')
    values = property(__get_values, doc='Number of values.')
    modified = property(__get_modified, doc='Time last modified.')
    difference = property(__get_difference, doc='Seconds since modified.')

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
