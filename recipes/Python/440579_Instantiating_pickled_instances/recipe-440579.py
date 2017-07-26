import os
import cPickle as pickle

__all__ = ['autopickle', 'BINMODE']

# whether the pickled files are binary
BINMODE = False

def autopickle(__init__):
    """Decorator for instantiating pickled instances transparently."""

    def new__init__(self, *args, **kwds):
        picklename = self.getPickleFilename(*args, **kwds)
        if os.path.exists(picklename):
            newSelf = pickle.load(open(picklename))
            assert type(newSelf) is type(self)
            # copy newSelf to self
            if hasattr(newSelf, '__getstate__'):
                state = newSelf.__getstate__()
            else:
                state = newSelf.__dict__
            if hasattr(self, '__setstate__'):
                self.__setstate__(state)
            else:
                self.__dict__.update(state)
        else:
            __init__(self, *args, **kwds)
            picklefile = open(picklename, BINMODE and 'wb' or 'w')
            try: pickle.dump(self, picklefile, BINMODE)
            finally: picklefile.close()
    return new__init__


if __name__ == '__main__':

    class Foo(object):
        @autopickle
        def __init__(self, id):
            import time; time.sleep(2)
            self.id = id
        def getPickleFilename(self, id):
            return "%s.dat" % id

    print Foo(1)
