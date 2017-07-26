#!/usr/bin/env python3
#-*- coding: iso-8859-1 -*-
################################################################################
#
# Function guards for Python 3.
#
# (c) 2016, Dmitry Dvoinikov <dmitry@targeted.org>
# Distributed under MIT license.
#
# Samples:
#
# from funcguard import guard
#
# @guard
# def abs(a, _when = "a >= 0"):
#     return a
#
# @guard
# def abs(a, _when = "a < 0"):
#     return -a
#
# assert abs(1) == abs(-1) == 1
#
# @guard
# def factorial(n): # no _when expression => default
#    return 1
#
# @guard
# def factorial(n, _when = "n > 1"):
#    return n * factorial(n - 1)
#
# assert factorial(10) == 3628800
#
# class TypeTeller:
#     @staticmethod
#     @guard
#     def typeof(value, _when = "isinstance(value, int)"):
#         return int
#     @staticmethod
#     @guard
#     def typeof(value, _when = "isinstance(value, str)"):
#         return str
#
# assert TypeTeller.typeof(0) is int
# TypeTeller.typeof(0.0) # throws
#
# class AllowedProcessor:
#     def __init__(self, allowed):
#         self._allowed = allowed
#     @guard
#     def process(self, value, _when = "value in self._allowed"):
#         return "ok"
#     @guard
#     def process(self, value): # no _when expression => default
#         return "fail"
#
# ap = AllowedProcessor({1, 2, 3})
# assert ap.process(1) == "ok"
# assert ap.process(0) == "fail"
#
# guard.default_eval_args( # values to insert to all guards scopes
#     office_hours = lambda: 9 <= datetime.now().hour < 18)
#
# @guard
# def at_work(*args, _when = "office_hours()", **kwargs):
#     print("welcome")
#
# @guard
# def at_work(*args, **kwargs):
#     print("come back tomorrow")
#
# at_work() # either "welcome" or "come back tomorrow"
#
# The complete source code with self-tests is available from:
# https://github.com/targeted/funcguard
#
################################################################################

__all__ = [ "guard", "GuardException", "IncompatibleFunctionsException",
            "FunctionArgumentsMatchException", "GuardExpressionException",
            "DuplicateDefaultGuardException", "GuardEvalException",
            "NoMatchingFunctionException" ]

################################################################################

import inspect; from inspect import getfullargspec
import functools; from functools import wraps
import sys; from sys import modules
try:
    (lambda: None).__qualname__
except AttributeError:
    import qualname; from qualname import qualname # prior to Python 3.3 workaround
else:
    qualname = lambda f: f.__qualname__

################################################################################

class GuardException(Exception): pass
class IncompatibleFunctionsException(GuardException): pass
class FunctionArgumentsMatchException(GuardException): pass
class GuardExpressionException(GuardException): pass
class DuplicateDefaultGuardException(GuardException): pass
class GuardEvalException(GuardException): pass
class NoMatchingFunctionException(GuardException): pass

################################################################################
# takes an argument specification for a function and a set of actual call
# positional and keyword arguments, returns a flat namespace-like dict
# mapping parameter names to their actual values

