def iopen(name, mode='rU', buffering = -1):
    '''
    iopen(name, mode = 'rU', buffering = -1) -> file (that closes automatically)

    A version of open() that automatically closes the file explicitly
    when input is exhausted. Use this in place of calls to open()
    or file() that are not assigned to a name and so can't be closed
    explicitly. This ensures early close of files in Jython but is
    completely unnecessary in CPython.

    usage:
    from iopen import iopen
    print iopen('fname').read(),
    for l in iopen('fname'): print l,
    lines = [l for l in iopen('fname')]
    lines = iopen('fname').readlines()
    '''
    class Iopen(file):
        def next(self):
            try: return super(Iopen, self).next()
            except StopIteration: self.close(); raise
        def read(self, size = -1):
            data = super(Iopen, self).read(size)
            if size < 0 or not len(data): self.close()
            return data
        def readline(self, size = -1):
            data = super(Iopen, self).readline(size)
            if size != 0 and not len(data): self.close()
            return data
        def readlines(self, size = -1):
            data = super(Iopen, self).readlines(size)
            if size < 0 or not len(data): self.close()
            return data
    return Iopen(name, mode, buffering)
