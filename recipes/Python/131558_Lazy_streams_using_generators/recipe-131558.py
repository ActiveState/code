class _stream_iter:
    def __init__(self, s):
        self.stream = s
        self.i = 0
    def next(self):
        try:
            val = self.stream[self.i]
        except IndexError: raise StopIteration
        self.i += 1
        return val

class stream(list):
    def __init__(self, iterator):
        list.__init__(self)
        self.it = iterator
        self.length = 0
        self.done = 0
    def __iter__(self):
        return _stream_iter(self)
    def __getitem__(self, i):
        if i >= self.length or self.length == 0:
            for j in range(i + 1 - self.length):
                self.append(self.it.next())
            self.length = i+1
        elif i < 0:
            for i in self.it:
                self.append(i)
            self.length = self.__len__()
        return list.__getitem__(self, i)
    def __getslice__(self, i, j):
        junk, junk = self[i], self[j]
        return list.__getslice__(self, i, j)
    def __repr__(self):
        return '<stream instance at 0x%x, %r materialized>' \
               % (id(self), list.__repr__(self))
                
