#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Yet another invariant/pre-/postcondition design-by-contract support module.
#
# Written by Dmitry Dvoinikov <dmitry@targeted.org>
# Distributed under MIT license.
#
# The latest version, complete with self-tests can be downloaded from:
# http://www.targeted.org/python/recipes/ipdbc.py
#
# Sample usage:
#
# import ipdbc.py
#
# class Balloon(ContractBase):             # demonstrates class invariant
#    def invariant(self):
#       return 0 <= self.weight < 1000     # returns True/False
#    def __init__(self):
#       self.weight = 0
#    def fails(self): # upon return this throws PostInvariantViolationError
#       self.weight = 1000
#
# class GuidedBalloon(Balloon):            # demonstrates pre/post condition
#    def pre_drop(self, _weight):          # pre_ receives exact copy of arguments
#       return self.weight >= _weight      # returns True/False
#    def drop(self, _weight):
#       self.weight -= _weight;
#       return self.weight                 # the result of the call is passed
#    def post_drop(self, result, _weight): # as a second parameter to post_
#       return result >= 0                 # followed again by copy of arguments
#
# Note: GuidedBalloon().fails() still fails, since Balloon's invariant is
#       inherited.
# Note: All the dbc infused methods are inherited in the mro-correct way.
# Note: Neither classmethods nor staticmethods are decorated, only "regular"
#       instance-bound methods.
#
# (c) 2005, 2006 Dmitry Dvoinikov <dmitry@targeted.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights to 
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
# of the Software, and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
#
###############################################################################

__all__ = ["ContractBase", "ContractViolationError", "InvariantViolationError",
           "PreInvariantViolationError", "PostInvariantViolationError",
           "PreConditionViolationError", "PostConditionViolationError",
           "PreconditionViolationError", "PostconditionViolationError" ]

CONTRACT_CHECKS_ENABLED = True # allows to turn contract checks off when needed

###############################################################################

class ContractViolationError(AssertionError): pass
class InvariantViolationError(ContractViolationError): pass
class PreInvariantViolationError(InvariantViolationError): pass
class PostInvariantViolationError(InvariantViolationError): pass
class PreConditionViolationError(ContractViolationError): pass
PreconditionViolationError = PreConditionViolationError # pep 316 calls it such
class PostConditionViolationError(ContractViolationError): pass
PostconditionViolationError = PostConditionViolationError # pep 316 calls it such

###############################################################################

from types import FunctionType
from sys import hexversion

have_python_24 = hexversion >= 0x2040000

################################################################################

def any(s, f = lambda e: bool(e)):
    for e in s:
        if f(e):
            return True
    else:
        return False

################################################################################

def none(s, f = lambda e: bool(e)):
    return not any(s, f)

################################################################################

def empty(s):
    return len(s) == 0

################################################################################

def pick_first(s, f = lambda e: bool(e)):
    for e in s:
        if f(e):
            return e
    else:
        return None
    
################################################################################

if not have_python_24:
    def reversed(s):
        r = list(s)
        r.reverse()
        return r

################################################################################

def merged_mro(*classes):
    """
    Returns list of all classes' bases merged and mro-correctly ordered,
    implemented as per http://www.python.org/2.3/mro.html
    """
    
    if any(classes, lambda c: not isinstance(c, type)):
        raise TypeError("merged_mro expects all it's parameters to be classes, got %s" %
                        pick_first(classes, lambda c: not isinstance(c, type)))
    
    def merge(lists):
        
        result = []
        
        lists = [ (list_[0], list_[1:]) for list_ in lists ]
        while not empty(lists):
            
            good_head, tail = pick_first(lists, lambda ht1: none(lists, lambda ht2: ht1[0] in ht2[1])) or (None, None)
            if good_head is None:
                raise TypeError("Cannot create a consistent method resolution "
                                "order (MRO) for bases %s" %
                                ", ".join([ cls.__name__ for cls in classes ]))
            result += [ good_head ]

            i = 0
            while i < len(lists):
                head, tail = lists[i]
                if head == good_head:
                    if empty(tail):
                        del(lists[i])
                    else:
                        lists[i] = ( tail[0], tail[1:] )
                        i += 1
                else:
                    i += 1
                    
        return result
        
    merged = [ cls.mro() for cls in classes ] + [ list(classes) ]
    return merge(merged)

