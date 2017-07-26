class PrefixStorage(object):
    """Storage for store information about prefixes.

    >>> s = PrefixStorage()

    First we save information for some prefixes:

    >>> s["123"] = "123 domain"
    >>> s["12"] = "12 domain"

    Then we can retrieve prefix information by full key
    (longest prefix always win):

    >>> s.getByPrefix("123456")
    '123 domain'
    >>> s.getByPrefix("12456")
    '12 domain'

    If no prefix has been found then getByPrefix() returns default value:

    >>> s.getByPrefix("13456", "None")
    'None'
    """

    def __init__(self):
        self._mapping = {}
        self._sizes = []

    def __setitem__(self, key, value):
        ln = len(key)
        if ln not in self._sizes:
            self._sizes.append(ln)
            self._sizes.sort()
            self._sizes.reverse()
        self._mapping[key] = value

    def getByPrefix(self, key, default=None):
        for ln in self._sizes:
            k = key[:ln]
            if k in self._mapping:
                return self._mapping[k]
        return default
