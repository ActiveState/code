#!/usr/bin/env python3
#-*- coding: iso-8859-1 -*-
################################################################################
#
# Parameter/return value type checking for Python 3 using function annotations.
#
# (c) 2008-2015, Dmitry Dvoinikov <dmitry@targeted.org>
# Distributed under BSD license.
#
# Samples:
#
# from typecheck import *
#
# @typecheck
# def foo(i: int, x = None, s: str = "default") -> bool:
#     ...
#
# @typecheck
# def foo(*args, k1: int, k2: str = "default", k3 = None) -> nothing:
#     ...
#
# @typecheck
# def foo(ostream: with_attr("write", "flush"), f: optional(callable) = None):
#     ...
#
# divisible_by_three = lambda x: x % 3 == 0
# @typecheck
# def foo(i: by_regex("^[0-9]+$")) -> divisible_by_three:
#     ...
#
# @typecheck
# def reverse_2_tuple(t: (str, bytes)) -> (bytes, str):
#     ...
#
# @typecheck
# def reverse_3_list(t: [int, float, bool]) -> [bool, float, int]:
#     ...
#
# @typecheck
# def extract_from_dict(d: dict_of(int, str), k: tuple_of(int)) -> list_of(str):
#     ...
#
# @typecheck
# def contains(x: int, xs: set_of(int)) -> bool:
#     ...
#
# @typecheck
# def set_level(level: one_of(1, 2, 3)):
#     ...
#
# @typecheck
# def accept_number(x: either(int, by_regex("^[0-9]+$"))):
#     ...
#
# @typecheck_with_exceptions(input_parameter_error = MemoryError):
# def custom_input_error(x: int): # now custom_input_error("foo") throws MemoryError
#     ...
#
# @typecheck_with_exceptions(return_value_error = TypeError):
# def custom_return_error() -> str: # now custom_return_error() throws TypeError
#     return 1
#
# The (6 times longer) source code with self-tests is available from:
# http://www.targeted.org/python/recipes/typecheck3000.py
#
################################################################################

__all__ = [

# decorators

"typecheck", "typecheck_with_exceptions",

# check predicates

"optional", "with_attr", "by_regex", "callable", "anything", "nothing",
"tuple_of", "list_of", "set_of", "dict_of", "one_of", "either",

# exceptions

"TypeCheckError", "TypeCheckSpecificationError",
"InputParameterError", "ReturnValueError",

# utility methods

"disable",

]

################################################################################

import inspect
import functools
import re

callable = lambda x: hasattr(x, "__call__")
anything = lambda x: True
nothing = lambda x: x is None

################################################################################

_enabled = True

def disable():
    global _enabled
    _enabled = False

################################################################################

class TypeCheckError(Exception): pass
class TypeCheckSpecificationError(Exception): pass
class InputParameterError(TypeCheckError): pass
class ReturnValueError(TypeCheckError): pass

################################################################################

class Checker:

    class NoValue:
        def __str__(self):
            return "<no value>"
    no_value = NoValue()

    _registered = []

    @classmethod
    def register(cls, predicate, factory):
        cls._registered.append((predicate, factory))

    @classmethod
    def create(cls, value):
        if isinstance(value, cls):
            return value
        for predicate, factory in cls._registered:
            if predicate(value):
                return factory(value)
        else:
            return None

    def __call__(self, value):
        return self.check(value)

################################################################################

class TypeChecker(Checker):

    def __init__(self, cls):
        self._cls = cls

    def check(self, value):
        return isinstance(value, self._cls)

Checker.register(inspect.isclass, TypeChecker)

################################################################################

iterable = lambda x: hasattr(x, "__iter__")

class IterableChecker(Checker):

    def __init__(self, cont):
        self._cls = type(cont)
        self._checks = tuple(Checker.create(x) for x in iter(cont))

    def check(self, value):
        if not iterable(value):
            return False
        vals = tuple(iter(value))
        return isinstance(value, self._cls) and len(self._checks) == len(vals) and \
               functools.reduce(lambda r, c_v: r and c_v[0].check(c_v[1]),
                                zip(self._checks, vals), True)

Checker.register(iterable, IterableChecker)

################################################################################

class CallableChecker(Checker):

    def __init__(self, func):
        self._func = func

    def check(self, value):
        return bool(self._func(value))

Checker.register(callable, CallableChecker)

################################################################################

class OptionalChecker(Checker):

    def __init__(self, check):
        self._check = Checker.create(check)

    def check(self, value):
        return value is Checker.no_value or value is None or self._check.check(value)

optional = OptionalChecker

################################################################################

class WithAttrChecker(Checker):

    def __init__(self, *attrs):
        self._attrs = attrs

    def check(self, value):
        for attr in self._attrs:
            if not hasattr(value, attr):
                return False
        else:
            return True

with_attr = WithAttrChecker

################################################################################

