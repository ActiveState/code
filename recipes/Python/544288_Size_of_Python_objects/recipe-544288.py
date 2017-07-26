The recipe below is obsolete.  Please use this one instead

<http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/546530>


#!/usr/bin/env python

 # <http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/544288>

 # Copyright, license and disclaimer are at the end of this file.

'''This module exposes function  asizeof() which calculates the
   (approximate) size of Python objects in bytes.

   The size of an object is defined as the sum of the basic size
   of the object type, the item size times the number of items
   and the size of any referenced objects.

   The basic and item sizes are obtained from the __basicsize__
   resp. __itemsize__ attributes of the type of the object.  Any
   zero item size (for sequence objects) is replaced by the size
   of the C typedef of the item.

   Referenced objects are visited recursively up to a given depth.
   The size of any objects referenced multiple times is included
   only once.

   Multi-precision int (aka long) objects and over-allocation of
   mutable sequence objects as lists are taken into account.

   The (byte)code size of objects as classes, functions, methods,
   modules, etc. can be included, optionally.

   Sizes can be aligned to a given alignment (power of 2).

   To prevent excessive sizes, several object types are ignored,
   e.g. builtins, referenced modules and function globals.  But
   module objects will be sized if passed as arguments.

   In addition, many __...__ attributes of callable objects are
   ignored, except crucial ones, e.g. class attributes __dict__,
   __doc__, __name__.  For more details, check the type-specific
   functions returning referenced objects.

   These and possibly other assumptions are rather arbitrary and
   may need corrections or adjustments.

   Tested with Python 2.2.3, 2.3.4, 2.4.3, 2.5.1 or 3.0a2 on RHEL
   3u7, CentOS 4.6, SuSE 9.3, MacOS X Tiger (Intel) and Panther
   (PPC), Solaris 10 and Windows XP.

   Function  asizeof() is not thread-safe.
'''

__version__ = '2.12 (Feb 21, 2008)'

__all__ = ['asizeof',]

from inspect import isbuiltin, isclass, iscode, isframe, isfunction, ismethod, ismodule
from math    import log
from struct  import pack
from sys     import getrecursionlimit

 # type-specific functions
def _dir(obj, prefix):
    '''Return list of matching attributes, except globals.
    '''
    g = prefix + 'globals'  # sized in modules
    return [a for a in dir(obj) if a.startswith(prefix) and a != g]

def _refs(obj, *ats):
    '''Return list of specified attribute objects.
    '''
    return [getattr(obj, a) for a in ats if hasattr(obj, a)]

def _class(obj):
    '''Class objects.
    '''
    return _refs(obj, '__class__', '__dict__', '__doc__', '__name__', '__slots__', '__weakref__')

def _code(obj):
    '''Code objects.
    '''
    return _refs(obj, *_dir(obj, 'co_'))

def _dict(obj):
    '''Dict keys and value.
    '''
    return list(obj.keys()) + list(obj.values())

def _frame(obj):
    '''Frame objects.
    '''
    return _refs(obj, *_dir(obj, 'f_'))

def _function(obj):
    '''Function or lambda objects.
    '''
    return _refs(obj, '__doc__', '__name__', *_dir(obj, 'func_'))

def _instance(obj):
    '''Class instance objects.
    '''
    return _refs(obj, '__dict__', '__slots__')

def _method(obj):
    '''Method objects.
    '''
    return _refs(obj, '__doc__', '__name__', *_dir(obj, 'im_'))

def _module(obj):
    '''Module objects.
    '''
     # essentially a dict
    return dict([(a, getattr(obj, a)) for a in dir(obj)])

def _seq(obj):
    '''Frozen/set, list, tuple and xrange objects.
    '''
    return list(obj)

def _type(obj):
    '''Type objects.
    '''
    return _refs(obj, '__mro__', '__name__')

 # sizes of some C types
_Csizeof_int      =  len(pack('i', 0))  # sizeof(int)
_Csizeof_long     =  len(pack('l', 0))  # sizeof(long)
_Csizeof_ssize    =  len(pack('P', 0))  # sizeof(ssize_t)
_Csizeof_voidp    =  len(pack('P', 0))  # sizeof(void*)
try:  # multi-precision int (or long)
   _Csizeof_digit =  long.__itemsize__
except NameError:  # no long in Python 3.0
   _Csizeof_digit =  int.__itemsize__
