from __future__ import with_statement
from contextlib import contextmanager


@contextmanager
def redirect(object_, attr, value):
    orig = getattr(object_, attr)
    setattr(object_, attr, value)
    yield
    setattr(object_, attr, orig)

if __name__ == "__main__":
    import sys
    with redirect(sys, 'stdout', open('stdout', 'w')):
        print "hello"

    print "we're back"

        
