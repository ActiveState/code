import os
import tempfile

# This is the stupidest thing about POSIX and glibc, fixed only in Hurd: must
# change umask to be able read its value! Quantum umask!
my_umask = os.umask(0)
os.umask(my_umask)

class SafeOpen:
    '''Open a file for writing using safe atomic replacement

    Example usage:
    with SafeOpen(fname) as f:
        f.write('Hello World.\n')
    '''
    def __init__(self, target, mode='w', tempdir=None, prefix=None, perms=0666,
            use_umask=True):
        self.target = target
        assert mode in ['w', 'wb'], '(re)write is the only supported open mode!'
        self.mode = mode
        tdir, tname = os.path.split(target)
        assert tname, 'Remove slash at end of fname!'
        self.tdir = tempdir or tdir or '.' # in case dirname returns '' for
                                           # current dir...
        self.prefix = prefix or ('.%s.' % tname)
        self.perms = perms
        if use_umask:
            self.perms &= ~my_umask

    def __enter__(self):
        fd, self.tpath = tempfile.mkstemp(prefix=self.prefix, dir=self.tdir,
                text='b' not in self.mode)
        self.f = os.fdopen(fd, self.mode)
        return self.f

    def __exit__(self, exct, excv, exctb):
        self.f.close()
        if excv is None:
            os.chmod(self.tpath, self.perms)
            os.rename(self.tpath, self.target) # Unix only, meanless for Windows
                                               # with no atomic replace support
        else:
            # an error occurred, delete the file (and reraise exc)
            os.unlink(self.tpath)
        return False