_Csizeof_head     = _Csizeof_voidp + _Csizeof_ssize  # sizeof(PyObject_HEAD)
_Csizeof_var_head = _Csizeof_head  + _Csizeof_ssize  # sizeof(PyObject_VAR_HEAD)

 # length functions
def _len(obj):
    '''Safe len().
    '''
    try:
        return len(obj)
    except:  # TypeError
        return 0

def _len1(obj):
    '''Length of str and unicode.
    '''
    return len(obj) + 1  # XXX sentinel

def _len8(obj):
    '''Length of mutable sequences.
    '''
    n = len(obj)
     # estimate over-allocation
    if n < 9:
        n += 4
    else:
        n += 6 + (n >> 3)
    return n

_digit2p2 = 1 << (_Csizeof_digit * 8)
_digitmax = _digit2p2 - 1  # == (2 * PyLong_MASK + 1)
_digitlog = 1.0 / log(_digit2p2)

def _ilen(obj):
    '''Length of multi-precision int (aka long) in digits.
    '''
    n, i = 1, abs(obj)
    if i > _digitmax:
         # no log(x[, base]) in Python 2.2
        n += int(log(i) * _digitlog)
    return n

# [type] = (_ref(), _len(), basicsize, itemsize)
_types_data = {}

def _types(types, t, t4):
    '''Add type to types.
    '''
    if t in types:  # and types[t] != t4
        raise KeyError('asizeof type conflict: %r %r' % (t, t4))
    types[t] = t4

def _basic(t, r, n, i):
    '''Return basicsize of type and add type.
    '''
    s = getattr(t, '__basicsize__', 0)
    _types(_types_data, t, (r, n, s, getattr(t, '__itemsize__', 0) or i))
    return s

 # basicsize of data types
_basicsize_dict     = _basic(dict,          _dict, _len8, _Csizeof_ssize + (_Csizeof_voidp * 2))  # sizeof(PyDictEntry)
_basicsize_ellipsis = _basic(type(Ellipsis), None,  None,  0)
_basicsize_float    = _basic(float,          None,  None,  0)
_basicsize_int      = _basic(int,            None, _ilen,  int.__itemsize__)  # multi-precision in Python 3.0
_basicsize_list     = _basic(list,          _seq,  _len8, _Csizeof_voidp)  # sizeof(PyObject*)
_basicsize_none     = _basic(type(None),     None,  None,  0)
_basicsize_tuple    = _basic(tuple,         _seq,  _len,  _Csizeof_voidp)  # sizeof(PyObject*)

 # newer or obsolete data types
try:
    if isbuiltin(bool):  # Python 2.2
        _basicsize_bool = int.__basicsize__  # like int
    else:  # bool is a type
        _basicsize_bool = _basic(bool, None, None, 0)
except NameError:  # missing
    _basicsize_bool = 0

try:
    _basicsize_bytes = _basic(bytes, None, _len, 1)
except NameError:  # missing
    _basicsize_bytes = 0
try:  # XXX str8 == bytes + sentinel?
    _basic(str8, None, _len1, 1)
except NameError:  # missing
    pass

try:
    _basicsize_frozenset = _basic(frozenset, _seq, _len8, (_Csizeof_voidp + _Csizeof_long))  # sizeof(setentry)
except NameError:  # missing
    _basicsize_frozenset = 0
try:
    _basicsize_set = _basic(set, _seq, _len8, (_Csizeof_voidp + _Csizeof_long))  # sizeof(setentry)
except NameError:  # missing
    _basicsize_set = 0

try:
    _basicsize_long = _basic(long, None, _ilen, 0)  # multi-precision
except NameError:  # missing
    _basicsize_long = 0

try:
    _basic(type(NotImplemented), None, None, 0)
except NameError:  # missing
    pass

try:
    _basicsize_unicode = _basic(unicode, None, _len1, 2)  # sizeof(PY_UNICODE_TYPE) 2-byte short
    _basicsize_str     = _basic(str,     None, _len1, 1)  # 1-byte char
except NameError:  # missing
    _basicsize_unicode = 0  # str is unicode
    _basicsize_str     = _basic(str, None, _len1, 2)  # XXX 2-byte char?

try:
    if isbuiltin(xrange):  # Python 2.2
        _basicsize_xrange = 0
    else:  # xrange is a type
        _basicsize_xrange = _basic(xrange, _seq, _len, _basicsize_int)
except NameError:  # missing
    _basicsize_xrange = 0

 # basicsize of code and some special types
class _C:
    pass

class _M:
    def m(self):
        pass

def _F():
    pass

