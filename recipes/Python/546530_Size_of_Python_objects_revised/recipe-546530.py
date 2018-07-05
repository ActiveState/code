#!/usr/bin/env python

# Copyright, license and disclaimer are at the very end of this file.

# This is the latest, enhanced version of the asizeof.py recipes at
# <http://GitHub.com/ActiveState/code/blob/master/recipes/Python/
#         546530_Size_of_Python_objects_revised/recipe-546530.py>,
# <http://Code.ActiveState.com/recipes/546530-size-of-python-objects-revised>
# and <http://Code.ActiveState.com/recipes/544288-size-of-python-objects>.

# Recent versions of this module handle objects like ``namedtuples``,
# ``closure``, and NumPy data ``arange``, ``array``, ``matrix``, etc.
# Sizing of ``__slots__`` has been incorrect before this version.

# See also project Pympler at <http://GitHub.com/pympler/pympler> and
# memory footprint recipe <http://Code.ActiveState.com/recipes/577504/>.

# Tested with 64-bit Python 2.7.15 and 3.7.0 on macOS 10.13.5 High Sierra.
# Earlier versions of this module were tested with 32-bit Python 2.2.3,
# 2.3.7, 2.4.5, 2.5.1, 2.5.2, 2.6.2, 3.0.1 or 3.1a2 on CentOS 4.6, SuSE
# 9.3, MacOS X 10.3.9 Panther (PPC), MacOS X 10.4.11 Tiger, Solaris 10
# (Opteron) and Windows XP, with 64-bit Python 3.0.1 on RHEL 3u7 and
# Solaris 10 (Opteron) and with 64-bit Python 2.7.10 and 3.5.1 on MacOS
# X 10.11.5 El Capitan (all without numpy) and with 64-bit Python 2.6.9
# (and numpy 1.6.2), 2.7.13 (and numpy 1.13.1), 3.5.3 and 3.6.2 on macOS
# 10.12.6 Sierra, with 64-bit Intel-Python 3.5.3 (and numpy 1.11.3) on
# macOS 10.12.6 Sierra and with Pythonista 3.1 using 64-bit Python 2.7.12
# and 3.5.1 (both with numpy 1.8.0) on iOS 10.3.3.

# This module was checked statically with PyChecker 0.8.12, PyFlakes
# 1.5.0, PyCodeStyle 2.3.1 (formerly Pep8) and McCabe 0.6.1 using Python
# 2.7.13 and with Flake8 3.3.0 using Python 3.6.2, all thru this post-
# processor <http://code.activestate.com/recipes/546532/>

'''
This module exposes 9 functions and 2 classes to obtain lengths (in
items) and sizes (in bytes) of Python objects for Python 2.6 and later,
including Python 3+ [#v]_.

**Public Functions** [#unsafe]_

    Function **asizeof** calculates the combined (approximate) size
    in bytes of one or several Python objects.

    Function **asizesof** returns a tuple containing the (approximate)
    size in bytes for each given Python object separately.

    Function **asized** returns for each object an instance of class
    **Asized** containing all the size information of the object and
    a tuple with the referents [#refs]_.

    Functions **basicsize** and **itemsize** return the *basic*
    respectively *itesize* of the given object, both in bytes.  For
    objects as ``array.array``, ``numpy.array``, ``numpy.matrix``,
    etc. where the item size varies depending on the instance-specific
    data type, function **itemsize** returns that item size.

    Function **flatsize** returns the *flat size* of a Python object
    in bytes defined as the *basic size* plus the *item size* times
    the *length* of the given object.

    Function **alen** [#alen]_ returns the *length* of an object like
    standard function ``len`` but extended for several types.  E.g.
    the **alen** of a multi-precision int (or long) is the number of
    ``digits`` [#digit]_.  The *length* of most *mutable* sequence
    objects includes an estimate of the over-allocation and therefore,
    the **alen** value may differ from the standard ``len`` result.
    For objects like ``array.array``, ``numpy.array``, ``numpy.matrix``,
    etc. function **alen** returns the proper number of items.

    Function **refs** returns (a generator for) the referents [#refs]_
    of the given object.

    Certain classes are known to be sub-classes of or to behave as
    ``dict`` objects.  Function **adict** can be used to install
    other class objects to be treated like ``dict``.

**Public Classes** [#unsafe]_

    Class **Asizer** may be used to accumulate the results of several
    sizing calls.  After creating an **Asizer** instance, use methods
    **asizeof** and **asizesof** as needed to size any number of
    additional objects and accumulate the sizes.

    Call methods **exclude_refs** and/or **exclude_types** to exclude
    references to respectively instances or types of certain objects.

    Use one of the **print\_...** methods to report the statistics.

    An instance of class **Asized** is returned for each object sized
    with the **asized** function or method.

**Duplicate Objects**

    Any duplicate, given objects are sized only once and the size
    is included in the combined total only once.  But functions
    **asizesof** and **asized** will return a size value respectively
    an **Asized** instance for each given object, including duplicates.

**Definitions** [#arb]_

    The *length* of an objects like ``dict``, ``list``, ``set``,
    ``str``, ``tuple``, etc. is defined as the number of items held
    in or allocated by the object.  Held items are *references* to
    other objects, called the *referents*.

    The *size* of an object is defined as the sum of the *flat size*
    of the object plus the sizes of any referents [#refs]_.  Referents
    are visited recursively up to the specified detail level.  However,
    the size of objects referenced multiple times is included only once
    in the total *size*.

    The *flat size* of an object is defined as the *basic size* of the
    object plus the *item size* times the number of allocated *items*,
    *references* to referents.  The *flat size* does include the size
    for the *references* to the referents, but not the size of the
    referents themselves.

    The *flat size* returned by function *flatsize* equals the result
    of function *asizeof* with options *code=True*, *ignored=False*,
    *limit=0* and option *align* set to the same value.

    The accurate *flat size* for an object is obtained from function
    ``sys.getsizeof()`` where available.  Otherwise, the *length* and
    *size* of sequence objects as ``dicts``, ``lists``, ``sets``, etc.
    is based on an estimate for the number of allocated items.  As a
    result, the reported *length* and *size* may differ substantially
    from the actual *length* and *size*.

    The *basic* and *item size* are obtained from the ``__basicsize__``
    respectively ``__itemsize__`` attributes of the (type of the)
    object.  Where necessary (e.g. sequence objects), a zero
    ``__itemsize__`` is replaced by the size of a corresponding C type.

    The overhead for Python's garbage collector (GC) is included in
    the *basic size* of (GC managed) objects as well as the space
    needed for ``refcounts`` (used only in certain Python builds).

    Optionally, size values can be aligned to any power of 2 multiple.

**Size of (byte)code**

    The *(byte)code size* of objects like classes, functions, methods,
    modules, etc. can be included by setting option *code=True*.

    Iterators are handled like sequences: iterated object(s) are
    sized like *referents* [#refs]_ but only up to the specified level
    or recursion *limit* (and only if function ``gc.get_referents()``
    returns the referent object of iterators).

    Generators are sized as *(byte)code* only, but the generated objects
    are never sized.

**Old- and New-style Classes**

    All old- and new-style ``class``, instance and ``type`` objects,
    are handled uniformly such that (a) instance objects are distinguished
    from class objects and (b) instances of different old-style classes
    can be dealt with separately.

    Class and type objects are represented as ``<class ....* def>``
    respectively ``<type ... def>`` where the ``*`` indicates an old-style
    class and the ``... def`` suffix marks the *definition object*.
    Instances of  classes are shown as ``<class module.name*>`` without
    the ``... def`` suffix.  The ``*`` after the name indicates an
    instance of an old-style class.

**Ignored Objects**

    To avoid excessive sizes, several object types are ignored [#arb]_
    by default, e.g. built-in functions, built-in types and classes
    [#bi]_, function globals and module referents.  However, any
    instances thereof and module objects will be sized when passed as
    given objects.  Ignored object types are included unless option
    *ignored* is set accordingly.

    In addition, many ``__...__`` attributes of callable objects are
    ignored [#arb]_, except crucial ones, e.g. class attributes ``__dict__``,
    ``__doc__``, ``__name__`` and ``__slots__``.  For more details, see
    the type-specific ``_..._refs()`` and ``_len_...()`` functions below.

.. rubric:: Footnotes
.. [#unsafe] The functions and classes in this module are not thread-safe.

.. [#v] Earlier editions of this module supported Python versions down
    to Python 2.2.  To use Python 2.5 or older, try module ``asizeof``
    from project `Pympler 0.3.x <https://github.com/pympler/pympler>`_.

.. [#alen] Former function *leng*, class attribute *leng* and keyword
    argument *leng* have all been renamed to *alen*.  However, function
    *leng* is still available for backward compatibility.

.. [#refs] The *referents* of an object are the objects referenced *by*
    that object.  For example, the *referents* of a ``list`` are the
    objects held in the ``list``, the *referents* of a ``dict`` are
    the key and value objects in the ``dict``, etc.

.. [#arb] These definitions and other assumptions are rather arbitrary
    and may need corrections or adjustments.

.. [#digit] See Python source file ``.../Include/longinterp.h`` for the
    C ``typedef`` of ``digit`` used in multi-precision int (or long)
    objects.  The C ``sizeof(digit)`` in bytes can be obtained in
    Python from the int (or long) ``__itemsize__`` attribute.
    Function **alen** determines the number of ``digits`` of an int
    (or long) object.

.. [#bi] ``Type``s and ``class``es are considered built-in if the
    ``__module__`` of the type or class is listed in the private
    ``_builtin_modules``.
'''  # PYCHOK \_
import sys
if sys.version_info < (2, 6, 0):
    raise NotImplementedError('%s requires Python 2.6 or newer' % ('asizeof',))

from inspect import (isbuiltin, isclass, iscode, isframe, isfunction,
                     ismethod, ismodule, stack)
from math import log
from os import curdir, linesep
from struct import calcsize  # type/class Struct only in Python 2.5+
import types as Types
import warnings
import weakref as Weakref

__all__ = ['adict', 'asized', 'asizeof', 'asizesof',
           'Asized', 'Asizer',  # classes
           'basicsize', 'flatsize', 'itemsize', 'alen', 'refs']
__version__ = '18.07.04'

