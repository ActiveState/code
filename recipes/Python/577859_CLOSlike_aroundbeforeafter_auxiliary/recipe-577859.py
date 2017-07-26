#!/usr/bin/env python
#
# Copyright (c) 2011 Jan Kaliszewski (zuo). All rights reserved.
# Licensed under the MIT License.
#
# Python 2.5+/3.x-compatibile.
#
# The newest version of this module should be downloadable from:
# https://github.com/zuo/Zuo-s-Recipes-and-Drafts/blob/master/auxmethods.py

from __future__ import with_statement  # (Py2.5 needs this)

from functools import wraps
from inspect import getmro, isfunction

__all__ = (
    'ClassNameConflictError',
    'aux', 'primary',
    'AutoAuxBase', 'AutoAuxMeta',
)


#
# exceptions

class ClassNameConflictError(Exception):
    """
    Conflict: class names are identical after stripping leading underscores.
    """

    def __str__(self):
        cls1, cls2 = self.args
        return (
            'Class names: %r and %r -- are identical after stripping leading '
            'underscores, which is forbidden when using aux/primary methods.'
            % (cls1.__name__, cls2.__name__))


#
# non-public stuff

_SUFFIXES = '_primary', '_before', '_after', '_around'


class _WrappedMethodPlaceholder(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        raise TypeError('method placeholder is not callable '
                        '(forgot to apply aux() class decorator?)')


def _next_around(obj_around, self, basename, *args, **kwargs):
    # try to get and call next `around` aux method
    meth_around = getattr(obj_around, basename + '_around', None)
    if meth_around is not None:
        return meth_around(*args, **kwargs)
    else:
        # if there is no more `around` methods, get and call:
        # `before` aux method (it can call superclasses' `before` methods)
        meth_before = getattr(self, basename + '_before', None)
        if meth_before is not None:
            meth_before(*args, **kwargs)
        # primary method (it can call superclasses' primary methods)
        meth_primary = getattr(self, basename + '_primary')
        pri_result = meth_primary(*args, **kwargs)
        # `after` aux method (it can call superclasses' `after` methods)
        meth_after = getattr(self, basename + '_after', None)
        if meth_after is not None:
            meth_after(*args, **kwargs)
        return pri_result

def _provide_wrapper(cls, func, basename):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return _next_around(self, self, basename, *args, **kwargs)
    added_doc = '(See: %s%s() signature).' % (basename, '_primary')
    existing_doc = (getattr(wrapper, '__doc__', None) or '').rstrip()
    if existing_doc:
        wrapper.__doc__ = '%s\n\n%s' % (existing_doc, added_doc)
    else:
        wrapper.__doc__ = added_doc
    setattr(cls, basename, wrapper)

def _provide_primary(cls, func, basename):
    suffixed_name = basename + '_primary'
    func.__name__ = suffixed_name
    func.__doc__ = (
        'The actual method implementation '
        '(%s() is only a wrapper).' % basename)
    setattr(cls, suffixed_name, func)

def _provide_wrapped_primary(cls, func):
    basename = func.__name__
    _provide_wrapper(cls, func, basename)
    _provide_primary(cls, func, basename)

def _strip_and_check_cls_name(cls):
    cls_stripped_name = cls.__name__.lstrip('_')
    for supercls in getmro(cls):
        if (supercls is not cls and
              cls_stripped_name == supercls.__name__.lstrip('_')):
            raise ClassNameConflictError(supercls, cls)
    return cls_stripped_name

def _provide_call_next(cls, suffixed_name):
    cls_stripped_name = _strip_and_check_cls_name(cls)
    basename, qualifier = suffixed_name.rsplit('_', 1)
    cn_name = '_%s__%s' % (
        cls_stripped_name,
        (basename if qualifier == 'primary' else suffixed_name))
    if cn_name in vars(cls):
        return
    if qualifier == 'around':
        def call_next(self, *args, **kwargs):
            return _next_around(
                super(cls, self), self, basename, *args, **kwargs)
    else:
        def call_next(self, *args, **kwargs):
            super_meth = getattr(super(cls, self), suffixed_name, None)
            if super_meth is not None:
                return super_meth(*args, **kwargs)
    call_next.__name__ = cn_name
    setattr(cls, cn_name, call_next)


#
# actual decorators

def aux(cls):
    """Class decorator (for classes containing primary and/or aux methods)."""
    if not isinstance(cls, type):
        raise TypeError('%r is not a type' % cls)
    # wrap/rename primary methods
    for name, obj in tuple(vars(cls).items()):  # (Py2.x/3.x-compatibile way)
        if isinstance(obj, _WrappedMethodPlaceholder):
            _provide_wrapped_primary(cls, obj.func)
    # provide `call-next-method`-like methods
    for name, obj in tuple(vars(cls).items()):
        if isfunction(obj) and obj.__name__.endswith(_SUFFIXES):
            _provide_call_next(cls, obj.__name__)
    return cls

def primary(func):
    """Method decorator (for primary methods only)."""
    if not isfunction(func):
        raise TypeError('%r is not a function' % func)
    return _WrappedMethodPlaceholder(func)


#
# convenience classes (any of them can be used *optionally*...)

class AutoAuxMeta(type):
    """Convenience metaclass: `aux()`-decorates classes created by it."""
    def __new__(mcs, name, bases, attr_dict):
        return aux(type.__new__(mcs, name, bases, attr_dict))

# (here: Py2.x/3.x-compatibile way to create a class with a custom metaclass)
AutoAuxBase = AutoAuxMeta('AutoAuxBase', (object,), {'__doc__':
    """`AutoAuxMeta`-created base class: `aux()`-decorates its subclasses."""})


#
# basic example

if __name__ == '__main__':

    import sys
    import time

    class TimedAction(AutoAuxBase):
        # note: AutoAuxBase automatically decorates your classes with aux()

        def action_before(self, *args, **kwargs):
            """Start action timer."""
            print('starting action timer...')
            self.start_time = time.time()

        def action_after(self, *args, **kwargs):
            """Stop action timer and report measured duration."""
            self.action_duration = time.time() - self.start_time
            print('action duration: %f' % self.action_duration)


    class FileContentAction(AutoAuxBase):

        def action_around(self, path):
            """Read file and pass its content on; report success or error."""
            print('opening file %r...' % path)
            try:
                with open(path) as f:
                    content = f.read()
            except EnvironmentError:
                print(sys.exc_info()[1])
            else:
                result = self.__action_around(path, content)
                print('file %r processed successfully' % path)
                return result


    class NewlinesCounter(FileContentAction, TimedAction):

        item_descr = 'newlines'

        @primary
        def action(self, path, content):
            """Get number of newlines in a given string."""
            return content.count('\n')

        def action_before(self, path, *args):
            """Print a message and go on..."""
            print('counting %s in file %r will start...' % (
                self.item_descr, path))
            self.__action_before(path, *args)

        def action_around(self, path):
            """Start operation with given file path. Finally, show summary."""
            result = self.__action_around(path)
            if result is not None:
                print('%s in file %r: %s\n' % (
                    self.item_descr, path, result))
            else:
                print('could not count %s in file %r\n' % (
                    self.item_descr, path))
            return result


    class SpacesAndNewlinesCounter(NewlinesCounter):

        item_descr = 'spaces and newlines'

        @primary
        def action(self, path, content):
            """Get number of spaces and newlines in a given string."""
            spaces = content.count(' ')
            newlines = self.__action(path, content)
            return spaces + newlines


    example_file_paths = __file__, 'spam/spam/spam/non-existent'

    nl_counter = NewlinesCounter()
    spc_nl_counter = SpacesAndNewlinesCounter()

    for path in example_file_paths:
        nl_counter.action(path)
        spc_nl_counter.action(path)