_basicsize_class    =   type(_C).__basicsize__
_basicsize_function =   type(_F).__basicsize__
_basicsize_instance = type(_C()).__basicsize__
_basicsize_method   = type(_M.m).__basicsize__

_basicsize_type     = _basic(type, _type, None, 0)

_basicsize_code     = _Csizeof_head + (10 * _Csizeof_voidp) + (5 * _Csizeof_int)  # sizeof(PyCodeObject)
_basicsize_frame    = _Csizeof_var_head + (13 * _Csizeof_voidp) + (21 * 3 * _Csizeof_int)  # sizeof(PyFrameObject)
_basicsize_module   = _Csizeof_head + _Csizeof_voidp  # sizeof(PyModuleObject)

del _C, _M, _F

 # keep code and data types separate
_types_code = _types_data.copy()

try:  # sum() builtin
    _sum = sum
except NameError:  # no sum() in Python 2.2
    def _sum(vals):
        t = 0
        for v in vals:
            t += v
        return t

def _sizer(obj, deep, code, mask, types, seen):
    '''Size an object, recursively.
    '''
    s, k = 0, id(obj)
    if k in seen:  # obj seen before
        seen[k] += 1
    else:
        seen[k]  = 1
        t = type(obj)
        try:  # get _ref(), _len(), basic- and itemsize
            r, n, s, i = types[t]
        except KeyError:  # new type
            r, n, i = None, _len, 0
            if isbuiltin(obj) or ismodule(obj):
                pass  # ignore
            elif isframe(obj):
                r, s = _frame, _basicsize_frame
            elif iscode(obj):
                if code:
                    r, s = _code, _basicsize_code
            elif hasattr(obj, '__call__'):  # no callable() in Python 3.0
                if code:
                    if isclass(obj):
                        r, s = _class, _basicsize_class
                    elif isfunction(obj):
                        r, s = _function, _basicsize_function
                    elif ismethod(obj):
                        r, s = _method, _basicsize_method
                    elif isinstance(obj, type):
                        r, s = _type, _basicsize_type
            else:  # assume some class inst
                r, s = _instance, _basicsize_instance
            if s:  # adjust size
                s = max(s, getattr(t, '__basicsize__', 0))
             # add new type
            _types(types, t, (r, n, s, getattr(t, '__itemsize__', i)))
        if n and i > 0:  # items size
            s += i * n(obj)
        if mask:  # align
            s = (s + mask) & ~mask
        if r and deep > 0:  # add sizes of ref'd objs
            try:
                deep -= 1
                s += _sum([_sizer(o, deep, code, mask, types, seen) for o in r(obj)])
                seen[0] = min(deep, seen[0])  # recursion depth
            except RuntimeError:  # XXX RecursionLimitExceeded:
                pass
    return s

def _obj(obj):
    '''Handle special cases.
    '''
    if ismodule(obj):
        return _module(obj)
    return obj

def _print(fmt, *args):
     if fmt and args:
         print(fmt % args)
     else:
         print(fmt)