# any classes or types in modules listed in _builtin_modules are
# considered built-in and ignored by default, as built-in functions
if __name__ == '__main__':
    _builtin_modules = (int.__module__, 'types', Exception.__module__)  # , 'weakref'
else:  # treat this very module as built-in
    _builtin_modules = (int.__module__, 'types', Exception.__module__, __name__)  # , 'weakref'

# sizes of some primitive C types
# XXX len(pack(T, 0)) == Struct(T).size == calcsize(T)
_sizeof_Cbyte = calcsize('c')  # sizeof(unsigned char)
_sizeof_Clong = calcsize('l')  # sizeof(long)
_sizeof_Cvoidp = calcsize('P')  # sizeof(void*)

# sizeof(long) != sizeof(ssize_t) on LLP64
if _sizeof_Clong < _sizeof_Cvoidp:  # pragma: no coverage
    _z_P_L = 'P'
else:
    _z_P_L = 'L'


def _calcsize(fmt):
    '''Like struct.calcsize() but handling 'z' for Py_ssize_t.
    '''
    return calcsize(fmt.replace('z', _z_P_L))


# defaults for some basic sizes with 'z' for C Py_ssize_t
_sizeof_CPyCodeObject = _calcsize('Pz10P5i0P')  # sizeof(PyCodeObject)
_sizeof_CPyFrameObject = _calcsize('Pzz13P63i0P')  # sizeof(PyFrameObject)
_sizeof_CPyModuleObject = _calcsize('PzP0P')  # sizeof(PyModuleObject)

# defaults for some item sizes with 'z' for C Py_ssize_t
_sizeof_CPyDictEntry = _calcsize('z2P')  # sizeof(PyDictEntry)
_sizeof_Csetentry = _calcsize('lP')  # sizeof(setentry)

try:  # C typedef digit for multi-precision int (or long)
    _sizeof_Cdigit = long.__itemsize__
except NameError:  # no long in Python 3.0
    _sizeof_Cdigit = int.__itemsize__
if _sizeof_Cdigit < 2:  # pragma: no coverage
    raise AssertionError('sizeof(%s) bad: %d' % ('digit', _sizeof_Cdigit))

# Get character size for internal unicode representation in Python < 3.3
try:  # sizeof(unicode_char)
    u = unicode('\0')
except NameError:  # no unicode() in Python 3.0
    u = '\0'
u = u.encode('unicode-internal')  # see .../Lib/test/test_sys.py
_sizeof_Cunicode = len(u)
del u

try:  # size of GC header, sizeof(PyGC_Head)
    import _testcapi as t
    _sizeof_CPyGC_Head = t.SIZEOF_PYGC_HEAD  # new in Python 2.6
except (ImportError, AttributeError):  # sizeof(PyGC_Head)
    # alignment should be to sizeof(long double) but there
    # is no way to obtain that value, assume twice double
    t = calcsize('2d') - 1
    _sizeof_CPyGC_Head = (_calcsize('2Pz') + t) & ~t
del t

# size of refcounts (Python debug build only)
if hasattr(sys, 'gettotalrefcount'):  # pragma: no coverage
    _sizeof_Crefcounts = _calcsize('2z')
else:
    _sizeof_Crefcounts = 0

try:
    from abc import ABCMeta
except ImportError:
    class ABCMeta(type):
        pass

# some flags from .../Include/object.h
_Py_TPFLAGS_HEAPTYPE = 1 << 9  # Py_TPFLAGS_HEAPTYPE
_Py_TPFLAGS_HAVE_GC = 1 << 14  # Py_TPFLAGS_HAVE_GC

_Type_type = type(type)  # == type and new-style class type


# compatibility functions for more uniform
# behavior across Python version 2.2 thu 3.0

def _items(obj):  # dict only
    '''Return iter-/generator, preferably.
    '''
    return getattr(obj, 'iteritems', obj.items)()


def _keys(obj):  # dict only
    '''Return iter-/generator, preferably.
    '''
    return getattr(obj, 'iterkeys', obj.keys)()


def _values(obj):  # dict only
    '''Return iter-/generator, preferably.
    '''
    return getattr(obj, 'itervalues', obj.values)()


try:  # callable() builtin
    _iscallable = callable
except NameError:  # callable() removed in Python 3.0
    def _iscallable(obj):
        '''Substitute for callable().'''
        return hasattr(obj, '__call__')

# 'cell' is holding data used in closures
c = (lambda unused: (lambda: unused))(None)
try:
    _cell_type = type(c.__closure__[0])
except AttributeError:  # Python 2.5
    _cell_type = type(c.func_closure[0])
del c

try:
    from gc import get_objects as _getobjects  # containers only?
except ImportError:
    def _getobjects():
        # modules first, globals and stack
        # objects (may contain duplicates)
        return tuple(_values(sys.modules)) + (
               globals(), stack(sys.getrecursionlimit())[2:])

try:  # only used to get referents of
    # iterators, but gc.get_referents()
    # returns () for dict...-iterators
    from gc import get_referents as _getreferents
except ImportError:
    def _getreferents(unused):
        return ()  # sorry, no refs

# sys.getsizeof() new in Python 2.6, adjusted below
_getsizeof = getattr(sys, 'getsizeof', None)

try:  # str intern()
    _intern = intern
except NameError:  # no intern() in Python 3.0
    def _intern(val):
        return val


# private functions

def _basicsize(t, base=0, heap=False, obj=None):
    '''Get non-zero basicsize of type,
       including the header sizes.
    '''
    s = max(getattr(t, '__basicsize__', 0), base)
    # include gc header size
    if t != _Type_type:
        h = getattr(t, '__flags__', 0) & _Py_TPFLAGS_HAVE_GC
    elif heap:  # type, allocated on heap
        h = True
    else:  # None has no __flags__ attr
        h = getattr(obj, '__flags__', 0) & _Py_TPFLAGS_HEAPTYPE
    if h:
        s += _sizeof_CPyGC_Head
    # include reference counters
    return s + _sizeof_Crefcounts


def _c100(stats):
    '''Cutoff as percentage.
    '''
    return int((stats - int(stats)) * 100.0 + 0.5)


def _classof(obj, dflt=None):
    '''Return the object's class object.
    '''
    return getattr(obj, '__class__', dflt)


def _derive_typedef(typ):
    '''Return single, existing super type typedef or None.
    '''
    v = [v for v in _values(_typedefs) if _issubclass(typ, v.type)]
    if len(v) == 1:
        return v[0]
    return None


def _dir2(obj, pref='', excl=(), slots=None, itor=''):
    '''Return an attribute name, object 2-tuple for certain
       attributes or for the ``__slots__`` attributes of the
       given object, but not both.  Any iterator referent
       objects are returned with the given name if the
       latter is non-empty.
    '''
    if slots:  # __slots__ attrs
        if hasattr(obj, slots):
            # collect all inherited __slots__ attrs
            # from list, tuple, or dict __slots__,
            # while removing any duplicate attrs
            s = {}
            for c in type(obj).mro():
                for a in getattr(c, slots, ()):
                    if a.startswith('__'):
                        a = '_' + c.__name__ + a
                    if hasattr(obj, a):
                        s.setdefault(a, getattr(obj, a))
            #  assume a __slots__ tuple is holding the values
            # yield slots, _Slots(s)  # _keys(s) ... REMOVED,
            #  see _Slots.__doc__ further below
            for t in _items(s):
                yield t  # attr name, value
    elif itor:  # iterator referents
        for o in obj:  # iter(obj)
            yield itor, o
    else:  # regular attrs
        for a in dir(obj):
            if a.startswith(pref) and hasattr(obj, a) and a not in excl:
                yield a, getattr(obj, a)


def _infer_dict(obj):
    '''Return True for likely dict object via duck typing.
    '''
    for ats in (('__len__', 'get', 'has_key', 'items', 'keys', 'update', 'values'),
                ('__len__', 'get', 'has_key', 'iteritems', 'iterkeys', 'itervalues')):
        if all(_iscallable(getattr(obj, a, None)) for a in ats):
            return True
    return False


def _iscell(obj):
    '''Return True if obj is a cell as used in a closure.
    '''
    return isinstance(obj, _cell_type)


def _isdictclass(obj):
    '''Return True for known dict objects.
    '''
    c = _classof(obj)
    return c and c.__name__ in _dict_classes.get(c.__module__, ())


def _isframe(obj):
    '''Return True for a stack frame object.
    '''
    try:  # safe isframe(), see pympler.muppy
        return isframe(obj)
    except ReferenceError:
        return False


def _isnamedtuple(obj):
    '''Named tuples are identified via duck typing:
       <http://www.gossamer-threads.com/lists/python/dev/1142178>
    '''
    return isinstance(obj, tuple) and hasattr(obj, '_fields')


def _isNULL(obj):
    '''Prevent asizeof(all=True, ...) crash.

       Sizing gc.get_objects() crashes in Pythonista3 with
       Python 3.5.1 on iOS due to 1-tuple (<Null>,) object.
    '''
    return isinstance(obj, tuple) and len(obj) == 1 \
                                  and repr(obj) == '(<NULL>,)'


def _isnumpy(obj):
    '''Return True for a NumPy arange, array, matrix, etc. instance.
    '''
    if _numpy_types:  # see also _len_numpy
        return isinstance(obj, _numpy_types) or \
             (_moduleof(_classof(obj)).startswith('numpy') and
               hasattr(obj, 'nbytes'))
    return False


def _issubclass(sub, sup):
    '''Safe issubclass().
    '''
    if sup is not object:
        try:
            return issubclass(sub, sup)
        except TypeError:
            pass
    return False


def _itemsize(t, item=0):
    '''Get non-zero itemsize of type.
    '''
    # replace zero value with default
    return getattr(t, '__itemsize__', 0) or item


def _kwdstr(**kwds):
    '''Keyword arguments as a string.
    '''
    return ', '.join(sorted('%s=%r' % kv for kv in _items(kwds)))


def _lengstr(obj):
    '''Object length as a string.
    '''
    n = alen(obj)
    if n is None:  # no len
        r = ''
    elif n > _len(obj):  # extended
        r = ' alen %d!' % n
    else:
        r = ' alen %d' % n
    return r


def _moduleof(obj, dflt=''):
    '''Return the object's module name.
    '''
    return getattr(obj, '__module__', dflt)


