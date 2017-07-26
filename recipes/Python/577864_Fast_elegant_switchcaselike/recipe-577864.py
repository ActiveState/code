#!/usr/bin/env python
#
# Copyright (c) 2011 Jan Kaliszewski (zuo). All rights reserved.
# Licensed under the MIT License.
#
# Python 2.5+/3.x-compatibile.
#
# The newest version of this module should be downloadable from:
# https://github.com/zuo/Zuo-s-Recipes-and-Drafts/blob/master/caseswitch.py

from collections import defaultdict
import inspect

try: xrange
except NameError:
    xrange = range  # Py3.x

__all__ = 'with_switch', 'case', 'list_switch_factory', 'SwitchMeta', 'Switch'


#
# non-public stuff

class _DefaultCaseKey(object):
    def __repr__(self):
        return '<default>'

_DEF_CASE_KEY = _DefaultCaseKey()


# public classes and functions

def with_switch(cls):
    """
    Class decorator that adds two attributes to the `cls` class:

    * `switch` -- a defaultdict (or collection of other type, created with
      cls.custom_switch_factory) mapping case keys to case objects (that
      have been decorated with the @case() decorator;

    * `get_default_case` -- a static method that returns the default case
      object, i.e. one which has been decorated with @case(default=True)
      (or returns None if no object has been decorated in that way).

    Typically, case object is a callable method (but doesn't need to be).
    """
    keys_to_cases = {}
    for name, obj in inspect.getmembers(cls):
        for key in getattr(obj, '_switch_case_keys', ()):
            _obj = keys_to_cases.setdefault(key, obj)
            if _obj is not obj:
                raise ValueError('More than one case for key %r' % key)
    default_case = keys_to_cases.pop(_DEF_CASE_KEY, None)
    get_default_case = (lambda: default_case)
    switch_factory = getattr(cls, 'custom_switch_factory', defaultdict)
    kwargs = getattr(cls, 'custom_switch_factory_kwargs', {})
    cls.switch = switch_factory(get_default_case, keys_to_cases, **kwargs)
    cls.get_default_case = staticmethod(get_default_case)
    return cls

def case(*keys, **kwargs):
    """Decorator: tags an attribute (probably a method) as a case object."""
    keys = list(keys)
    _default = kwargs.pop('default', False)
    _itsname = kwargs.pop('itsname', False)
    _classmethod = kwargs.pop('classmethod', False)
    _staticmethod = kwargs.pop('staticmethod', True)  # default option
    if kwargs:
        raise TypeError(
            'case() got unexpected keyword arguments: %s' %
            ', '.join(sorted(kwargs)))
    def case_decorator(obj):
        if _default:
            keys.append(_DEF_CASE_KEY)
        if _itsname:
            keys.append(obj.__name__)
        obj._switch_case_keys = keys
        if _classmethod:
            return classmethod(obj)
        elif _staticmethod:
            return staticmethod(obj)
        else:
            return obj
    return case_decorator

@staticmethod
def list_switch_factory(get_default_case, keys_to_cases, length=1000):
    """
    Factory to create fast integer-only-based switches (using list-indexing).

    A usefule example of the optional 'custom_switch_factory' attribute value.
    """
    default_case = get_default_case()
    switch = [keys_to_cases.pop(key, default_case) for key in xrange(length)]
    if keys_to_cases:
        raise ValueError(
            'declared list length is too small for keys: ' +
            ', '.join(map(repr, sorted(keys_to_cases))))
    return switch


#
# convenience classes (any of them can be used *optionally*
# -- instead of using @with_switch directly)

class SwitchMeta(type):
    """Metaclass: decorates classes created by it with @with_switch."""
    def __new__(mcs, name, bases, attr_dict):
        return with_switch(type.__new__(mcs, name, bases, attr_dict))

# (here: Py2.x/3.x-compatibile way to create a class with a custom metaclass)
Switch = SwitchMeta(
    'Switch', (object,), {'__doc__':
    """SwitchMeta()-created class: decorates subclasses with @with_switch."""})




#
# some performance tests (with example switch declarations)...

