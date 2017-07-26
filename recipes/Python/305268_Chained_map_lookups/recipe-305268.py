import UserDict

class Chainmap(UserDict.DictMixin):
    """Combine multiple mappings for sequential lookup.

    For example, to emulate Python's normal lookup sequence:

        import __builtin__
        pylookup = Chainmap(locals(), globals(), vars(__builtin__))        
    """

    def __init__(self, *maps):
        self._maps = maps

    def __getitem__(self, key):
        for mapping in self._maps:
            try:
                return mapping[key]
            except KeyError:
                pass
        raise KeyError(key)

if __name__ == "__main__":
    d1 = {'a':1, 'b':2}
    d2 = {'a':3, 'd':4}
    cm = Chainmap(d1, d2)
    assert cm['a'] == 1
    assert cm['b'] == 2
    assert cm['d'] == 4
    try:
        print cm['f']
    except KeyError:
        pass
    else:
        raise Exception('Did not raise KeyError for missing key')
    assert 'a' in cm  and  'b' in cm  and  'd' in cm
    assert cm.get('a', 10) == 1
    assert cm.get('b', 20) == 2
    assert cm.get('d', 30) == 4
    assert cm.get('f', 40) == 40