def _nameof(obj, dflt=''):
    '''Return the name of an object.
    '''
    return getattr(obj, '__name__', dflt)


def _objs_opts(objs, all=None, **opts):
    '''Return given or 'all' objects
       and the remaining options.
    '''
    if objs:  # given objects
        t = objs
    elif all in (False, None):
        t = ()
    elif all is True:  # 'all' objects
        t = tuple(_getobjects())
        if sys.platform == 'ios':
            # remove any tuples containing NULLs
            t = tuple(o for o in t if not _isNULL(o))
    else:
        raise ValueError('invalid option: %s=%r' % ('all', all))
    return t, opts


def _p100(part, total, prec=1):
    '''Return percentage as string.
    '''
    r = float(total)
    if r:
        r = part * 100.0 / r
        return '%.*f%%' % (prec, r)
    return 'n/a'


def _plural(num):
    '''Return 's' if plural.
    '''
    if num == 1:
        s = ''
    else:
        s = 's'
    return s


def _power2(n):
    '''Finds the next power of 2.
    '''
    p2 = 16
    while n > p2:
        p2 += p2
    return p2


def _prepr(obj, clip=0):
    '''Prettify and clip long repr() string.
    '''
    return _repr(obj, clip=clip).strip('<>').replace("'", '')  # remove <''>


def _printf(fmt, *args, **print3opts):
    '''Formatted print to sys.stdout or given stream.

        *print3opts* -- print keyword arguments, like Python 3.+
    '''
    if print3opts:  # like Python 3.0
        f = print3opts.get('file', None) or sys.stdout
        if args:
            f.write(fmt % args)
        else:
            f.write(fmt)
        f.write(print3opts.get('end', linesep))
        if print3opts.get('flush', False):
            f.flush()
    elif args:
        print(fmt % args)
    else:
        print(fmt)


def _refs(obj, named, *attrs, **kwds):
    '''Return specific attribute objects of an object.
    '''
    if named:
        _N = _NamedRef
    else:
        def _N(_, o):
            return o

    for a in attrs:  # cf. inspect.getmembers()
        if hasattr(obj, a):
            yield _N(a, getattr(obj, a))
    if kwds:  # kwds are _dir2() args
        for a, o in _dir2(obj, **kwds):
            yield _N(a, o)


