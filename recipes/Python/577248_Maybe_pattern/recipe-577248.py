#!/usr/bin/env python
# -*- coding: utf-8 -*-

NOVALUE = object()

class Maybe(object):
    _has_value = False
    _value = None
    def __init__(self, value):
        if value is not NOVALUE:
            self._has_value = True
            self._value = value

    def __nonzero__(self):
        return self.has_value

    @property
    def has_value(self):
        return self._has_value

    @property
    def value(self):
        return self._value

# optional sugar factories
def Some(value):
    return Maybe(value)

def NoValue():
    return Maybe(NOVALUE)

if __name__ == "__main__":
    class MaybeSupportingRepository(object):
        def __init__(self, *args):
            self._d = dict(args)

        def get(self, key):
            return Maybe(self._d.get(key, NOVALUE))
 
    repo = MaybeSupportingRepository( ("a", 1), ("b", 2), ("c", 3) )

    key = "x"
    maybe_v = repo.get(key)
    if maybe_v:
        print "There's a value for %s: %s" % (key, maybe_v.value)
    else:
        print "There's no value for %s" % key

    key = "a"
    maybe_v = repo.get(key)
    if maybe_v.has_value:
        print "There's a value for %s: %s" % (key, maybe_v.value)
    else:
        print "There's no value for %s" % key
