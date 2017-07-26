import collections, os.path
import _winreg

# Alternative to support unicode in Python 2
# http://pypi.python.org/pypi/winreg_unicode
#import winreg_unicode as _winreg 

for key in dir(_winreg):
    if key.startswith('HKEY_'):
        globals()[key[5:]] = getattr(_winreg, key)
del key

def interpret(value_type, value):
    if value_type == _winreg.REG_SZ:
        return value
    elif value_type == _winreg.REG_EXPAND_SZ:
        return os.path.expandvars(value)
    else:
        return None

class HiveKeyIterator(collections.KeysView):
    def __init__(self, hivekey):
        self._key = _winreg.OpenKey(hivekey._hive, hivekey._key)
        self._index = 0
        self._done = False

    def next(self):
        if self._done:
            raise StopIteration
        while True:
            for i in range(3):
                try:
                    name, data, data_type = _winreg.EnumValue(self._key,
                                                              self._index)
                    break
                except WindowsError:
                    continue
            else:
                self._done = True
                self._key.Close()
                raise StopIteration

            self._index += 1
            rv = interpret(data_type, name)
            if rv is not None:
                return rv

class HiveKey(collections.MutableMapping):
    def __init__(self, hive, key=''):
        self._hive = hive
        self._key = key

    def _getvalue(self, key, subkey):
        with _winreg.OpenKey(self._hive, key) as root_key:
            value, value_type = _winreg.QueryValueEx(root_key, subkey)
        rv = interpret(value_type, value)
        if rv is None:
            raise NotImplementedError('type: %d' % value_type)
        return rv

    def __getitem__(self, key):
        key, subkey = self._compute_subkey(key)
        try:
            return self._getvalue(key, subkey)
        except WindowsError:
            pass
        key = key + '\\' + subkey
        try:
            with _winreg.OpenKey(self._hive, key): # verify that key exists
                pass
        except WindowsError:
            raise KeyError
        return HiveKey(self._hive, key)

    def __iter__(self):
        return HiveKeyIterator(self)

    def __len__(self):
        "value is approximate since .keys() drops non-string types"
        with _winreg.OpenKey(self._hive, self._key) as k:
            num_subkeys, num_values, t = _winreg.QueryInfoKey(k)
            return num_values

    def _compute_subkey(self, k):
        key = (self._key + '\\' + k.strip('\\')).strip('\\')
        subkeys = key.split('\\')
        key = '\\'.join(subkeys[:-1])
        subkey = subkeys[-1]
        return key, subkey

    def __setitem__(self, k, v):
        if type(v) != type(u''):
            raise NotImplementedError
        key, subkey = self._compute_subkey(k)
        with _winreg.CreateKey(self._hive, key) as root_key:
            _winreg.SetValueEx(root_key, subkey, 0, _winreg.REG_SZ, v)

    def __delitem__(self, k):
        key, subkey = self._compute_subkey(k)
        with _winreg.OpenKey(self._hive, key,
                             0, _winreg.KEY_ALL_ACCESS) as root_key:
            try:
                _winreg.DeleteValue(root_key, subkey)
            except WindowsError:
                try:
                    _winreg.DeleteKey(root_key, subkey)
                except WindowsError:
                    raise KeyError

    def get_keys(self):
        values = []
        with _winreg.OpenKey(self._hive, self._key) as root_key:
            try:
                for i in range(100000):
                    key = _winreg.EnumKey(root_key, i)
                    if '\x00' in key: continue
                    values.append(key)
            except WindowsError:
                pass
        return values
