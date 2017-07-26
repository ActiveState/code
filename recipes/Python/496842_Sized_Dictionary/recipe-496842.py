import time

class SizedDict(dict):
    ''' Sized dictionary without timeout. '''

    def __init__(self, size=1000):
        dict.__init__(self)
        self._maxsize = size
        self._stack = []

    def __setitem__(self, name, value):
        if len(self._stack) >= self._maxsize:
            self.__delitem__(self._stack[0])
            del self._stack[0]
        self._stack.append(name)
        return dict.__setitem__(self, name, value)

    # Recommended but not required:
    def get(self, name, default=None, do_set=False):
        try:
            return self.__getitem__(name)
        except KeyError:
            if default is not None:
                if do_set:
                    self.__setitem__(name, default)
                return default
            else:
                raise

class CacheDict(dict):
    ''' A sized dictionary with a timeout (seconds) '''

    def __init__(self, size=1000, timeout=None):
        dict.__init__(self)
        self._maxsize = size
        self._stack = []
        self._timeout = timeout

    def __setitem__(self, name, value, timeout=None):
        if len(self._stack) >= self._maxsize:
            self.__delitem__(self._stack[0])
            del self._stack[0]
        if timeout is None:
            timeout = self._timeout
        if timeout is not None:
            timeout = time.time() + timeout
        self._stack.append(name)
        dict.__setitem__(self, name, (value, timeout))

    def get(self, name, default=None):
        try:
            focus = self.__getitem__(name)
            if focus[1] is not None:
                if focus[1] < time.time():
                    self.__delitem__(name)
                    self._stack.remove(name)
                    raise KeyError
            return focus[0]
        except KeyError:
            return default

#sample usage:
# d = SizedDict()
# for i in xrange(10000): d[i] = 'test'
# print len(d)