def _repr(obj, clip=80):
    '''Clip long repr() string.
    '''
    try:  # safe repr()
        r = repr(obj)
    except TypeError:
        r = 'N/A'
    if 0 < clip < len(r):
        h = (clip // 2) - 2
        if h > 0:
            r = r[:h] + '....' + r[-h:]
    return r

def _SI(size, K=1024):
    '''Return size as SI string.
    '''
    if 1 < K < size:
       f = float(size)
       for si in iter('KMGPTE'):
           f /= K
           if f < K:
               return ' or %.1f %sB' % (f, si)
    return ''

def _asizeof(objs, deep=100, code=False, align=8, verbose=0):
    '''Combine size one or more objects.
    '''
    if align > 1:
        m = align - 1
        if (align & m) != 0:
            raise ValueError('asizeof invalid alignment: %r' % align)
    else:
        m = 0
    if code:
        t = _types_code
    else:
        t = _types_data
    v = {0: deep}  # recursion depth
     # positional arguments
    s = _sum([_sizer(_obj(o), deep, code, m, t, v) for o in objs])

     # print some details
    if verbose > 0:
        d = deep - v[0];  del v[0]
        w = 1 + len(str(s))
         # print size and stats
        _print('asizeof(%s, verbose=%d): ...', _repr(objs), verbose)
        if code:
           _print('%*d bytes%s (incl. code)', w, s, _SI(s))
        else:
           _print('%*d bytes%s', w, s, _SI(s))
        if m:
           _print('%*d byte aligned', w, m + 1)
        _print('%*d byte sizeof(void*)', w, _Csizeof_voidp)
        _print('%*d objects sized', w, len(v))
        _print('%*d objects seen', w, _sum(v.values()))
        if d > 0:
           _print('%*d deepest recursion', w, d)
        if verbose > 1:
             # print types
            def _sorted(args):
                try:  # XXX Python 3.0
                    args.sort()
                except AttributeError:
                    pass
                return args
            _print('%*d types:  (_ref(), _len(), basicsize, itemsize)', w, len(t))
            for t in _sorted(t.items()):
               _print('%*s %r:  %r', w, '', *t)
    return s

def asizeof(*objs, **kwds):
    '''Return the total size in bytes of all objects passed as
       positional argments.

       asizeof(obj, ..., deep=100,    # recursion limit
                         code=False,  # incl. size of callables
                         align=8,     # size alignment
                         verbose=0)   # verbosity level

       Set  deep to a positive value to accumulate the sizes of
       all objects referenced by obj, recursively.  Using  deep
       zero returns the basic size of the object, incl. the size
       for the dict, frozen/set, str, list or tuple items space.

       The code size of callable objects like classes, functions,
       methods, etc. is included only if  code is True.

       Set  align to a power of 2 to align sizes.  Any value less
       than 2 avoids size alignment.

       A positive value for  verbose prints some stats like the
       number and types of objects used.
    '''
    return _asizeof(objs, **kwds)  # (deep=100, code=False, align=8, verbose=0)


if __name__ == '__main__':

    MAX = getrecursionlimit() + 4

    def _aprint(obj, deep=MAX, **kwds):
        _print(" asizeof(%s) is %d, %d, %d", _repr(obj),
                 asizeof(obj, deep=0,    code=False),
                 asizeof(obj, deep=deep, code=False, **kwds),
                 asizeof(obj, deep=deep, code=True,  **kwds))

    _print('some C sizes:')
    s = [t for t in locals().items() if t[0].startswith('_Csizeof_')]
    s.sort()
    for k, v in s:
        _print(" sizeof(%s) is %d", k[9:], v)

    _print('')
    _print('type.__basicsize__ (0 means missing type):')
    s = [t for t in locals().items() if t[0].startswith('_basicsize_')]
    s.sort()
    for k, v in s:
        _print(" %s is %d", k[11:], v)

    class C: pass

    class D:
        _attr1 = None
        _attr2 = None

    class E(D):
        def __init__(self, a1=1, a2=2):
            _attr1 = a1
            _attr2 = a2

    class S:
        __slots__ = ('a', 'b')

    class T:
        __slots__ = ('a', 'b')
        def __init__(self):
            self.a = self.b = 0

    _print('')
    _print('asizeof(%s, deep=%s, code=%s)', '<non-callable>', '0/MAX', 'False/True')
    for o in (None,
              1.0, 1.0e100, 1024, 1000000000,
              MAX, 1<<32, 1<<64, 1<<256, -(1 << 256),
              '', 'a', 'abcdefg',
              type, {}, (), [], s,
              C(), C.__dict__,
              D(), D.__dict__,
              E(), E.__dict__,
              S(), S.__dict__,
              T(), T.__dict__,
             _types_data):
        _aprint(o)

    _print('')
    _print('asizeof(%s, deep=%s, code=%s)', '<callable>', '0/MAX', 'False/True')
    for o in (C, D, E, S, T,  # classes are callable
             _code, _dict, _instance, _ilen, _seq, lambda x: x,
            (_code, _dict, _instance, _ilen, _seq)):
        _aprint(o)

    _print('')
    _print('asizeof(%s, deep=%s, code=%s)', 'locals()', 'MAX', False)
    asizeof(locals(), deep=MAX, code=False, verbose=1)

    _print('')
    _print('asizeof(%s, deep=%s, code=%s)', 'globals()', 'MAX', False)
    asizeof(globals(), deep=MAX, code=False, verbose=2)

    _print('')
    _print('asizeof(deep=%s, code=%s, *%s)', 'MAX', True, 'sys.modules.values()')
    from sys import modules
    asizeof(deep=MAX, code=True, verbose=2, *modules.values())


# License file from an earlier version of asizeof() follows:

#---------------------------------------------------------------------
#       Copyright (c) 2002-2008 -- ProphICy Semiconductor, Inc.
#                        All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# - Neither the name of ProphICy Semiconductor, Inc. nor the names
#   of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#---------------------------------------------------------------------