class ByRegexChecker(Checker):

    _regex_eols = { str: "$", bytes: b"$" }
    _value_eols = { str: "\n", bytes: b"\n" }

    def __init__(self, regex):
        self._regex_t = type(regex)
        self._regex = re.compile(regex)
        self._regex_eol = regex[-1:] == self._regex_eols.get(self._regex_t)
        self._value_eol = self._value_eols[self._regex_t]

    def check(self, value):
        return type(value) is self._regex_t and \
               (not self._regex_eol or not value.endswith(self._value_eol)) and \
               self._regex.match(value) is not None

by_regex = ByRegexChecker

################################################################################

class ContainerChecker(Checker):

    def __init__(self, check):
        self._check = Checker.create(check)

    def check(self, value):
        return isinstance(value, self.container) and \
               functools.reduce(lambda r, v: r and self._check.check(v), value, True)

################################################################################

class TupleOfChecker(ContainerChecker):

    container = tuple

tuple_of = TupleOfChecker

################################################################################

class ListOfChecker(ContainerChecker):

    container = list

list_of = ListOfChecker

################################################################################

class SetOfChecker(ContainerChecker):

    container = set

set_of = SetOfChecker

################################################################################

class DictOfChecker(Checker):

    def __init__(self, key_check, value_check):
        self._key_check = Checker.create(key_check)
        self._value_check = Checker.create(value_check)

    def check(self, value):
        return isinstance(value, dict) and \
               functools.reduce(lambda r, t: r and self._key_check.check(t[0]) and \
                                             self._value_check.check(t[1]),
                                value.items(), True)

dict_of = DictOfChecker

################################################################################

class OneOfChecker(Checker):

    def __init__(self, *values):
        self._values = values

    def check(self, value):
        return value in self._values

one_of = OneOfChecker

################################################################################

class EitherChecker(Checker):

    def __init__(self, *args):
        self._checks = tuple(Checker.create(arg) for arg in args)

    def check(self, value):
        for c in self._checks:
            if c.check(value):
                return True
        else:
            return False

either = EitherChecker

################################################################################

def typecheck(method, *, input_parameter_error = InputParameterError,
                         return_value_error = ReturnValueError):

    argspec = inspect.getfullargspec(method)
    if not argspec.annotations or not _enabled:
        return method

    default_arg_count = len(argspec.defaults or [])
    non_default_arg_count = len(argspec.args) - default_arg_count

    method_name = method.__name__
    arg_checkers = [None] * len(argspec.args)
    kwarg_checkers = {}
    return_checker = None
    kwarg_defaults = argspec.kwonlydefaults or {}

    for n, v in argspec.annotations.items():
        checker = Checker.create(v)
        if checker is None:
            raise TypeCheckSpecificationError("invalid typecheck for {0}".format(n))
        if n in argspec.kwonlyargs:
            if n in kwarg_defaults and \
               not checker.check(kwarg_defaults[n]):
                raise TypeCheckSpecificationError("the default value for {0} is incompatible "
                                                  "with its typecheck".format(n))
            kwarg_checkers[n] = checker
        elif n == "return":
            return_checker = checker
        else:
            i = argspec.args.index(n)
            if i >= non_default_arg_count and \
               not checker.check(argspec.defaults[i - non_default_arg_count]):
                raise TypeCheckSpecificationError("the default value for {0} is incompatible "
                                                  "with its typecheck".format(n))
            arg_checkers[i] = (n, checker)

    def typecheck_invocation_proxy(*args, **kwargs):

        for check, arg in zip(arg_checkers, args):
            if check is not None:
                arg_name, checker = check
                if not checker.check(arg):
                    raise input_parameter_error("{0}() has got an incompatible value "
                                                "for {1}: {2}".format(method_name, arg_name,
                                                                      str(arg) == "" and "''" or arg))

        for arg_name, checker in kwarg_checkers.items():
            kwarg = kwargs.get(arg_name, Checker.no_value)
            if not checker.check(kwarg):
                raise input_parameter_error("{0}() has got an incompatible value "
                                            "for {1}: {2}".format(method_name, arg_name,
                                                                  str(kwarg) == "" and "''" or kwarg))

        result = method(*args, **kwargs)

        if return_checker is not None and not return_checker.check(result):
            raise return_value_error("{0}() has returned an incompatible "
                                     "value: {1}".format(method_name, str(result) == "" and "''" or result))

        return result

    return functools.update_wrapper(typecheck_invocation_proxy, method,
                                    assigned = ("__name__", "__module__", "__doc__"))

################################################################################

_exception_class = lambda t: isinstance(t, type) and issubclass(t, Exception)

@typecheck
def typecheck_with_exceptions(*, input_parameter_error: optional(_exception_class) = InputParameterError,
                                 return_value_error: optional(_exception_class) = ReturnValueError):

    return lambda method: typecheck(method, input_parameter_error = input_parameter_error,
                                            return_value_error = return_value_error)

################################################################################
# EOF