def _eval_args(argspec, args, kwargs):

    # match positional arguments

    matched_args = {}
    expected_args = argspec.args
    default_args = argspec.defaults or ()

    _many = lambda t: "argument" + ("s" if len(t) != 1 else "")

    # copy provided args to expected, append defaults if necessary

    for i, name in enumerate(expected_args):
        if i < len(args):
            value = args[i]
        elif i >= len(expected_args) - len(default_args):
            value = argspec.defaults[i - len(expected_args) + len(default_args)]
        else:
            missing_args = expected_args[len(args):len(expected_args) - len(default_args)]
            raise FunctionArgumentsMatchException("missing required positional {0:s}: {1:s}".\
                      format(_many(missing_args), ", ".join(missing_args)))
        matched_args[name] = value

    # put extra provided args to *args if the function allows

    if argspec.varargs:
        matched_args[argspec.varargs] = args[len(expected_args):] if len(args) > len(expected_args) else ()
    elif len(args) > len(expected_args):
        raise FunctionArgumentsMatchException(
                  "takes {0:d} positional {1:s} but {2:d} {3:s} given".
                  format(len(expected_args), _many(expected_args),
                         len(args), len(args) == 1 and "was" or "were"))

    # match keyword arguments

    matched_kwargs = {}
    expected_kwargs = argspec.kwonlyargs
    default_kwargs = argspec.kwonlydefaults or {}

    # extract expected kwargs from provided, using defaults if necessary

    missing_kwargs = []
    for name in expected_kwargs:
        if name in kwargs:
            matched_kwargs[name] = kwargs[name]
        elif name in default_kwargs:
            matched_kwargs[name] = default_kwargs[name]
        else:
            missing_kwargs.append(name)
    if missing_kwargs:
        raise FunctionArgumentsMatchException("missing required keyword {0:s}: {1:s}".\
                  format(_many(missing_kwargs), ", ".join(missing_kwargs)))

    extra_kwarg_names = [ name for name in kwargs if name not in matched_kwargs ]
    if argspec.varkw:
        if extra_kwarg_names:
            extra_kwargs = { name: kwargs[name] for name in extra_kwarg_names }
        else:
            extra_kwargs = {}
        matched_args[argspec.varkw] = extra_kwargs
    elif extra_kwarg_names:
        raise FunctionArgumentsMatchException("got unexpected keyword {0:s}: {1:s}".\
                  format(_many(extra_kwarg_names), ", ".join(extra_kwarg_names)))

    # both positional and keyword argument are returned in the same scope-like dict

    for name, value in matched_kwargs.items():
        matched_args[name] = value

    return matched_args

################################################################################
# takes an argument specification for a function, from it extracts and returns
# a compiled expression which is to be matched against call arguments

def _get_guard_expr(func_name, argspec):

    guard_expr_text = None

    if "_when" in argspec.args:
        defaults = argspec.defaults or ()
        i = argspec.args.index("_when")
        if i >= len(argspec.args) - len(defaults):
            guard_expr_text = defaults[i - len(argspec.args) + len(defaults)]
    elif "_when" in argspec.kwonlyargs:
        guard_expr_text = (argspec.kwonlydefaults or {}).get("_when")
    else:
        return None # indicates default guard

    if guard_expr_text is None:
        raise GuardExpressionException("guarded function {0:s}() requires a \"_when\" "
                                       "argument with guard expression text as its "
                                       "default value".format(func_name))
    try:
        guard_expr = compile(guard_expr_text, func_name, "eval")
    except Exception as e:
        error = str(e)
    else:
        error = None
    if error is not None:
        raise GuardExpressionException("invalid guard expression for {0:s}(): "
                                       "{1:s}".format(func_name, error))

    return guard_expr

################################################################################
# checks whether two functions' argspecs are compatible to be guarded as one,
# compatible argspecs have identical positional and keyword parameters except
# for "_when" and annotations

def _compatible_argspecs(argspec1, argspec2):
    return _stripped_argspec(argspec1) == _stripped_argspec(argspec2)

def _stripped_argspec(argspec):

    args = argspec.args[:]
    defaults = list(argspec.defaults or ())
    kwonlyargs = argspec.kwonlyargs[:]
    kwonlydefaults = (argspec.kwonlydefaults or {}).copy()

    if "_when" in args:
        i = args.index("_when")
        if i >= len(args) - len(defaults):
            del defaults[i - len(args) + len(defaults)]
            del args[i]
    elif "_when" in kwonlyargs and "_when" in kwonlydefaults:
        i = kwonlyargs.index("_when")
        del kwonlyargs[i]
        del kwonlydefaults["_when"]

    return (args, defaults, kwonlyargs, kwonlydefaults, argspec.varargs, argspec.varkw)

################################################################################

