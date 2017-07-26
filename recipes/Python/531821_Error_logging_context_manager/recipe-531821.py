from __future__ import with_statement
from contextlib import contextmanager
from functools import wraps

import logging

@contextmanager
def error_trapping(ident=None):
    ''' A context manager that traps and logs exception in its block.
        Usage:
        with error_trapping('optional description'):
            might_raise_exception()
        this_will_always_be_called()
    '''
    try:
        yield None
    except Exception:
        if ident:
            logging.error('Error in ' + ident, exc_info=True)
        else:
            logging.error('Error', exc_info=True)
            
            
def trap_errors(f):
    ''' A decorator to trap and log exceptions '''
    @wraps(f)
    def wrapper(*args, **kwds):
        with error_trapping(f.__name__):
            return f(*args, **kwds)
    return wrapper
