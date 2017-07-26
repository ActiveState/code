#!/usr/bin/python
from __future__ import with_statement

import sys
from StringIO import StringIO

__all__ = ['RedirectedIO', 'redirect_io']


class RedirectedIO(object):
    def __init__(self, target=None, mode='a+',
                 close_target=True):
        try:
            target = open(target, mode)
        except TypeError:
            if target is None:
                target = StringIO()
        self.target = target
        self.close_target = close_target

    def __enter__(self):
        """ Redirect IO to self.target.
        """
        self.original_stdout = sys.stdout
        sys.stdout = self.target
        return self.target

    def __exit__(self, *args, **kwargs):
        """ Restore stdio and close the file.
        """
        sys.stdout = self.original_stdout
        if self.close_target:
            self.target.close()


def redirect_io(target=None, mode='a+', keep_target=True):
    """ Returns a decorator that wrapps a
    function and redirects its IO to a target
    file (a StringIO by default). The target is
    available as .iotarget on the decorated function.
    """
    def dec(func):

        def wrapper(*args, **kwargs):
            with RedirectedIO(target, mode, not keep_target) as iotarget:
                result = func(*args, **kwargs)
                if keep_target:
                    wrapper.iotarget = iotarget
            return result

        wrapper.iotarget = None
        wrapper.__doc__ = func.__doc__
        wrapper.__name__ = func.__name__
        return wrapper

    return dec