if __name__ == '__main__':

    import random
    import sys
    import timeit


    # useful in most situations when the number of cases is not-so-small
    # (for small numbers the traditional if/elif/else approach seems to be
    # most efficient)
    class DefaultDictSwitch(Switch):

        @case(1)
        def one(arg):
            return 'one' + arg

        @case(2)
        def two(arg):
            return 'two' + arg

        @case(3)
        def three(arg):
            return 'three' + arg

        @case(4)
        def four(arg):
            return 'four' + arg

        @case(5)
        def five(arg):
            return 'five' + arg

        @case(6)
        def six(arg):
            return 'six' + arg

        @case(7)
        def seven(arg):
            return 'seven' + arg

        @case(8)
        def eight(arg):
            return 'eight' + arg

        @case(9)
        def nine(arg):
            return 'nine' + arg

        @case(10)
        def ten(arg):
            return 'ten' + arg

        @case(11)
        def eleven(arg):
            return 'eleven' + arg

        @case(12)
        def twelve(arg):
            return 'twelve' + arg

        @case(13)
        def thirteen(arg):
            return 'thirteen' + arg

        @case(14)
        def fourteen(arg):
            return 'fourteen' + arg

        @case(15)
        def fifteen(arg):
            return 'fifteen' + arg

        @case(16)
        def sixteen(arg):
            return 'sixteen' + arg

        @case(17, 71, 77)
        def seventeen_plus(arg):
            return 'seventeen_plus' + arg

        @case(18, 81, 88, 111, 118, 181, 188, 811, 818, 881, 888)
        def eighteen_plus(arg):
            return 'eighteen_plus' + arg

        @case(
            19, 91, 99, 119, 191, 199, 911, 919, 991, 999,
            1111, 1119, 1191, 1199, 1911, 1919, 1991, 1999,
            9111, 9119, 9191, 9199, 9911, 9919, 9991, 9999)
        def nineteen_plus(arg):
            return 'nineteen_plus' + arg

        @case(33, 333, 3333, default=True)
        def something_else(arg):
            return 'the default case' + arg


    # we add some cases, basing on an already defined switch class
    # (note that subclassing does not slow down the switch at all!)
    class AdminCommandSwitch(DefaultDictSwitch):

        @case(itsname=True)  # @case('shutdown') expressed in a DRY way
        def shutdown():
            return 'shutdown'

        @case('get-class', classmethod=True)
        def get_class(cls):
            return cls

        @case(*xrange(30000, 40000))
        def many_keys():
            return 'many_keys'


    # special-case optimization (for integer-only keys from a limited range)
    class ListBasedSwitch(DefaultDictSwitch):
        custom_switch_factory = list_switch_factory
        custom_switch_factory_kwargs = {'length': 10000}


    # no real advantages over DefaultDictSwitch (added here only to show that)
    class DictBasedSwitch(DefaultDictSwitch):
        custom_switch_factory = staticmethod(
            lambda get_default_case, keys_to_cases: dict(keys_to_cases))


    def test_standard():
        "standard switch (out-of-the-box default case support)"
        switch = DefaultDictSwitch.switch
        x = ''
        for key in case_keys:
            x = switch[key](x[:10])

    def test_standard2():
        "another standard switch -- subclass with more cases"
        switch = AdminCommandSwitch.switch
        x = ''
        for key in case_keys:
            x = switch[key](x[:10])
        assert switch['shutdown']() == 'shutdown'
        assert switch['get-class']() is AdminCommandSwitch
        assert switch[34567]() == 'many_keys'

    def test_list_based_range_default():
        "list-based switch (default case support for keys from the range)"
        switch = ListBasedSwitch.switch
        x = ''
        for key in case_keys:
            x = switch[key](x[:10])

    def test_list_based_with_try_except():
        "list-based switch + additional try/except-based default case support"
        switch = ListBasedSwitch.switch
        default_case = ListBasedSwitch.get_default_case()
        _error = IndexError
        x = ''
        for key in case_keys:
            try:
                x = switch[key](x[:10])
            except _error:
                x = default_case(x[:10])

    def test_dict_based_no_default():
        "ordinary-dict-based switch, no default case support"
        switch = DictBasedSwitch.switch
        x = ''
        for key in case_keys:
            x = switch[key](x[:10])

    def test_dict_based_with_get():
        "ordinary-dict-based switch + dict.get()-based default case support"
        switch = DictBasedSwitch.switch
        default_case = DictBasedSwitch.get_default_case()
        x = ''
        for key in case_keys:
            x = switch.get(key, default_case)(x[:10])

    def test_dict_based_with_try_except():
        "ordinary-dict-based switch + try/except-based default case support"
        switch = DictBasedSwitch.switch
        default_case = DictBasedSwitch.get_default_case()
        _error = KeyError
        x = ''
        for key in case_keys:
            try:
                x = switch[key](x[:10])
            except _error:
                x = default_case(x[:10])

    def test_if_elif():
        "traditional if/elif.../else sequence"
        x = ''
        for key in case_keys:
            if key == 1:
                x = 'one' + x[:10]
            elif key == 2:
                x = 'two' + x[:10]
            elif key == 3:
                x = 'three' + x[:10]
            elif key == 4:
                x = 'four' + x[:10]
            elif key == 5:
                x = 'five' + x[:10]
            elif key == 6:
                x = 'six' + x[:10]
            elif key == 7:
                x = 'seven' + x[:10]
            elif key == 8:
                x = 'eight' + x[:10]
            elif key == 9:
                x = 'nine' + x[:10]
            elif key == 10:
                x = 'ten' + x[:10]
            elif key == 11:
                x = 'eleven' + x[:10]
            elif key == 12:
                x = 'twelve' + x[:10]
            elif key == 13:
                x = 'thirteen' + x[:10]
            elif key == 14:
                x = 'fourteen' + x[:10]
            elif key == 15:
                x = 'fifteen' + x[:10]
            elif key == 16:
                x = 'sixteen' + x[:10]
            elif key in (17, 71, 77):
                x = 'seventeen_plus' + x[:10]
            elif key in (18, 81, 88, 111, 118, 181, 188, 811, 818, 881, 888):
                x = 'eighteen_plus' + x[:10]
            elif key in (
                  19, 91, 99, 111, 119, 191, 199, 911, 919, 991, 999,
                  1111, 1119, 1191, 1199, 1911, 1919, 1991, 1999):
                x = 'nineteen_plus' + x[:10]
            else:
                x = 'the default case' + x[:10]

    def test_tour(test_seq, msg, case_keys_choice, case_keys_length=1000000):
        global case_keys
        case_keys_choice = sorted(case_keys_choice)
        print(
            '\ngenerating random-ordered, %d-item-long, '
            'sequence of keys from the set: {%s}...' %
            (case_keys_length, ', '.join(map(repr, case_keys_choice))))
        case_keys = [
            random.choice(case_keys_choice) for i in xrange(case_keys_length)]
        print('\n' + msg)
        fastest_tests = []
        for test in test_seq:
            try:
                results = timeit.Timer(
                    'test()',
                    'from __main__ import %s as test' % test.__name__,
                ).repeat(number=1, repeat=3)
            except Exception:
                print('* %s: [could not be used]' % test.__doc__)
            else:
                fastest = min(results)
                print('* %s: %s (fastest: %f)' % (
                    test.__doc__,
                    ', '.join('%f' % t for t in results),
                    fastest))
                fastest_tests.append((fastest, test.__doc__))
        if fastest_tests:
            print('\nthe winner is: %f/%s' % (min(fastest_tests)))


    print('%r simple performance tests' % sys.argv[0])

    test_seq = (
        test_if_elif,
        test_standard,
        test_standard2,
        test_list_based_range_default,
        test_list_based_with_try_except,
        test_dict_based_no_default,
        test_dict_based_with_get,
        test_dict_based_with_try_except,
    )

    test_tour(
        test_seq,
        'test tour #1 (default cases not used; small number of keys):',
        case_keys_choice = tuple(xrange(1, 10)))

    test_tour(
        test_seq,
        'test tour #2 (default cases not used; not-so-small number of keys):',
        case_keys_choice = (tuple(xrange(1, 20)) + (
            71, 77, 18, 81, 88, 111, 118, 181, 188, 811, 818, 881, 888,
            91, 99, 119, 191, 199, 911, 919, 991, 999,
            1111, 1119, 1191, 1199, 1911, 1919, 1991, 1999,
            9111, 9119, 9191, 9199, 9911, 9919, 9991, 9999)))

    test_tour(
        test_seq,
        'test tour #3 (using default cases, keys in list-based switch range):',
        # about half of the keys do not have their cases (default case is used)
        case_keys_choice = (tuple(xrange(1, 70)) + (
            71, 77, 18, 81, 88, 111, 118, 181, 188, 811, 818, 881, 888,
            91, 99, 119, 191, 199, 911, 919, 991, 999,
            1111, 1119, 1191, 1199, 1911, 1919, 1991, 1999,
            9111, 9119, 9191, 9199, 9911, 9919, 9991, 9999)))

    test_tour(
        test_seq,
        'test tour #4 (using default cases, their keys not in that range):',
        # about half of the keys do not have their cases (default case is used)
        # + that keys are not in the list-based switch key range
        case_keys_choice=(tuple(xrange(1, 20)) + (
            71, 77, 18, 81, 88, 111, 118, 181, 188, 811, 818, 881, 888,
            91, 99, 119, 191, 199, 911, 919, 991, 999,
            1111, 1119, 1191, 1199, 1911, 1919, 1991, 1999,
            9111, 9119, 9191, 9199, 9911, 9919, 9991, 9999) +
            tuple(xrange(10000, 10050))))
