from __future__ import with_statement
from contextlib import contextmanager
import inspect

@contextmanager
def lexical_scope(*args):
    frame = inspect.currentframe().f_back.f_back
    saved = frame.f_locals.keys()
    try:
        if not args:
            yield
        elif len(args) == 1:
            yield args[0]
        else:
            yield args
    finally:
        f_locals = frame.f_locals
        for key in (x for x in f_locals.keys() if x not in saved):
            del f_locals[key]
        del frame


if __name__ == '__main__':

    b = 0

    with lexical_scope(1) as (a):
        print a
    with lexical_scope(1,2,3) as (a,b,c):
        print a,b,c

    with lexical_scope():
        d = 10

        def foo():
            pass

    print dir() # check those temporary variables are deleted.
    print b # XXX variable 'b' is alive.