def guard(func, module = None): # the main decorator function

    # see if it is a function of a lambda

    try:
        eval(func.__name__)
    except SyntaxError:
        return func # <lambda> => not guarded
    except NameError:
        pass # valid name

    # get to the bottom of a possible decorator chain
    # to get the original function's specification

    original_func = func
    while hasattr(original_func, "__wrapped__"):
        original_func = original_func.__wrapped__

    func_name = qualname(original_func)
    func_module = module or modules[func.__module__] # module serves only as a place to keep state
    argspec = getfullargspec(original_func)

    # the registry of known guarded function is attached to the module containg them

    guarded_functions = getattr(func_module, "__guarded_functions__", None)
    if guarded_functions is None:
        guarded_functions = func_module.__guarded_functions__ = {}

    original_argspec, first_guard, last_guard = guard_info = \
        guarded_functions.setdefault(func_name, [argspec, None, None])

    # all the guarded functions with the same name must have identical signature

    if argspec is not original_argspec and not _compatible_argspecs(argspec, original_argspec):
        raise IncompatibleFunctionsException("function signature is incompatible "
                    "with the previosly registered {0:s}()".format(func_name))

    @wraps(func)
    def func_guard(*args, **kwargs): # the call proxy function

        # since all versions of the function have essentially identical signatures,
        # their mapping to the actually provided arguments can be calculated once
        # for each call and not against every version of the function

        try:
            eval_args = _eval_args(argspec, args, kwargs)
        except FunctionArgumentsMatchException as e:
            error = str(e)
        else:
            error = None
        if error is not None:
            raise FunctionArgumentsMatchException("{0:s}() {1:s}".format(func_name, error))

        for name, value in guard.__default_eval_args__.items():
            eval_args.setdefault(name, value)

        # walk the chain of function versions starting with the first, looking
        # for the one for which the guard expression evaluates to truth

        current_guard = func_guard.__first_guard__
        while current_guard:
            try:
                if not current_guard.__guard_expr__ or \
                   eval(current_guard.__guard_expr__, globals(), eval_args):
                    break
            except Exception as e:
                error = str(e)
            else:
                error = None
            if error is not None:
                raise GuardEvalException("guard expression evaluation failed for "
                                         "{0:s}(): {1:s}".format(func_name, error))
            current_guard = current_guard.__next_guard__
        else:
            raise NoMatchingFunctionException("none of the guard expressions for {0:s}() "
                                              "matched the call arguments".format(func_name))

        return current_guard.__wrapped__(*args, **kwargs) # call the winning function version

    # in different version of Python @wraps behaves differently with regards
    # to __wrapped__, therefore we set it the way we need it here

    func_guard.__wrapped__ = func

    # the guard expression is attached

    func_guard.__guard_expr__ = _get_guard_expr(func_name, argspec)

    # maintain a linked list for all versions of the function

    if last_guard and not last_guard.__guard_expr__: # the list is not empty and the
                                                     # last guard is already a default
        if not func_guard.__guard_expr__:
            raise DuplicateDefaultGuardException("the default version of {0:s}() has already "
                                                 "been specified".format(func_name))

        # the new guard has to be inserted one before the last

        if first_guard is last_guard: # the list contains just one guard

            # new becomes first, last is not changed

            first_guard.__first_guard__ = func_guard.__first_guard__ = func_guard
            func_guard.__next_guard__ = first_guard
            first_guard = guard_info[1] = func_guard

        else: # the list contains more than one guard

            # neither first nor last are changed

            prev_guard = first_guard
            while prev_guard.__next_guard__ is not last_guard:
                prev_guard = prev_guard.__next_guard__

            func_guard.__first_guard__ = first_guard
            func_guard.__next_guard__ = last_guard
            prev_guard.__next_guard__ = func_guard

    else: # the new guard is inserted last

        if not first_guard:
            first_guard = guard_info[1] = func_guard
        func_guard.__first_guard__ = first_guard
        func_guard.__next_guard__ = None
        if last_guard:
            last_guard.__next_guard__ = func_guard
        last_guard = guard_info[2] = func_guard

    return func_guard

guard.__default_eval_args__ = {}
guard.default_eval_args = lambda *args, **kwargs: guard.__default_eval_args__.update(*args, **kwargs)

################################################################################
# EOF