def _repr(obj, clip=80):
    '''Clips long repr() string.
    '''
    try:  # safe repr()
        r = repr(obj)
    except Exception:
        r = 'N/A'
    if 0 < clip < len(r):
        h = (clip // 2) - 2
        if h > 0:
            r = r[:h] + '....' + r[-h:]
    return r


def _SI(size, K=1024, i='i'):
    '''Return size as SI string.
    '''
    if 1 < K < size:
        f = float(size)
        for si in iter('KMGPTE'):
            f /= K
            if f < K:
                return ' or %.1f %s%sB' % (f, si, i)
    return ''


def _SI2(size, **kwds):
    '''Return size as regular plus SI string.
    '''
    return str(size) + _SI(size, **kwds)


# type-specific referents functions

def _cell_refs(obj, named):
    return _refs(obj, named, 'cell_contents')


def _class_refs(obj, named):
    '''Return specific referents of a class object.
    '''
    return _refs(obj, named, '__class__', '__doc__', '__mro__',
                             '__name__', '__slots__', '__weakref__',
                             '__dict__')  # __dict__ last


def _co_refs(obj, named):
    '''Return specific referents of a code object.
    '''
    return _refs(obj, named, pref='co_')


def _dict_refs(obj, named):
    '''Return key and value objects of a dict/proxy.
    '''
    try:
        if named:
            for k, v in _items(obj):
                s = str(k)
                yield _NamedRef('[K] ' + s, k)
                yield _NamedRef('[V] ' + s + ': ' + _repr(v), v)
        else:
            for k, v in _items(obj):
                yield k
                yield v
    except ReferenceError:
        warnings.warn("Reference error iterating '%s'" % (_classof(obj),))


def _enum_refs(obj, named):
    '''Return specific referents of an enumerate object.
    '''
    return _refs(obj, named, '__doc__')


def _exc_refs(obj, named):
    '''Return specific referents of an Exception object.
    '''
    # .message raises DeprecationWarning in Python 2.6
    return _refs(obj, named, 'args', 'filename', 'lineno', 'msg', 'text')  # , 'message', 'mixed'


def _file_refs(obj, named):
    '''Return specific referents of a file object.
    '''
    return _refs(obj, named, 'mode', 'name')


def _frame_refs(obj, named):
    '''Return specific referents of a frame object.
    '''
    return _refs(obj, named, pref='f_')


def _func_refs(obj, named):
    '''Return specific referents of a function or lambda object.
    '''
    return _refs(obj, named, '__doc__', '__name__', '__code__', '__closure__',
                 pref='func_', excl=('func_globals',))


def _gen_refs(obj, named):
    '''Return the referent(s) of a generator object.
    '''
    # only some gi_frame attrs
    f = getattr(obj, 'gi_frame', None)
    return _refs(f, named, 'f_locals', 'f_code')


def _im_refs(obj, named):
    '''Return specific referents of a method object.
    '''
    return _refs(obj, named, '__doc__', '__name__', '__code__', pref='im_')


def _inst_refs(obj, named):
    '''Return specific referents of a class instance.
    '''
    return _refs(obj, named, '__dict__', '__class__', slots='__slots__')


def _iter_refs(obj, named):
    '''Return the referent(s) of an iterator object.
    '''
    r = _getreferents(obj)  # special case
    return _refs(r, named, itor=_nameof(obj) or 'iteref')


def _module_refs(obj, named):
    '''Return specific referents of a module object.
    '''
    # ignore this very module
    if obj.__name__ == __name__:
        return ()
    # module is essentially a dict
    return _dict_refs(obj.__dict__, named)


def _namedtuple_refs(obj, named):
    '''Return specific referents of obj-as-sequence and slots but exclude dict.
    '''
    for r in _refs(obj, named, '__class__', slots='__slots__'):
        yield r
    for r in obj:
        yield r


def _prop_refs(obj, named):
    '''Return specific referents of a property object.
    '''
    return _refs(obj, named, '__doc__', pref='f')


def _seq_refs(obj, unused):  # named unused for PyChecker
    '''Return specific referents of a frozen/set, list, tuple and xrange object.
    '''
    return obj  # XXX for r in obj: yield r


def _stat_refs(obj, named):
    '''Return referents of a os.stat object.
    '''
    return _refs(obj, named, pref='st_')


def _statvfs_refs(obj, named):
    '''Return referents of a os.statvfs object.
    '''
    return _refs(obj, named, pref='f_')


def _tb_refs(obj, named):
    '''Return specific referents of a traceback object.
    '''
    return _refs(obj, named, pref='tb_')


def _type_refs(obj, named):
    '''Return specific referents of a type object.
    '''
    return _refs(obj, named, '__dict__', '__doc__', '__mro__',
                             '__name__', '__slots__', '__weakref__')


def _weak_refs(obj, unused):  # named unused for PyChecker
    '''Return weakly referent object.
    '''
    try:  # ignore 'key' of KeyedRef
        return (obj(),)
    except Exception:  # XXX ReferenceError
        return ()


_all_refs = (None, _cell_refs, _class_refs, _co_refs, _dict_refs, _enum_refs,
             _exc_refs, _file_refs, _frame_refs, _func_refs, _gen_refs,
             _im_refs, _inst_refs, _iter_refs, _module_refs, _namedtuple_refs,
             _prop_refs, _seq_refs, _stat_refs, _statvfs_refs, _tb_refs,
             _type_refs, _weak_refs)


# type-specific length functions

def _len(obj):
    '''Safe len().
    '''
    try:
        return len(obj)
    except TypeError:  # no len()
        return 0


def _len_array(obj):
    '''Array length (in bytes!).
    '''
    return len(obj) * obj.itemsize


def _len_bytearray(obj):
    '''Bytearray size.
    '''
    return obj.__alloc__()


def _len_code(obj):  # see .../Lib/test/test_sys.py
    '''Length of code object (stack and variables only).
    '''
    return (obj.co_stacksize + obj.co_nlocals +
           _len(obj.co_freevars) + _len(obj.co_cellvars) - 1)


def _len_dict(obj):
    '''Dict length in items (estimate).
    '''
    n = len(obj)  # active items
    if n < 6:  # ma_smalltable ...
        n = 0  # ... in basicsize
    else:  # at least one unused
        n = _power2(n + 1)
    return n


def _len_frame(obj):
    '''Length of a frame object.
    '''
    c = getattr(obj, 'f_code', None)
    if c:
        n = _len_code(c)
    else:
        n = 0
    return n


_digit2p2 = 1 << (_sizeof_Cdigit << 3)
_digitmax = _digit2p2 - 1  # == (2 * PyLong_MASK + 1)
_digitlog = 1.0 / log(_digit2p2)


def _len_int(obj):
    '''Length of multi-precision int (aka long) in digits.
    '''
    if obj:
        n, i = 1, abs(obj)
        if i > _digitmax:
            # no log(x[, base]) in Python 2.2
            n += int(log(i) * _digitlog)
    else:  # zero
        n = 0
    return n


def _len_iter(obj):
    '''Length (hint) of an iterator.
    '''
    n = getattr(obj, '__length_hint__', None)
    if n:
        n = n()
    else:  # try len()
        n = _len(obj)
    return n


def _len_list(obj):
    '''Length of list (estimate).
    '''
    n = len(obj)
    # estimate over-allocation
    if n > 8:
        n += 6 + (n >> 3)
    elif n:
        n += 4
    return n


def _len_module(obj):
    '''Module length.
    '''
    return _len(obj.__dict__)  # _len(dir(obj))


def _len_numpy(obj):
    '''NumPy array, matrix, etc. length (in bytes!).
    '''
    return obj.nbytes  # == obj.size * obj.itemsize


def _len_set(obj):
    '''Length of frozen/set (estimate).
    '''
    n = len(obj)
    if n > 8:  # assume half filled
        n = _power2(n + n - 2)
    elif n:  # at least 8
        n = 8
    return n


def _len_slice(obj):
    '''Slice length.
    '''
    try:
        return ((obj.stop - obj.start + 1) // obj.step)
    except (AttributeError, TypeError):
        return 0


# REMOVED, see _Slots.__doc__
# def _len_slots(obj):
#     '''Slots length.
#     '''
#     return len(obj) - 1


def _len_struct(obj):
    '''Struct length in bytes.
    '''
    try:
        return obj.size
    except AttributeError:
        return 0


def _len_unicode(obj):
    '''Unicode size.
    '''
    return len(obj) + 1


_all_lens = (None, _len, _len_array, _len_bytearray, _len_code,
                   _len_dict, _len_frame, _len_int, _len_iter,
                   _len_list, _len_module, _len_numpy, _len_set,
                   _len_slice, _len_struct, _len_unicode)  # _len_slots

# more private functions and classes

_old_style = '*'  # marker
_new_style = ''   # no marker


class _Claskey(object):
    '''Wrapper for class objects.
    '''
    __slots__ = ('_obj', '_sty')

    def __init__(self, obj, style):
        self._obj = obj  # XXX Weakref.ref(obj)
        self._sty = style

    def __str__(self):
        r = str(self._obj)
        if r.endswith('>'):
            r = '%s%s def>' % (r[:-1], self._sty)
        elif self._sty is _old_style and not r.startswith('class '):
            r = 'class %s%s def' % (r, self._sty)
        else:
            r = '%s%s def' % (r, self._sty)
        return r
    __repr__ = __str__


# For most objects, the object type is used as the key in the
# _typedefs dict further below, except class and type objects
# and old-style instances.  Those are wrapped with separate
# _Claskey or _Instkey instances to be able (1) to distinguish
# instances of different old-style classes by class, (2) to
# distinguish class (and type) instances from class (and type)
# definitions for new-style classes and (3) provide similar
# results for repr() and str() of new- and old-style classes
# and instances.

_claskeys = {}  # [id(obj)] = _Claskey()


def _claskey(obj, style):
    '''Wraps an old- or new-style class object.
    '''
    i = id(obj)
    k = _claskeys.get(i, None)
    if not k:
        _claskeys[i] = k = _Claskey(obj, style)
    return k


try:  # MCCABE 19
    # no Class- and InstanceType in Python 3.0
    _Types_ClassType = Types.ClassType
    _Types_InstanceType = Types.InstanceType

    class _Instkey(object):
        '''Wrapper for old-style class (instances).
        '''
        __slots__ = ('_obj',)

        def __init__(self, obj):
            self._obj = obj  # XXX Weakref.ref(obj)

        def __str__(self):
            t = _moduleof(self._obj), self._obj.__name__, _old_style
            return '<class %s.%s%s>' % t
        __repr__ = __str__

    _instkeys = {}  # [id(obj)] = _Instkey()

    def _instkey(obj):
        '''Wraps an old-style class (instance).
        '''
        i = id(obj)
        k = _instkeys.get(i, None)
        if not k:
            _instkeys[i] = k = _Instkey(obj)
        return k

    def _keytuple(obj):
        '''Return class and instance keys for a class.
        '''
        t = type(obj)
        if t is _Types_InstanceType:
            t = obj.__class__
            return _claskey(t, _old_style), _instkey(t)
        elif t is _Types_ClassType:
            return _claskey(obj, _old_style), _instkey(obj)
        elif t is _Type_type:
            return _claskey(obj, _new_style), obj
        return None, None  # not a class

    def _objkey(obj):
        '''Return the key for any object.
        '''
        k = type(obj)
        if k is _Types_InstanceType:
            k = _instkey(obj.__class__)
        elif k is _Types_ClassType:
            k = _claskey(obj, _old_style)
        elif k is _Type_type:
            k = _claskey(obj, _new_style)
        return k

except AttributeError:  # Python 3.0

    def _keytuple(obj):  # PYCHOK expected
        '''Return class and instance keys for a class.
        '''
        if type(obj) is _Type_type:  # isclass(obj):
            return _claskey(obj, _new_style), obj
        return None, None  # not a class

    def _objkey(obj):  # PYCHOK expected
        '''Return the key for any object.
        '''
        k = type(obj)
        if k is _Type_type:  # isclass(obj):
            k = _claskey(obj, _new_style)
        return k


class _NamedRef(object):
    '''Store referred object along
       with the name of the referent.
    '''
    __slots__ = ('name', 'ref')

    def __init__(self, name, ref):
        self.name = name
        self.ref = ref


# class _Slots(tuple):
#     '''Wrapper class for __slots__ attribute at class definition.
#        The instance-specific __slots__ attributes are stored in
#        a "tuple-like" space inside the instance, see Luciano
#        Ramalho, "Fluent Python", page 274+, O'Reilly, 2016 or
#        at <http://Books.Google.com/books>, then search for
#        "Fluent Python" "Space Savings with the __slots__".
#     '''
#     pass


# kinds of _Typedefs
_i = _intern
_all_kinds = (_kind_static, _kind_dynamic, _kind_derived, _kind_ignored, _kind_inferred) = (
                _i('static'), _i('dynamic'), _i('derived'), _i('ignored'), _i('inferred'))
del _i

_Not_vari = ''  # non-variable item size


class _Typedef(object):
    '''Type definition class.
    '''
    __slots__ = {
        'base': 0,     # basic size in bytes
        'item': 0,     # item size in bytes
        'alen': None,  # or _len_...() function
        'refs': None,  # or _..._refs() function
        'both': None,  # both data and code if True, code only if False
        'kind': None,  # _kind_... value
        'type': None,  # original type
        'vari': None}  # item size attr name or _Not_vari

    def __init__(self, **kwds):
        self.reset(**kwds)

    def __lt__(self, unused):  # for Python 3.0
        return True

    def __repr__(self):
        return repr(self.args())

    def __str__(self):
        t = [str(self.base), str(self.item)]
        for f in (self.alen, self.refs):
            if f:
                t.append(f.__name__)
            else:
                t.append('n/a')
        if not self.both:
            t.append('(code only)')
        return ', '.join(t)

    def args(self):  # as args tuple
        '''Return all attributes as arguments tuple.
        '''
        return (self.base, self.item, self.alen, self.refs,
                self.both, self.kind, self.type)

    def dup(self, other=None, **kwds):
        '''Duplicate attributes of dict or other typedef.
        '''
        if other is None:
            d = _dict_typedef.kwds()
        else:
            d = other.kwds()
        d.update(kwds)
        self.reset(**d)

    def flat(self, obj, mask=0):
        '''Return the aligned flat size.
        '''
        s = self.base
        if self.alen and self.item > 0:  # include items
            s += self.alen(obj) * self.item
        if _getsizeof:  # _getsizeof prevails
            s = _getsizeof(obj, s)
        if mask:  # align
            s = (s + mask) & ~mask
        return s

    def format(self):
        '''Return format dict.
        '''
        i = self.item
        if self.vari:
            i = 'var'
        c = n = ''
        if not self.both:
            c = ' (code only)'
        if self.alen:
            n = ' (%s)' % _nameof(self.alen)
        return dict(base=self.base, item=i, alen=n, code=c,
                    kind=self.kind)

    def kwds(self):
        '''Return all attributes as keywords dict.
        '''
        return dict(base=self.base, item=self.item,
                    alen=self.alen, refs=self.refs,
                    both=self.both, kind=self.kind,
                    type=self.type, vari=self.vari)

    def save(self, t, base=0, heap=False):
        '''Saves this typedef plus its class typedef.
        '''
        c, k = _keytuple(t)
        if k and k not in _typedefs:  # instance key
            _typedefs[k] = self
            if c and c not in _typedefs:  # class key
                if t.__module__ in _builtin_modules:
                    k = _kind_ignored  # default
                else:
                    k = self.kind
                _typedefs[c] = _Typedef(base=_basicsize(type(t), base=base, heap=heap),
                                        refs=_type_refs,
                                        both=False, kind=k, type=t)
        elif isbuiltin(t) and t not in _typedefs:  # array, range, xrange in Python 2.x
            _typedefs[t] = _Typedef(base=_basicsize(t, base=base),
                                    both=False, kind=_kind_ignored, type=t)
        else:
            raise KeyError('asizeof typedef %r bad: %r %r' % (self, (c, k), self.both))

    def set(self, safe_len=False, **kwds):
        '''Sets one or more attributes.
        '''
        if kwds:  # double check
            d = self.kwds()
            d.update(kwds)
            self.reset(**d)
        if safe_len and self.item:
            self.alen = _len

    def reset(self, base=0, item=0, alen=None, refs=None,
                    both=True, kind=None, type=None, vari=_Not_vari):
        '''Resets all specified attributes.
        '''
        if base < 0:
            raise ValueError('invalid option: %s=%r' % ('base', base))
        else:
            self.base = base
        if item < 0:
            raise ValueError('invalid option: %s=%r' % ('item', item))
        else:
            self.item = item
        if alen in _all_lens:  # XXX or _iscallable(alen)
            self.alen = alen
        else:
            raise ValueError('invalid option: %s=%r' % ('alen', alen))
        if refs in _all_refs:  # XXX or _iscallable(refs)
            self.refs = refs
        else:
            raise ValueError('invalid option: %s=%r' % ('refs', refs))
        if both in (False, True):
            self.both = both
        else:
            raise ValueError('invalid option: %s=%r' % ('both', both))
        if kind in _all_kinds:
            self.kind = kind
        else:
            raise ValueError('invalid option: %s=%r' % ('kind', kind))
        self.type = type
        self.vari = vari or _Not_vari
        if str(self.vari) != self.vari:
            raise ValueError('invalid option: %s=%r' % ('vari', vari))


_typedefs = {}  # [key] = _Typedef()


def _typedef_both(t, base=0, item=0, alen=None, refs=None,
                     kind=_kind_static, heap=False, vari=_Not_vari):
    '''Adds new typedef for both data and code.
    '''
    v = _Typedef(base=_basicsize(t, base=base), item=_itemsize(t, item),
                 refs=refs, alen=alen,
                 both=True, kind=kind, type=t, vari=vari)
    v.save(t, base=base, heap=heap)
    return v  # for _dict_typedef


def _typedef_code(t, base=0, refs=None, kind=_kind_static, heap=False):
    '''Adds new typedef for code only.
    '''
    v = _Typedef(base=_basicsize(t, base=base),
                 refs=refs,
                 both=False, kind=kind, type=t)
    v.save(t, base=base, heap=heap)
    return v  # for _dict_typedef


# static typedefs for data and code types
_typedef_both(complex)
_typedef_both(float)
_typedef_both(list, refs=_seq_refs, alen=_len_list, item=_sizeof_Cvoidp)  # sizeof(PyObject*)
_typedef_both(tuple, refs=_seq_refs, alen=_len, item=_sizeof_Cvoidp)  # sizeof(PyObject*)
_typedef_both(property, refs=_prop_refs)
_typedef_both(type(Ellipsis))
_typedef_both(type(None))

# _Slots are "tuple-like", REMOVED see _Slots.__doc__
# _typedef_both(_Slots, item=_sizeof_Cvoidp,
#               leng=_len_slots,  # length less one
#               refs=None,  # but no referents
#               heap=True)  # plus head

# dict, dictproxy, dict_proxy and other dict-like types
_dict_typedef = _typedef_both(dict, item=_sizeof_CPyDictEntry, alen=_len_dict, refs=_dict_refs)
try:  # <type dictproxy> only in Python 2.x
    _typedef_both(Types.DictProxyType, item=_sizeof_CPyDictEntry, alen=_len_dict, refs=_dict_refs)
except AttributeError:  # XXX any class __dict__ is <type dict_proxy> in Python 3.0?
    _typedef_both(type(_Typedef.__dict__), item=_sizeof_CPyDictEntry, alen=_len_dict, refs=_dict_refs)
# other dict-like classes and types may be derived or inferred,
# provided the module and class name is listed here (see functions
# adict, _isdictclass and _infer_dict for further details)
_dict_classes = {'UserDict': ('IterableUserDict', 'UserDict'),
                 'weakref': ('WeakKeyDictionary', 'WeakValueDictionary')}
try:  # <type module> is essentially a dict
    _typedef_both(Types.ModuleType, base=_dict_typedef.base,
                  item=_dict_typedef.item + _sizeof_CPyModuleObject,
                  alen=_len_module, refs=_module_refs)
except AttributeError:  # missing
    pass

_getsizeof_excls = ()  # to adjust _getsizeof


def _getsizeof_excls_add(typ):
    global _getsizeof_excls
    if typ not in _getsizeof_excls:
        _getsizeof_excls += (typ,)


# newer or obsolete types
try:
    from array import array  # array type

    def _array_kwds(obj):
        if hasattr(obj, 'itemsize'):
            v = 'itemsize'
        else:
            v = _Not_vari
        # since item size varies by the array data type, set
        # itemsize to 1 byte and use _len_array in bytes; note,
        # function itemsize returns the actual size in bytes
        # and function alen returns the length in number of items
        return dict(alen=_len_array, item=_sizeof_Cbyte, vari=v)

    _typedef_both(array, **_array_kwds(array('d', [])))

    v = sys.version_info
    _array_excl = (v[0] == 2 and v < (2, 7, 4)) or \
                  (v[0] == 3 and v < (3, 2, 4))
    if _array_excl:  # see function _typedef below
        _getsizeof_excls_add(array)

    del v
except ImportError:  # missing
    _array_excl = array = None  # see function _typedef below

try:  # bool has non-zero __itemsize__ in 3.0
    _typedef_both(bool)
except NameError:  # missing
    pass

try:  # ignore basestring
    _typedef_both(basestring, alen=None)
except NameError:  # missing
    pass

try:
    if isbuiltin(buffer):  # Python 2.2
        _typedef_both(type(buffer('')), item=_sizeof_Cbyte, alen=_len)  # XXX len in bytes?
    else:
        _typedef_both(buffer, item=_sizeof_Cbyte, alen=_len)  # XXX len in bytes?
except NameError:  # missing
    pass

try:
    _typedef_both(bytearray, item=_sizeof_Cbyte, alen=_len_bytearray)
except NameError:  # bytearray new in 2.6, 3.0
    pass
try:
    if type(bytes) is not type(str):  # bytes is str in 2.6, bytes new in 2.6, 3.0
        _typedef_both(bytes, item=_sizeof_Cbyte, alen=_len)  # bytes new in 2.6, 3.0
except NameError:  # missing
    pass
try:  # XXX like bytes
    _typedef_both(str8, item=_sizeof_Cbyte, alen=_len)  # PYCHOK str8 new in 2.6, 3.0
except NameError:  # missing
    pass

try:
    _typedef_both(enumerate, refs=_enum_refs)
except NameError:  # missing
    pass

try:  # Exception is type in Python 3.0
    _typedef_both(Exception, refs=_exc_refs)
except Exception:  # missing
    pass

try:
    _typedef_both(file, refs=_file_refs)
except NameError:  # missing
    pass

try:
    _typedef_both(frozenset, item=_sizeof_Csetentry, alen=_len_set, refs=_seq_refs)
except NameError:  # missing
    pass
try:
    _typedef_both(set, item=_sizeof_Csetentry, alen=_len_set, refs=_seq_refs)
except NameError:  # missing
    pass

try:  # not callable()
    _typedef_both(Types.GetSetDescriptorType)
except AttributeError:  # missing
    pass

try:  # if long exists, it is multi-precision ...
    _typedef_both(long, item=_sizeof_Cdigit, alen=_len_int)
    _typedef_both(int)  # ... and int is fixed size
except NameError:  # no long, only multi-precision int in Python 3.0
    _typedef_both(int, item=_sizeof_Cdigit, alen=_len_int)

try:  # not callable()
    _typedef_both(Types.MemberDescriptorType)
except AttributeError:  # missing
    pass

try:
    _typedef_both(type(NotImplemented))  # == Types.NotImplementedType
except NameError:  # missing
    pass

_numpy_types = ()
try:
    import numpy  # NumPy array, matrix, etc.

    def _numpy_kwds(obj):
        if _getsizeof:
            b = _getsizeof(obj, 96) - obj.nbytes
        else:
            b = 96  # 96..144 typical __basicsize__?
        # since item size depends on the nympy data type, set
        # itemsize to 1 byte and use _len_numpy in bytes; note,
        # function itemsize returns the actual size in bytes,
        # function alen returns the length in number of items
        return dict(base=b, item=_sizeof_Cbyte,  # not obj.itemsize
                            alen=_len_numpy,
                            vari='itemsize')

    for d in (numpy.array(range(0)), numpy.arange(0),
              numpy.matrix(range(0)), numpy.ma.masked_array([])):
        t = type(d)
        if t not in _numpy_types:
            _numpy_types += (t,)
            if _isnumpy(d):  # double check
                _typedef_both(t, **_numpy_kwds(d))
            else:
                raise AssertionError('not %s: %r' % ('numpy', d))

    # sizing numpy 1.13 arrays works fine, but 1.8 and older
    # appears to suffer from sys.getsizeof() bug like array
    v = tuple(map(int, numpy.__version__.split('.')))
    _numpy_excl = v < (1, 9, 0)
    if _numpy_excl:  # see function _typedef below
        for t in _numpy_types:
            _getsizeof_excls_add(t)

    del numpy, d, t, v
except ImportError:
    _numpy_excl = False  # see function _typedef below

try:
    _typedef_both(range)
except NameError:  # missing
    pass
try:
    _typedef_both(xrange)
except NameError:  # missing
    pass

try:
    _typedef_both(reversed, refs=_enum_refs)
except NameError:  # missing
    pass

try:
    _typedef_both(slice, item=_sizeof_Cvoidp, alen=_len_slice)  # XXX worst-case itemsize?
except NameError:  # missing
    pass

try:
    from os import stat
    _typedef_both(type(stat(curdir)), refs=_stat_refs)  # stat_result
except ImportError:  # missing
    pass

try:
    from os import statvfs
    _typedef_both(type(statvfs(curdir)), refs=_statvfs_refs,  # statvfs_result
                  item=_sizeof_Cvoidp, alen=_len)
except ImportError:  # missing
    pass

try:
    from struct import Struct  # only in Python 2.5 and 3.0
    _typedef_both(Struct, item=_sizeof_Cbyte, alen=_len_struct)  # len in bytes
except ImportError:  # missing
    pass

try:
    _typedef_both(Types.TracebackType, refs=_tb_refs)
except AttributeError:  # missing
    pass

try:
    _typedef_both(unicode, alen=_len_unicode, item=_sizeof_Cunicode)
    _typedef_both(str, alen=_len, item=_sizeof_Cbyte)  # 1-byte char
except NameError:  # str is unicode
    _typedef_both(str, alen=_len_unicode, item=_sizeof_Cunicode)

try:  # <type 'KeyedRef'>
    _typedef_both(Weakref.KeyedRef, refs=_weak_refs, heap=True)  # plus head
except AttributeError:  # missing
    pass

try:  # <type 'weakproxy'>
    _typedef_both(Weakref.ProxyType)
except AttributeError:  # missing
    pass

try:  # <type 'weakref'>
    _typedef_both(Weakref.ReferenceType, refs=_weak_refs)
except AttributeError:  # missing
    pass

# some other, callable types
_typedef_code(object, kind=_kind_ignored)
_typedef_code(super, kind=_kind_ignored)
_typedef_code(_Type_type, kind=_kind_ignored)

try:
    _typedef_code(classmethod, refs=_im_refs)
except NameError:
    pass
try:
    _typedef_code(staticmethod, refs=_im_refs)
except NameError:
    pass
try:
    _typedef_code(Types.MethodType, refs=_im_refs)
except NameError:
    pass

try:  # generator, code only, no len(), not callable()
    _typedef_code(Types.GeneratorType, refs=_gen_refs)
except AttributeError:  # missing
    pass

try:  # <type 'weakcallableproxy'>
    _typedef_code(Weakref.CallableProxyType, refs=_weak_refs)
except AttributeError:  # missing
    pass

# any type-specific iterators
s = [_items({}), _keys({}), _values({})]
try:  # reversed list and tuples iterators
    s.extend([reversed([]), reversed(())])
except NameError:  # missing
    pass

try:  # range iterator
    s.append(xrange(1))
except NameError:  # missing
    pass

try:  # callable-iterator
    from re import finditer
    s.append(finditer('', ''))
except ImportError:  # missing
    pass

for t in _values(_typedefs):
    if t.type and t.alen:
        try:  # create an (empty) instance
            s.append(t.type())
        except TypeError:
            pass
for t in s:
    try:
        i = iter(t)
        _typedef_both(type(i), alen=_len_iter, refs=_iter_refs, item=0)  # no itemsize!
    except (KeyError, TypeError):  # ignore non-iterables, duplicates, etc.
        pass
del i, s, t


if _getsizeof_excls and _getsizeof:
    # workaround the sys.getsizeof (and numpy?) bug
    def _wraps(sys_sizeof):
        def _getsizeof_wrap(obj, *default):
            if isinstance(obj, _getsizeof_excls):
                try:
                    return default[0]
                except IndexError:
                    raise TypeError('no default')
            else:
                return sys_sizeof(obj, *default)
        return _getsizeof_wrap

    _getsizeof = _wraps(_getsizeof)
    del _wraps


def _typedef(obj, derive=False, infer=False):  # MCCABE 24
    '''Creates a new typedef for an object.
    '''
    t = type(obj)
    v = _Typedef(base=_basicsize(t, obj=obj),
                 kind=_kind_dynamic, type=t)
#   _printf('new %r %r/%r %s', t, _basicsize(t), _itemsize(t), _repr(dir(obj)))
    if ismodule(obj):  # handle module like dict
        v.dup(item=_dict_typedef.item + _sizeof_CPyModuleObject,
              alen=_len_module,
              refs=_module_refs)
    elif _isframe(obj):
        v.set(base=_basicsize(t, base=_sizeof_CPyFrameObject, obj=obj),
              item=_itemsize(t),
              alen=_len_frame,
              refs=_frame_refs)
    elif iscode(obj):
        v.set(base=_basicsize(t, base=_sizeof_CPyCodeObject, obj=obj),
              item=_sizeof_Cvoidp,
              alen=_len_code,
              refs=_co_refs,
              both=False)  # code only
    elif _iscallable(obj):
        if isclass(obj):  # class or type
            v.set(refs=_class_refs,
                  both=False)  # code only
            if _moduleof(obj) in _builtin_modules:
                v.set(kind=_kind_ignored)
        elif isbuiltin(obj):  # function or method
            v.set(both=False,  # code only
                  kind=_kind_ignored)
        elif isfunction(obj):
            v.set(refs=_func_refs,
                  both=False)  # code only
        elif ismethod(obj):
            v.set(refs=_im_refs,
                  both=False)  # code only
        elif isclass(t):  # callable instance, e.g. SCons,
            # handle like any other instance further below
            v.set(item=_itemsize(t), safe_len=True,
                  refs=_inst_refs)  # not code only!
        else:
            v.set(both=False)  # code only
    elif _issubclass(t, dict):
        v.dup(kind=_kind_derived)
    elif _isdictclass(obj) or (infer and _infer_dict(obj)):
        v.dup(kind=_kind_inferred)
    elif _iscell(obj):
        v.set(item=_itemsize(t), refs=_cell_refs)
    elif _isnamedtuple(obj):
        v.set(refs=_namedtuple_refs)
    elif _isnumpy(obj):  # NumPy data
        v.set(**_numpy_kwds(obj))
        if _numpy_excl:
            _getsizeof_excls_add(t)
    elif array and isinstance(obj, array):
        v.set(**_array_kwds(obj))
        if _array_excl:
            _getsizeof_excls_add(t)
    elif _moduleof(obj) in _builtin_modules:
        v.set(kind=_kind_ignored)
    else:  # assume an instance of some class
        if derive:
            p = _derive_typedef(t)
            if p:  # duplicate parent
                v.dup(other=p, kind=_kind_derived)
                return v
        if _issubclass(t, Exception):
            v.set(item=_itemsize(t), safe_len=True,
                  refs=_exc_refs,
                  kind=_kind_derived)
        elif isinstance(obj, Exception):
            v.set(item=_itemsize(t), safe_len=True,
                  refs=_exc_refs)
        else:
            v.set(item=_itemsize(t), safe_len=True,
                  refs=_inst_refs)
    return v


class _Prof(object):
    '''Internal type profile class.
    '''
    total = 0      # total size
    high = 0       # largest size
    number = 0     # number of (unique) objects
    objref = None  # largest object (weakref)
    weak = False   # objref is weakref(object)

    def __cmp__(self, other):
        if self.total < other.total:
            return -1
        if self.total > other.total:
            return +1
        if self.number < other.number:
            return -1
        if self.number > other.number:
            return +1
        return 0

    def __lt__(self, other):  # for Python 3.0
        return self.__cmp__(other) < 0

    def format(self, clip=0, grand=None):
        '''Return format dict.
        '''
        if self.number > 1:  # avg., plural
            a, p = int(self.total / self.number), 's'
        else:
            a, p = self.total, ''
        o = self.objref
        if self.weak:  # weakref'd
            o = o()
        t = _SI2(self.total)
        if grand:
            t += ' (%s)' % _p100(self.total, grand, prec=0)
        return dict(avg=_SI2(a), high=_SI2(self.high),
                    lengstr=_lengstr(o), obj=_repr(o, clip=clip),
                    plural=p, total=t)

    def update(self, obj, size):
        '''Updates this profile.
        '''
        self.number += 1
        self.total += size
        if self.high < size:  # largest
            self.high = size
            try:  # prefer using weak ref
                self.objref, self.weak = Weakref.ref(obj), True
            except TypeError:
                self.objref, self.weak = obj, False


# public classes

class Asized(object):
    '''Stores the results of an **asized** object in the following
    4 attributes:

        *size* -- total size of the object (including referents)

        *flat* -- flat size of the object

        *name* -- name or ``repr`` of the object

        *refs* -- tuple containing an **Asized** instance for each referent
    '''
    __slots__ = ('flat', 'name', 'refs', 'size')

    def __init__(self, size, flat, refs=(), name=None):
        self.size = size  # total size
        self.flat = flat  # flat size
        self.name = name  # name, repr or None
        self.refs = tuple(refs)

    def __str__(self):
        return 'size %r, flat %r, refs[%d], name %r' % (
            self.size, self.flat, len(self.refs), self.name)

    def format(self, format='%(name)s size=%(size)d flat=%(flat)d',
                     detail=-1, order_by='size', indent=''):
        '''Formats the size information of the object and of all sized
        referents as a string.

            *format='%(name)s...'* -- specifies the format string per
            instance, valid interpolation parameters are 'name', 'size'
            and 'flat'

            *detail=-1* -- detail level up to which referents are
            printed (-1 for unlimited)

            *order_by='size'* -- sort order of referents, valid choices
            are 'name', 'size' or 'flat'

            *indent=''* -- optional indentation
        '''
        lines = [indent + (format % dict(size=self.size, flat=self.flat,
                                         name=self.name))]
        if detail and self.refs:
            refs = sorted(self.refs, key=lambda x: getattr(x, order_by),
                                     reverse=order_by in ('size', 'flat'))
            lines += [ref.format(format=format, detail=detail-1, order_by=order_by,
                                 indent=indent+'    ') for ref in refs]
        return '\n'.join(lines)

    def get(self, name, dflt=None):
        '''Return the named referent (or *dflt* if not found).
        '''
        for ref in self.refs:
            if name == ref.name:
                return ref
        return dflt


class Asizer(object):
    '''State and options to accumulate sizes.
    '''
    _align_ = 8
    _clip_ = 80
    _code_ = False
    _derive_ = False
    _detail_ = 0  # for Asized only
    _infer_ = False
    _limit_ = 100
    _stats_ = 0

    _cutoff = 0  # in percent
    _depth = 0  # deepest recursion
    _duplicate = 0
    _excl_d = None  # {}
    _ign_d = _kind_ignored
    _incl = ''  # or ' (incl. code)'
    _mask = 7   # see _align_
    _missed = 0   # due to errors
    _profile = False
    _profs = None  # {}
    _seen = None  # {}
    _total = 0   # total size

    _stream = None  # IO stream for printing

    def __init__(self, **opts):
        '''New **Asizer** accumulator.

        See this module documentation for more details.  See method
        **reset** for all available options and defaults.
        '''
        self._excl_d = {}
        self.reset(**opts)

    def _printf(self, fmt, *args, **print3opts):
        '''Prints to sys.stdout or the configured stream if any is
        specified and if the file keyword argument is not already
        set in the **print3opts for this specific call.
        '''
        if self._stream and not print3opts.get('file', None):
            if args:
                fmt = fmt % args
            _printf(fmt, file=self._stream, **print3opts)
        else:
            _printf(fmt, *args, **print3opts)

    def _clear(self):
        '''Clears state.
        '''
        self._depth = 0   # recursion depth reached
        self._duplicate = 0
        self._incl = ''  # or ' (incl. code)'
        self._missed = 0   # due to errors
        self._profile = False
        self._profs = {}
        self._seen = {}
        self._total = 0   # total size
        for k in _keys(self._excl_d):
            self._excl_d[k] = 0

    def _nameof(self, obj):
        '''Return the object's name.
        '''
        return _nameof(obj, '') or self._repr(obj)

    def _prepr(self, obj):
        '''Like **prepr()**.
        '''
        return _prepr(obj, clip=self._clip_)

    def _prof(self, key):
        '''Get _Prof object.
        '''
        p = self._profs.get(key, None)
        if not p:
            self._profs[key] = p = _Prof()
        return p

    def _repr(self, obj):
        '''Like ``repr()``.
        '''
        return _repr(obj, clip=self._clip_)

    def _sizer(self, obj, deep, sized):  # MCCABE 16
        '''Sizes an object, recursively.
        '''
        s, f, i = 0, 0, id(obj)
        # skip obj if seen before
        # or if ref of a given obj
        if i in self._seen:
            if deep:
                self._seen[i] += 1
                if sized:
                    s = sized(s, f, name=self._nameof(obj))
                return s
        else:
            self._seen[i] = 0
        try:
            k, rs = _objkey(obj), []
            if k in self._excl_d:
                self._excl_d[k] += 1
            else:
                v = _typedefs.get(k, None)
                if not v:  # new typedef
                    _typedefs[k] = v = _typedef(obj, derive=self._derive_,
                                                infer=self._infer_)
                if (v.both or self._code_) and v.kind is not self._ign_d:
                    s = f = v.flat(obj, self._mask)  # flat size
                    if self._profile:  # profile type
                        self._prof(k).update(obj, s)
                    # recurse, but not for nested modules
                    if v.refs and deep < self._limit_ \
                              and not (deep and ismodule(obj)):
                        # add sizes of referents
                        r, z, d = v.refs, self._sizer, deep + 1
                        if sized and deep < self._detail_:
                            # use named referents
                            for o in r(obj, True):
                                if isinstance(o, _NamedRef):
                                    t = z(o.ref, d, sized)
                                    t.name = o.name  # PYCHOK _sizer
                                else:
                                    t = z(o, d, sized)
                                    t.name = self._nameof(o)
                                rs.append(t)
                                s += t.size  # PYCHOK _sizer
                        else:  # no sum(<generator_expression>) in Python 2.2
                            s += sum(z(o, d, None) for o in r(obj, False))
                        # recursion depth reached
                        if self._depth < d:
                            self._depth = d
            self._seen[i] += 1
        except RuntimeError:  # XXX RecursionLimitExceeded:
            self._missed += 1
        if sized:
            s = sized(s, f, name=self._nameof(obj), refs=rs)
        return s

    def _sizes(self, objs, sized=None):
        '''Return the size or an **Asized** instance for each given
        object and the total size.  The total includes the size of
        any duplicates only once.
        '''
        self.exclude_refs(*objs)  # skip refs to objs
        s, t = {}, []
        for o in objs:
            i = id(o)
            if i in s:  # duplicate
                self._seen[i] += 1
                self._duplicate += 1
            else:
                s[i] = self._sizer(o, 0, sized)
            t.append(s[i])
        if sized:
            s = sum(i.size for i in _values(s))
        else:
            s = sum(_values(s))
        self._total += s  # accumulate
        return s, tuple(t)

    def asized(self, *objs, **opts):
        '''Sizes each object and returns an **Asized** instance with
        size information and *referents* up to the given detail level
        (and with modified options, see method **set**).

        If only one object is given, the return value is the **Asized**
        instance for that object.
        '''
        if opts:
            self.set(**opts)
        _, t = self._sizes(objs, Asized)
        if len(t) == 1:
            t = t[0]
        return t

    def asizeof(self, *objs, **opts):
        '''Return the combined size of the given objects (with modified
        options, see method **set**).
        '''
        if opts:
            self.set(**opts)
        s, _ = self._sizes(objs, None)
        return s

    def asizesof(self, *objs, **opts):
        '''Return the individual sizes of the given objects (with
        modified options, see method  **set**).
        '''
        if opts:
            self.set(**opts)
        _, t = self._sizes(objs, None)
        return t

    def _get_duplicate(self):
        '''Number of duplicate objects seen so far.
        '''
        return self._duplicate
    duplicate = property(_get_duplicate, doc=_get_duplicate.__doc__)

    def exclude_refs(self, *objs):
        '''Excludes any references to the specified objects from sizing.

        While any references to the given objects are excluded, the
        objects will be sized if specified as positional arguments in
        subsequent calls to methods **asizeof** and **asizesof**.
        '''
        for o in objs:
            self._seen.setdefault(id(o), 0)

    def exclude_types(self, *objs):
        '''Exclude the specified object instances and types from sizing.

        All instances and types of the given objects are excluded, even
        objects specified as positional arguments in subsequent calls
        to methods **asizeof** and **asizesof**.
        '''
        for o in objs:
            for t in _keytuple(o):
                if t and t not in self._excl_d:
                    self._excl_d[t] = 0

    def _get_missed(self):
        '''Number of objects missed due to errors.
        '''
        return self._missed
    missed = property(_get_missed, doc=_get_missed.__doc__)

    def print_profiles(self, w=0, cutoff=0, **print3opts):
        '''Prints the profiles above *cutoff* percentage.

        The available options and defaults are:

            *w=0* -- indentation for each line

            *cutoff=0* -- minimum percentage printed

            *print3opts* -- print keyword arguments, like Python 3.+
        '''
        # get the profiles with non-zero size or count
        t = [(v, k) for k, v in _items(self._profs) if v.total > 0 or v.number > 1]
        if (len(self._profs) - len(t)) < 9:  # just show all
            t = [(v, k) for k, v in _items(self._profs)]
        if t:
            s = ''
            if self._total:
                s = ' (% of grand total)'
                c = max(cutoff, self._cutoff)
                c = int(c * 0.01 * self._total)
            else:
                c = 0
            self._printf('%s%*d profile%s:  total%s, average, and largest flat size%s:  largest object',
                         linesep, w, len(t), _plural(len(t)), s, self._incl, **print3opts)
            r = len(t)
            for v, k in sorted(t, reverse=True):
                s = 'object%(plural)s:  %(total)s, %(avg)s, %(high)s:  %(obj)s%(lengstr)s' % v.format(self._clip_, self._total)
                self._printf('%*d %s %s', w, v.number, self._prepr(k), s, **print3opts)
                r -= 1
                if r > 1 and v.total < c:
                    c = max(cutoff, self._cutoff)
                    self._printf('%+*d profiles below cutoff (%.0f%%)', w, r, c)
                    break
            z = len(self._profs) - len(t)
            if z > 0:
                self._printf('%+*d %r object%s', w, z, 'zero', _plural(z), **print3opts)

    def print_stats(self, objs=(), opts={}, sized=(), sizes=(), stats=3.0, **print3opts):
        '''Prints the statistics.

        The available options and defaults are:

            *w=0* -- indentation for each line

            *objs=()* -- optional, list of objects

            *opts={}* -- optional, dict of options used

            *sized=()* -- optional, tuple of **Asized** instances returned

            *sizes=()* -- optional, tuple of sizes returned

            *stats=0.0* -- print stats, see function **asizeof**

            *print3opts* -- print keyword arguments, like Python 3.+
        '''
        s = min(opts.get('stats', stats) or 0, self._stats_)
        if s > 0:  # print stats
            t = self._total + self._missed + sum(_values(self._seen))
            w = len(str(t)) + 1
            t = c = ''
            o = _kwdstr(**opts)
            if o and objs:
                c = ', '
            # print header line(s)
            if sized and objs:
                n = len(objs)
                if n > 1:
                    self._printf('%sasized(...%s%s) ...', linesep, c, o, **print3opts)
                    for i in range(n):  # no enumerate in Python 2.2.3
                        self._printf('%*d: %s', w - 1, i, sized[i], **print3opts)
                else:
                    self._printf('%sasized(%s): %s', linesep, o, sized, **print3opts)
            elif sizes and objs:
                self._printf('%sasizesof(...%s%s) ...', linesep, c, o, **print3opts)
                for z, o in zip(sizes, objs):
                    self._printf('%*d bytes%s%s:  %s', w, z, _SI(z), self._incl, self._repr(o), **print3opts)
            else:
                if objs:
                    t = self._repr(objs)
                self._printf('%sasizeof(%s%s%s) ...', linesep, t, c, o, **print3opts)
            # print summary
            self.print_summary(w=w, objs=objs, **print3opts)
            if s > 1:  # print profile
                self.print_profiles(w=w, cutoff=_c100(s), **print3opts)
                if s > 2:  # print typedefs
                    self.print_typedefs(w=w, **print3opts)

    def print_summary(self, w=0, objs=(), **print3opts):
        '''Prints the summary statistics.

        The available options and defaults are:

            *w=0* -- indentation for each line

            *objs=()* -- optional, list of objects

            *print3opts* -- print keyword arguments, like Python 3.+
        '''
        self._printf('%*d bytes%s%s', w, self._total, _SI(self._total), self._incl, **print3opts)
        if self._mask:
            self._printf('%*d byte aligned', w, self._mask + 1, **print3opts)
        self._printf('%*d byte sizeof(void*)', w, _sizeof_Cvoidp, **print3opts)
        n = len(objs or ())
        if n > 0:
            d = self._duplicate or ''
            if d:
                d = ', %d duplicate' % self._duplicate
            self._printf('%*d object%s given%s', w, n, _plural(n), d, **print3opts)
        t = sum(1 for t in _values(self._seen) if t != 0)
        self._printf('%*d object%s sized', w, t, _plural(t), **print3opts)
        if self._excl_d:
            t = sum(_values(self._excl_d))
            self._printf('%*d object%s excluded', w, t, _plural(t), **print3opts)
        t = sum(_values(self._seen))
        self._printf('%*d object%s seen', w, t, _plural(t), **print3opts)
        if self._missed > 0:
            self._printf('%*d object%s missed', w, self._missed, _plural(self._missed), **print3opts)
        if self._depth > 0:
            self._printf('%*d deepest recursion', w, self._depth, **print3opts)

    def print_typedefs(self, w=0, **print3opts):
        '''Prints the types and dict tables.

        The available options and defaults are:

            *w=0* -- indentation for each line

            *print3opts* -- print keyword arguments, like Python 3.+
        '''
        for k in _all_kinds:
            # XXX Python 3.0 doesn't sort type objects
            t = [(self._prepr(a), v) for a, v in _items(_typedefs) if v.kind == k and (v.both or self._code_)]
            if t:
                self._printf('%s%*d %s type%s:  basicsize, itemsize, _len_(), _refs()',
                             linesep, w, len(t), k, _plural(len(t)), **print3opts)
                for a, v in sorted(t):
                    self._printf('%*s %s:  %s', w, '', a, v, **print3opts)
        # dict and dict-like classes
        t = sum(len(v) for v in _values(_dict_classes))
        if t:
            self._printf('%s%*d dict/-like classes:', linesep, w, t, **print3opts)
            for m, v in _items(_dict_classes):
                self._printf('%*s %s:  %s', w, '', m, self._prepr(v), **print3opts)

    def _get_total(self):
        '''Total size (in bytes) accumulated so far.
        '''
        return self._total
    total = property(_get_total, doc=_get_total.__doc__)

    def reset(self, align=8, clip=80, code=False, derive=False,  # PYCHOK too many args
              detail=0, ignored=True, infer=False, limit=100, stats=0,
              stream=None):
        '''Resets the options, state, etc.

        The available options and defaults are:

            *align=8* -- size alignment

            *clip=80* -- clip repr() strings

            *code=False* -- incl. (byte)code size

            *derive=False* -- derive from super type

            *detail=0* -- **Asized** refs level

            *ignored=True* -- ignore certain types

            *infer=False* -- try to infer types

            *limit=100* -- recursion limit

            *stats=0.0* -- print statistics, see function **asizeof**

            *stream=None* -- output stream for printing

        See function **asizeof** for a description of the options.
        '''
        # options
        self._align_ = align
        self._clip_ = clip
        self._code_ = code
        self._derive_ = derive
        self._detail_ = detail  # for Asized only
        self._infer_ = infer
        self._limit_ = limit
        self._stats_ = stats
        self._stream = stream
        if ignored:
            self._ign_d = _kind_ignored
        else:
            self._ign_d = None
        # clear state
        self._clear()
        self.set(align=align, code=code, stats=stats)

    def set(self, align=None, code=None, detail=None, limit=None, stats=None):
        '''Sets some options.  See also method **reset**.

        Any options not set remain unchanged from the previous setting.
        The available options are:

            *align* -- size alignment

            *code* -- incl. (byte)code size

            *detail* -- **Asized** refs level

            *limit* -- recursion limit

            *stats* -- print statistics, see function **asizeof**
        '''
        # adjust
        if align is not None:
            self._align_ = align
            if align > 1:
                self._mask = align - 1
                if (self._mask & align) != 0:
                    raise ValueError('invalid option: %s=%r' % ('align', align))
            else:
                self._mask = 0
        if code is not None:
            self._code_ = code
            if code:  # incl. (byte)code
                self._incl = ' (incl. code)'
        if detail is not None:
            self._detail_ = detail
        if limit is not None:
            self._limit_ = limit
        if stats is not None:
            if stats < 0:
                raise ValueError('invalid option: %s=%r' % ('stats', stats))
            self._stats_ = s = int(stats)
            self._cutoff = _c100(stats)
            if s > 1:  # profile types
                self._profile = True
            else:
                self._profile = False


# public functions

def adict(*classes):
    '''Installs one or more classes to be handled as dict.
    '''
    a = True
    for c in classes:
        # if class is dict-like, add class
        # name to _dict_classes[module]
        if isclass(c) and _infer_dict(c):
            t = _dict_classes.get(c.__module__, ())
            if c.__name__ not in t:  # extend tuple
                _dict_classes[c.__module__] = t + (c.__name__,)
        else:  # not a dict-like class
            a = False
    return a  # all installed if True


_asizer = Asizer()


def asized(*objs, **opts):
    '''Return a tuple containing an **Asized** instance for each
    object passed as positional argument.

    The available options and defaults are:

        *align=8* -- size alignment

        *clip=80* -- clip repr() strings

        *code=False* -- incl. (byte)code size

        *derive=False* -- derive from super type

        *detail=0* -- **Asized** refs level

        *ignored=True* -- ignore certain types

        *infer=False* -- try to infer types

        *limit=100* -- recursion limit

        *stats=0.0* -- print statistics, see function **asizeof**

    If only one object is given, the return value is the **Asized**
    instance for that object.  Otherwise, the length of the returned
    tuple matches the number of given objects.

    Set *detail* to the desired referents level and *limit* to the
    maximum recursion depth.

    See function **asizeof** for descriptions of the other options.
    '''
    if 'all' in opts:
        raise KeyError('invalid option: %s=%r' % ('all', opts['all']))
    if objs:
        _asizer.reset(**opts)
        t = _asizer.asized(*objs)
        _asizer.print_stats(objs, opts=opts, sized=t)  # show opts as _kwdstr
        _asizer._clear()
    else:
        t = ()
    return t


def asizeof(*objs, **opts):
    '''Return the combined size (in bytes) of all objects passed
    as positional arguments.

    The available options and defaults are:

        *align=8* -- size alignment

        *all=False* -- all current objects

        *clip=80* -- clip ``repr()`` strings

        *code=False* -- incl. (byte)code size

        *derive=False* -- derive from super type

        *ignored=True* -- ignore certain types

        *infer=False* -- try to infer types

        *limit=100* -- recursion limit

        *stats=0.0* -- print statistics

    Set *align* to a power of 2 to align sizes.  Any value less
    than 2 avoids size alignment.

    If *all* is True and if no positional arguments are supplied.
    size all current gc objects, including module, global and stack
    frame objects.

    A positive *clip* value truncates all repr() strings to at
    most *clip* characters.

    The (byte)code size of callable objects like functions,
    methods, classes, etc. is included only if *code* is True.

    If *derive* is True, new types are handled like an existing
    (super) type provided there is one and only of those.

    By default certain base types like object, super, etc. are
    ignored.  Set *ignored* to False to include those.

    If *infer* is True, new types are inferred from attributes
    (only implemented for dict types on callable attributes
    as get, has_key, items, keys and values).

    Set *limit* to a positive value to accumulate the sizes of
    the referents of each object, recursively up to the limit.
    Using *limit=0* returns the sum of the flat[4] sizes of
    the given objects.  High *limit* values may cause runtime
    errors and miss objects for sizing.

    A positive value for *stats* prints up to 8 statistics, (1)
    a summary of the number of objects sized and seen, (2) a
    simple profile of the sized objects by type and (3+) up to
    6 tables showing the static, dynamic, derived, ignored,
    inferred and dict types used, found respectively installed.
    The fractional part of the *stats* value (x 100) is the
    cutoff percentage for simple profiles.

    See this module documentation for the definition of flat size.
    '''
    t, p = _objs_opts(objs, **opts)
    if t:
        _asizer.reset(**p)
        s = _asizer.asizeof(*t)
        _asizer.print_stats(objs=t, opts=opts)  # show opts as _kwdstr
        _asizer._clear()
    else:
        s = 0
    return s


def asizesof(*objs, **opts):
    '''Return a tuple containing the size (in bytes) of all objects
    passed as positional argments.

    The available options and defaults are:

        *align=8* -- size alignment

        *clip=80* -- clip ``repr()`` strings

        *code=False* -- incl. (byte)code size

        *derive=False* -- derive from super type

        *ignored=True* -- ignore certain types

        *infer=False* -- try to infer types

        *limit=100* -- recursion limit

        *stats=0.0* -- print statistics

    See function **asizeof** for a description of the options.

    The length of the returned tuple equals the number of given objects.
    '''
    if 'all' in opts:
        raise KeyError('invalid option: %s=%r' % ('all', opts['all']))
    if objs:  # size given objects
        _asizer.reset(**opts)
        t = _asizer.asizesof(*objs)
        _asizer.print_stats(objs, opts=opts, sizes=t)  # show opts as _kwdstr
        _asizer._clear()
    else:
        t = ()
    return t


def _typedefof(obj, save=False, **opts):
    '''Get the typedef for an object.
    '''
    k = _objkey(obj)
    v = _typedefs.get(k, None)
    if not v:  # new typedef
        v = _typedef(obj, **opts)
        if save:
            _typedefs[k] = v
    return v


def alen(obj, **opts):
    '''Return the length of an object (in *items*).

    See function **basicsize** for a description of the options.
    '''
    n = t = _typedefof(obj, **opts)
    if t:
        n = t.alen
        if n and _iscallable(n):
            i, v, n = t.item, t.vari, n(obj)
            if v and i == _sizeof_Cbyte:
                i = getattr(obj, v, i)
                if i > _sizeof_Cbyte:
                    n = n // i
    return n


leng = alen  # for backward comptibility


def basicsize(obj, **opts):
    '''Return the basic size of an object (in bytes).

    The available options and defaults are:

        *derive=False* -- derive type from super type

        *infer=False* -- try to infer types

        *save=False* -- save the type definition if new
    '''
    b = _typedefof(obj, **opts)
    if b:
        b = b.base
    return b


def flatsize(obj, align=0, **opts):
    '''Return the flat size of an object (in bytes), optionally aligned
    to a given power of 2.

    See function **basicsize** for a description of all other options.

    See this module documentation for the definition of *flat size*.
    '''
    v = _typedefof(obj, **opts)
    if v:
        if align > 1:
            m = align - 1
            if (align & m) != 0:
                raise ValueError('invalid option: %s=%r' % ('align', align))
        else:
            m = 0
        v = v.flat(obj, mask=m)
    return v


def itemsize(obj, **opts):
    '''Return the item size of an object (in bytes).

    See function **basicsize** for a description of the options.
    '''
    i = t = _typedefof(obj, **opts)
    if t:
        i, v = t.item, t.vari
        if v and i == _sizeof_Cbyte:
            i = getattr(obj, v, i)
    return i


def named_refs(obj, **opts):
    """Returns (a generator for) all named *referents* of an object
    (re-using functionality from **asizeof**).

    See function **basicsize** for a description of the options.

    Does not return un-named *referents*, e.g. objects in a list.
    """
    t = _typedefof(obj, **opts)
    if t:
        r = t.refs
        if r and _iscallable(r):
            for nr in r(obj, True):
                try:
                    yield nr.name, nr.ref
                except AttributeError:
                    pass


def refs(obj, **opts):
    '''Return (a generator for) specific *referents* of an object.

    See function **basicsize** for a description of the options.
    '''
    r = t = _typedefof(obj, **opts)
    if t:
        r = t.refs
        if r and _iscallable(r):
            r = r(obj, False)
    return r


if __name__ == '__main__':

    if '-types' in sys.argv:  # print static _typedefs
        n = len(_typedefs)
        w = len(str(n)) * ' '
        _printf('%s%d type definitions: %s and %s, kind ... %s', linesep,
                 n, 'basic-', 'itemsize (alen)', '-type[def]s')
        for k, v in sorted((_prepr(k), v) for k, v in _items(_typedefs)):
            s = '%(base)s and %(item)s%(alen)s, %(kind)s%(code)s' % v.format()
            _printf('%s %s: %s', w, k, s)

    else:
        if '-gc' in sys.argv:
            try:
                import gc  # PYCHOK expected
                gc.collect()
            except ImportError:
                pass

        # just an example
        asizeof(all=True, stats=2)  # print summary

    if '-v' in sys.argv:
        print('\n%s %s (Python %s)' % (__file__, __version__, sys.version.split()[0]))

# License from the initial version of this source file follows:

# --------------------------------------------------------------------
#       Copyright (c) 2002-2018 -- ProphICy Semiconductor, Inc.
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
# --------------------------------------------------------------------