###############################################################################

class ContractFactory(type):

    def _wrap(_method, preinvariant, precondition, postcondition, postinvariant,
              _classname, _methodname):
        
        def preinvariant_check(result):
            if not result:
                raise PreInvariantViolationError(
                    "Class invariant does not hold before a call to %s.%s"
                    % (_classname, _methodname))
        
        def precondition_check(result):
            if not result:
                raise PreConditionViolationError(
                    "Precondition failed before a call to %s.%s"
                    % (_classname, _methodname))
        
        def postcondition_check(result):
            if not result:
                raise PostConditionViolationError(
                    "Postcondition failed after a call to %s.%s"
                    % (_classname, _methodname))
        
        def postinvariant_check(result):
            if not result:
                raise PostInvariantViolationError(
                    "Class invariant does not hold after a call to %s.%s"
                    % (_classname, _methodname))
        
        if preinvariant is not None and precondition is not None \
        and postcondition is not None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is not None and precondition is not None \
        and postcondition is not None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                return result
        elif preinvariant is not None and precondition is not None \
        and postcondition is None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is not None and precondition is not None \
        and postcondition is None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                return result
        elif preinvariant is not None and precondition is None \
        and postcondition is not None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is not None and precondition is None \
        and postcondition is not None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                return result
        elif preinvariant is not None and precondition is None \
        and postcondition is None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                result = _method(self, *args, **kwargs)
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is not None and precondition is None \
        and postcondition is None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                preinvariant_check(preinvariant(self))
                result = _method(self, *args, **kwargs)
                return result
        elif preinvariant is None and precondition is not None \
        and postcondition is not None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is None and precondition is not None \
        and postcondition is not None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                return result
        elif preinvariant is None and precondition is not None \
        and postcondition is None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is None and precondition is not None \
        and postcondition is None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                precondition_check(precondition(self, *args, **kwargs))
                result = _method(self, *args, **kwargs)
                return result
        elif preinvariant is None and precondition is None \
        and postcondition is not None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is None and precondition is None \
        and postcondition is not None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                result = _method(self, *args, **kwargs)
                postcondition_check(postcondition(self, result, *args, **kwargs))
                return result
        elif preinvariant is None and precondition is None \
        and postcondition is None and postinvariant is not None:
            def dbc_wrapper(self, *args, **kwargs):
                result = _method(self, *args, **kwargs)
                postinvariant_check(postinvariant(self))
                return result
        elif preinvariant is None and precondition is None \
        and postcondition is None and postinvariant is None:
            def dbc_wrapper(self, *args, **kwargs):
                result = _method(self, *args, **kwargs)
                return result

        if have_python_24:
            dbc_wrapper.__name__ = _methodname

        return dbc_wrapper

    _wrap = staticmethod(_wrap)

    def __new__(_class, _name, _bases, _dict):

        # because the mro for the class being created is not yet available
        # we'll have to build it by hand using our own mro implementation
        
        mro = merged_mro(*_bases) # the lack of _class itself in mro is compensated ...
        dict_with_bases = {}
        for base in reversed(mro):
            if hasattr(base, "__dict__"):
                dict_with_bases.update(base.__dict__)
        dict_with_bases.update(_dict) # ... here by explicitly adding it's method last

        try:
            invariant = dict_with_bases["invariant"]
        except KeyError:
            invariant = None

        for name, target in dict_with_bases.iteritems():
            if isinstance(target, FunctionType) and name != "__del__" and name != "invariant" \
            and not name.startswith("pre_") and not name.startswith("post_"):
    
                try:
                    pre = dict_with_bases["pre_%s" % name]
                except KeyError:
                    pre = None
                
                try:
                    post = dict_with_bases["post_%s" % name]
                except KeyError:
                    post = None

                # note that __del__ is not checked at all

                _dict[name] = ContractFactory._wrap(target, 
                                                    name != "__init__" and invariant or None,
                                                    pre or None, post or None, invariant or None,
                                                    _name, name)

        return super(ContractFactory, _class).__new__(_class, _name, _bases, _dict)

class ContractBase(object):
    if CONTRACT_CHECKS_ENABLED:
        __metaclass__ = ContractFactory

###############################################################################
