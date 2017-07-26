#!/usr/bin/env python

# Copyright, license and disclaimer are at the end of this file.

'''This module exposes 10 functions and 2 classes to obtain lengths
   and sizes of Python objects (for Python 2.2 or later [1]).

   The main changes in this version are new function  calcsize(),
   use  gc.get_objects() to get all objects, use sys.int_info if
   available and some improvements in the examples and in this
   documentation.

Public Functions [2]

   Function  asizeof calculates the combined (approximate) size
   in bytes of one or several Python objects.

   Function  asizesof returns a tuple containing the (approximate)
   size in bytes for each given Python object separately.

   Function  asized returns for each object an instance of class
   Asized containing all the size information of the object and a
   tuple with the referents.

   Functions  basicsize and  itemsize return the basic respectively
   item size of the given object.

   Function  flatsize returns the flat size of a Python object in
   bytes defined as the basic size plus the item size times the
   length of the given object.

   Function  leng returns the length of an object, like standard
   len but extended for several types, e.g. the  leng of a multi-
   precision int (or long) is the number of digits [3].  The length
   of most mutable sequence objects includes an estimate of the
   over-allocation and therefore, the  leng value may differ from
   the standard  len result.

   Function  refs returns (a generator for) the referents of the
   given object, i.e. the objects referenced by the given object.

   Function  calcsize is equivalent to standard  struct.calcsize
   but handles format characters 'z' for signed C type  Py_ssize_t
   and 'Z' for unsigned C type  size_t.

   Certain classes are known to be sub-classes of or to behave as
   dict objects.  Function  adict can be used to install other
   class objects to be treated like dict.

Public Classes [2]

   An instance of class  Asized is returned for each object sized
   with the  asized function or method.

   Class  Asizer can be used to accumulate the results of several
   asizeof or  asizesof calls.  After creating an  Asizer instance,
   use methods  asizeof and  asizesof to size additional objects.

   Call methods  exclude_refs and/or  exclude_types to exclude
   references to or instances or types of certain objects.

   Use one of the  print\_... methods to report the statistics.

Duplicate Objects

   Any duplicate, given objects are sized only once and the size
   is included in the combined total only once.  But functions
   asizesof and  asized do return a size value respectively an
   Asized instance for each given object, the same for duplicates.

Definitions [4]

   The size of an object is defined as the sum of the flat size
   of the object plus the sizes of any referents.  Referents are
   visited recursively up to a given limit.  However, the size
   of objects referenced multiple times is included only once.

   The flat size of an object is defined as the basic size of the
   object plus the item size times the number of allocated items.
   The flat size does include the size for the items (references
   to the referents), but not the referents themselves.

   The flat size returned by function  flatsize equals the result
   of the  asizeof function with options code=True, ignored=False,
   limit=0 and option  align set to the same value.

   The accurate flat size for an object is obtained from function
   sys.getsizeof() where available.  Otherwise, the length and
   size of sequence objects as dicts, lists, sets, etc. is based
   on an estimate for the number of allocated items.  As a result,
   the reported length and size may substantially differ from the
   actual length and size.

   The basic and item sizes are obtained from the __basicsize__
   respectively __itemsize__ attribute of the (type of the) object.
   Where necessary (e.g. sequence objects), a zero __itemsize__
   is replaced by the size of a corresponding C type.

   The basic size (of GC managed objects) objects includes the
   overhead for Python's garbage collector (GC) as well as the
   space needed for refcounts (only in certain Python builds).

   Optionally, sizes can be aligned to any power of 2 multiple.

Size of (byte)code

   The (byte)code size of objects as classes, functions, methods,
   modules, etc. can be included by setting option  code.

   Iterators are handled similar to sequences: iterated object(s)
   are sized like referents if the recursion limit permits.  Also,
   function  gc.get_referents() must return the referent object
   of iterators.

   Generators are sized as (byte)code only, but generated objects
   are never sized.

Old- and New-style Classes

   All old- and new-style class, instance and type objects, are
   handled uniformly such that (a) instance and class objects can
   be distinguished and (b) instances of different old-style
   classes can be dealt with separately.

   Class and type objects are represented as <class ....* def>
   respectively as <type ... def> where an '*' indicates an old-
   style class and the  def suffix marks the definition object.
   Instances of old-style classes are shown as new-style ones but
   with an '*' at the end of the name, like <class module.name*>.

Ignored Objects

   To avoid excessive sizes, several object types are ignored [4]
   by default, e.g. built-in functions, built-in types and classes
   [5], function globals and module referents.  However, any
   instances thereof are sized and module objects will be sized
   when passed as given objects.  Ignored object types are included
   if option  ignored is set accordingly.

   In addition, many __...__ attributes of callable objects are
   ignored, except crucial ones, e.g. class attributes __dict__,
   __doc__, __name__ and __slots__.  For more details, see the
   type-specific _..._refs() and _len_...() functions below.

   Option  all can be used to size all Python objects and/or get
   the referents from  gc.get_referents() and override the type-
   specific __..._refs() functions.

Notes

   [1] Tested with 32-bit Python 2.2.3, 2.3.7, 2.4.5, 2.5.1, 2.5.2,
       2.6.2, 3.0.1 or 3.1a2 on CentOS 4.6, SuSE 9.3, MacOS X 10.3.9
       Panther (PPC), MacOS X 10.4.11 Tiger, Solaris 10 (Opteron)
       and Windows XP, with 64-bit Python 3.0.1 on RHEL 3u7 and
       Solaris 10 (Opteron) and with 64-bit Python 2.7.10 and 3.5.1
       on MacOS X 10.11.5.

   [2] The functions and classes in this module are not thread-safe.

   [3] See Python source file .../Include/longinterpr.h for the
       C typedef of digit and PYLONG_BITS_IN_DIGIT used in multi-
       precision int (or long) objects.  The digit size in bytes
       can be obtained from int (or long) attribute __itemsize__
       or from sys.int_info since Python 3.1.  Function leng
       (rather _len_int) below determines the number of digits
       from the int (or long) value or from int method bit_length
       since Python 2.7.

   [4] These definitions and other assumptions are rather arbitrary
       and may need corrections or adjustments.

   [5] Types and classes are considered built-in if the module of
       the type or class is listed in  _builtin_modules below.

'''  # PYCHOK expected

from __future__ import generators  # PYCHOK for yield in Python 2.2

from inspect    import getmro, isbuiltin, isclass, iscode, isframe, \
                       isfunction, ismethod, ismodule, stack
from math       import log
from os         import curdir, linesep
from struct     import calcsize as _calcsize
import sys
import types    as     Types
import weakref  as     Weakref

__version__ = '16.07.15'  # aka Revision 18
__all__     = ['adict', 'asized', 'asizeof', 'asizesof',
               'Asized', 'Asizer',  # classes
               'basicsize', 'flatsize', 'itemsize', 'leng', 'refs',
               'calcsize']  # handles 'z' and 'Z'

# any classes or types in modules listed in _builtin_modules are
# considered built-in and ignored by default, as built-in functions
if __name__ == '__main__':
    _builtin_modules = (int.__module__, 'types', Exception.__module__)  # , 'weakref'
else:  # treat this very module as built-in
    _builtin_modules = (int.__module__, 'types', Exception.__module__, __name__)  # , 'weakref'

# sizes of some primitive C types
# XXX len(pack(T, 0)) == Struct(T).size == _calcsize(T)
# but type/class Struct only available since Python 2.5
_sizeof_Cbyte  = _calcsize('c')  # sizeof(unsigned char)
_sizeof_Clong  = _calcsize('l')  # sizeof(long)
_sizeof_Cvoidp = _calcsize('P')  # sizeof(void*)

# sizeof(long) != sizeof(ssize_t) on LLP64
if _sizeof_Clong < _sizeof_Cvoidp:
    _Z = _z = 'P'
else:
    _Z, _z = 'L', 'l'


def calcsize(fmt):
    '''struct.calcsize() substitute handling 'z' for signed Py_ssize_t
       and 'Z' for unsigned size_t.
    '''
    return _calcsize(fmt.replace('Z', _Z).replace('z', _z))

# defaults for some basic sizes with 'z' for C Py_ssize_t
_sizeof_CPyCodeObject   = calcsize('Pz10P5i0P')    # sizeof(PyCodeObject)
_sizeof_CPyFrameObject  = calcsize('Pzz13P63i0P')  # sizeof(PyFrameObject)
_sizeof_CPyModuleObject = calcsize('PzP0P')        # sizeof(PyModuleObject)

# defaults for some item sizes with 'z' for C Py_ssize_t
_sizeof_CPyDictEntry    = calcsize('z2P')  # sizeof(PyDictEntry)
_sizeof_Csetentry       = calcsize('lP')   # sizeof(setentry)

i = getattr(sys, 'int_info', None)  # new in Python 3.1+
if i:
    _bitsof_Cdigit = i.bits_per_digit
    _sizeof_Cdigit = i.sizeof_digit
    if _sizeof_Cdigit != int.__itemsize__:
        raise AssertionError('sizeof(%s) bad: %d vs %s' % ('digit',
                             _sizeof_Cdigit, int.__itemsize__))
else:  # Python 2.x
    try:  # C typedef digit for multi-precision int (or long)
        _sizeof_Cdigit = long.__itemsize__
    except NameError:  # no long in Python 3.0
        _sizeof_Cdigit = int.__itemsize__
    # _bitsof_Cdigit must be a multiple of 5, see PyLong_SHIFT
    # check in C Python source file .../Include/longinterpr.h
    _bitsof_Cdigit = ((_sizeof_Cdigit << 3) // 5) * 5
if _sizeof_Cdigit < 4:
    raise AssertionError('sizeof(%s) bad: %d' % ('digit', _sizeof_Cdigit))
del i

try:  # sizeof(unicode_char) in Python < 3.3
    u = unicode('\0')
except NameError:  # no unicode() in Python 3.0
    u = '\0'
u = u.encode('unicode-internal')  # see .../Lib/test/test_sys.py
_sizeof_Cunicode = len(u)
del u
if (1 << (_sizeof_Cunicode << 3)) <= sys.maxunicode:
    raise AssertionError('sizeof(%s) bad: %d' % ('unicode', _sizeof_Cunicode))

if hasattr(sys, 'maxsize'):  # new in Python 2.6
    Z = calcsize('Z')  # check sizeof(size_t)
    if (1 << (Z << 3)) <= sys.maxsize:
        raise AssertionError('sizeof(%s) bad: %d' % ('size_t', Z))
    del Z

try:  # size of GC header, sizeof(PyGC_Head)
    import _testcapi as t
    _sizeof_CPyGC_Head = t.SIZEOF_PYGC_HEAD  # new in Python 2.6
except (ImportError, AttributeError):  # sizeof(PyGC_Head)
    # alignment should be to sizeof(long double) but there
    # is no way to obtain that value, assume twice double
    t = calcsize('2d') - 1
    _sizeof_CPyGC_Head = (calcsize('2Pz') + t) & ~t
del t

# size of refcounts (Python debug build only)
if hasattr(sys, 'gettotalrefcount'):
    _sizeof_Crefcounts = calcsize('2z')
else:
    _sizeof_Crefcounts = 0

# some flags from .../Include/object.h
_Py_TPFLAGS_HEAPTYPE = 1 <<  9  # Py_TPFLAGS_HEAPTYPE
_Py_TPFLAGS_HAVE_GC  = 1 << 14  # Py_TPFLAGS_HAVE_GC

# 'cell' is holding data used in closures
closure = (lambda x: (lambda: x))(None)
try:
    _Cell_type = type(closure.__closure__[0])
except AttributeError:  # Python 2.5
    _Cell_type = type(closure.func_closure[0])
del closure

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


def _set(*args):
    '''Type set.
    '''
    try:
        return set(args)
    except NameError:
        return tuple(args)


def _values(obj):  # dict only
    '''Use iter-/generator, preferably.
    '''
    return getattr(obj, 'itervalues', obj.values)()


try:  # callable() builtin
    _callable = callable
except NameError:  # callable() removed in Python 3.0
    def _callable(obj):
        '''Substitute for callable().'''
        return hasattr(obj, '__call__')

try:  # get 'all' current objects
    from gc import get_objects as _getobjects
except ImportError:
    def _getobjects():
        # modules first, globals and stack
        # (may contain duplicate objects)
        return tuple(_values(sys.modules)) + (
               globals(), stack(sys.getrecursionlimit()))

try:  # get 'all' referents of objects
    # note that gc.get_referents()
    # returns () for dict...-iterators
    from gc import get_referents as _getreferents
except ImportError:  # no get_referents() in Python 2.2
    def _getreferents(unused):
        return ()  # sorry, no refs

# sys.getsizeof() new in Python 2.6 (prior to Python
# 2.7.4 and 3.2.4, sys.getsizeof(array) was unreliable)
_getsizeof = getattr(sys, 'getsizeof', None)

try:  # str intern()
    _intern = intern
except NameError:  # no intern() in Python 3.0
    def _intern(val):
        return val


def _kwds(**kwds):  # no dict(key=value, ...) in Python 2.2
    '''Return name=value pairs as keywords dict.
    '''
    return kwds

try:  # sorted() builtin
    _sorted = sorted
except NameError:  # no sorted() in Python 2.2
    def _sorted(vals, reverse=False, **unused):
        '''Partial substitute for missing sorted().'''
        vals.sort()  # inplace OK
        if reverse:
            vals.reverse()
        return vals

try:  # sum() builtin
    _sum = sum
except NameError:  # no sum() in Python 2.2
    def _sum(vals, start=0):
        '''Partial substitute for missing sum().'''
        s = start
        for v in vals:
            s += v
        return s


# private functions

def _basicsize(t, base=0, heap=False, obj=None):
    '''Get non-zero basicsize of type,
       including the header sizes.
    '''
    s = max(getattr(t, '__basicsize__', 0), base)
    # include gc header size
    if t != _Type_type:
        h = getattr(t,   '__flags__', 0) & _Py_TPFLAGS_HAVE_GC
    elif heap:  # type, allocated on heap
        h = True
    else:  # None has no __flags__ attr
        h = getattr(obj, '__flags__', 0) & _Py_TPFLAGS_HEAPTYPE
    if h:
        s += _sizeof_CPyGC_Head
    # include reference counters
    return s + _sizeof_Crefcounts


def _derive_typedef(typ):
    '''Return single, existing super type typedef or None.
    '''
    v = [v for v in _values(_typedefs) if _issubclass(typ, v.type)]
    if len(v) == 1:
        return v[0]
    return None


def _dir2(obj, pref='', excl=(), slots=None, itor=''):
    '''Return an attribute name, object 2-tuple for certain
       attributes or for the '__slots__' attributes of the
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
                    if a.startswith('__'):  # XXX
                        a = '_' + c.__name__ + a
                    if hasattr(obj, a):
                        s.setdefault(a, getattr(obj, a))
            # assume __slots__ tuple/list
            # is holding the attr values
            yield slots, _Slots(s)  # _keys(s)
            for t in _items(s):
                yield t  # attr name, value
    elif itor:  # iterator referents
        for o in obj:  # iter(obj)
            yield itor, o
    else:  # regular attrs
        for a in dir(obj):
            if a.startswith(pref) and a not in excl and hasattr(obj, a):
                yield a, getattr(obj, a)


def _infer_dict(obj):
    '''Return True for likely dict object.
    '''
    for ats in (('__len__', 'get', 'has_key',     'items',     'keys',     'values'),
                ('__len__', 'get', 'has_key', 'iteritems', 'iterkeys', 'itervalues')):
        for a in ats:  # no all(<generator_expression>) in Python 2.2
            if not _callable(getattr(obj, a, None)):
                break
        else:  # all True
            return True
    return False


def _iscell(obj):
    '''Return True if obj is a cell as used in a closure.
    '''
    return isinstance(obj, _Cell_type)


def _isdictclass(obj):
    '''Return True for known dict objects.
    '''
    c = getattr(obj, '__class__', None)
    return c and c.__name__ in _dict_classes.get(c.__module__, ())


def _isnamedtuple(obj):  # rather instance of a namedtuple
    '''Named tuple instances are identified via duck typing, see
       <http://www.gossamer-threads.com/lists/python/dev/1142178>,
    '''
    if isinstance(obj, tuple):  # and hasattr(obj, '__slots__'):
        fs = getattr(obj, '_fields', None)
        if isinstance(fs, tuple) and len(fs) == len(obj):
            # each of the _fields items is an attr
            # name and each such attr is a property
            return True
    return False


def _issubclass(sub, sup):
    '''Safe issubclass().
    '''
    if sup is not object:
        try:  # builtin
            return issubclass(sub, sup)
        except TypeError:
            pass
    return sup in getmro(sub)


def _itemsize(t, item=0):
    '''Get non-zero itemsize of type.
    '''
    # replace zero value with default
    return getattr(t, '__itemsize__', 0) or item


def _kwdstr(**kwds):
    '''Keyword arguments as a string.
    '''
    return ', '.join(_sorted(['%s=%r' % kv for kv in _items(kwds)]))  # [] for Python 2.2


def _lengstr(obj):
    '''Object length as a string.
    '''
    n = leng(obj)
    if n is None:  # no len
        r = ''
    elif n > _len(obj):  # extended
        r = ' leng %d!' % n
    else:
        r = ' leng %d' % n
    return r


def _nameof(obj, dflt=''):
    '''Return the name of an object.
    '''
    return getattr(obj, '__name__', dflt)


def _objs(objs, all=None, **unused):
    '''Return the given or 'all' objects.
    '''
    if objs:
        t = objs
    elif all in (False, None):
        t = ()
    elif all is True:  # 'all' objects
        t = _getobjects()
    else:
        raise ValueError('invalid option: %s=%r' % ('all', all))
    return t


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
    '''Find the next power of 2.
    '''
    p2 = 16
    while n > p2:
        p2 += p2
    return p2


def _prepr(obj, clip=0):
    '''Prettify and clip long repr() string.
    '''
    return _repr(obj, clip=clip).strip('<>').replace("'", '')  # remove <''>


def _printf(fmt, *args, **opts):
    '''Formatted print.
    '''
    if opts:  # like Python 3.0
        f = opts.get('file', None) or sys.stdout
        if args:
            f.write(fmt % args)
        else:
            f.write(fmt)
        f.write(opts.get('end', linesep))
    elif args:
        print(fmt % args)
    else:
        print(fmt)


def _refs(obj, named, *ats, **kwds):
    '''Return specific attribute objects of an object.
    '''
    if named:
        for a in ats:  # cf. inspect.getmembers()
            if hasattr(obj, a):
                yield _NamedRef(a, getattr(obj, a))
        if kwds:  # kwds are _dir2() args
            for a, o in _dir2(obj, **kwds):
                yield _NamedRef(a, o)
    else:
        for a in ats:  # cf. inspect.getmembers()
            if hasattr(obj, a):
                yield getattr(obj, a)
        if kwds:  # kwds are _dir2() args
            for _, o in _dir2(obj, **kwds):
                yield o


def _repr(obj, clip=80):
    '''Clip long repr() string.
    '''
    try:  # safe repr()
        r = repr(obj)
    except TypeError:  # XXX Exception
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


# type-specific referent functions

def _cell_refs(obj, named):
    return _refs(obj, named, 'cell_contents')


def _class_refs(obj, named):
    '''Return specific referents of a class object.
    '''
    return _refs(obj, named, '__class__', '__dict__',  '__doc__', '__mro__',
                             '__name__',  '__slots__', '__weakref__')


def _co_refs(obj, named):
    '''Return specific referents of a code object.
    '''
    return _refs(obj, named, pref='co_')


def _dict_refs(obj, named):
    '''Return key and value objects of a dict/proxy.
    '''
    if named:
        for k, v in _items(obj):
            s = str(k)
            yield _NamedRef(s, k, 1)  # key
            yield _NamedRef(s, v, 2)  # value
    else:  # XXX try: ... except ReferenceError
        for k, v in _items(obj):
            yield k
            yield v


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
    return _refs(obj, named, '__doc__', '__name__', '__code__',
                             pref='im_')


def _inst_refs(obj, named):
    '''Return specific referents of a class instance.
    '''
    return _refs(obj, named, '__dict__', '__class__',
                             slots='__slots__')


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
    '''Return slots but exclude dict
    '''
    return _refs(obj, named, '__class__', slots='__slots__')


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
    except:  # XXX ReferenceError
        return ()  # PYCHOK OK


_all_refs = _set(_cell_refs,    _class_refs,  _co_refs,
                 _dict_refs,    _enum_refs,   _exc_refs,
                 _file_refs,    _frame_refs,  _func_refs,
                 _gen_refs,     _im_refs,     _inst_refs,
                 _iter_refs,    _module_refs, _namedtuple_refs,
                 _prop_refs,    _seq_refs,    _stat_refs,
                 _statvfs_refs, _tb_refs,     _type_refs,
                 _weak_refs,     None)


# type-specific length functions

def _len(obj):
    '''Safe len().
    '''
    try:
        return len(obj)
    except TypeError:  # no len()
        return 0


def _len_array(obj):
    '''Array length in bytes.
    '''
    return len(obj) * obj.itemsize


def _len_bytearray(obj):
    '''Bytearray size.
    '''
    return obj.__alloc__()


def _len_code(obj):  # see .../Lib/test/test_sys.py
    '''Length of code object (stack and variables only).
    '''
    return obj.co_stacksize +      obj.co_nlocals  \
                            + _len(obj.co_freevars) \
                            + _len(obj.co_cellvars) - 1


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


if hasattr(int, 'bit_length'):
    def _len_int(obj):
        '''Length of multi-precision int in digits.
        '''
        # bit_length returns zero for zero value
        return (obj.bit_length() + _bitsof_Cdigit - 1) // _bitsof_Cdigit
else:
    _digit_max = (1 << _bitsof_Cdigit) - 1  # == (2 * PyLong_MASK + 1)
    _digit_log =  1.0 / log(_digit_max + 1.0)

    def _len_int(obj):  # PYCHOK expected
        '''Length of multi-precision int (aka long) in digits.
        '''
        if obj:
            n, i = 1, abs(obj)
            if i > _digit_max:
                # no log(x[, base]) in Python 2.2
                n += int(log(i) * _digit_log)
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


def _len_slots(obj):
    '''Slots length.
    '''
    return len(obj)  # XXX - 1


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


_all_lengs = _set(_len,        _len_array,  _len_bytearray,
                  _len_code,   _len_dict,   _len_frame,
                  _len_int,    _len_iter,   _len_list,
                  _len_module, _len_set,    _len_slice,
                  _len_slots,  _len_struct, _len_unicode, None)


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
# _typedefs dict further below, except class (and type) objects
# and old-style instances.  Those are wrapped with separate
# _Claskey or _Instkey instances to be able (1) to distinguish
# instances of different old-style classes by class, (2) to
# distinguish class (and type) instances from class (and type)
# definitions for new-style classes and (3) provide similar
# results for repr() and str() of new- and old-style classes
# and instances.

_claskeys = {}  # [id(obj)] = _Claskey()


def _claskey(obj, style):
    '''Wrap an old- or new-style class object.
    '''
    i =  id(obj)
    k = _claskeys.get(i, None)
    if not k:
        _claskeys[i] = k = _Claskey(obj, style)
    return k


try:  # no Class- and InstanceType in Python 3.0
    _Types_ClassType    = Types.ClassType
    _Types_InstanceType = Types.InstanceType

    class _Instkey(object):
        '''Wrapper for old-style class (instances).
        '''
        __slots__ = ('_obj',)

        def __init__(self, obj):
            self._obj = obj  # XXX Weakref.ref(obj)

        def __str__(self):
            return '<class %s.%s%s>' % (self._obj.__module__, self._obj.__name__, _old_style)
        __repr__ = __str__

    _instkeys = {}  # [id(obj)] = _Instkey()

    def _instkey(obj):
        '''Wrap an old-style class (instance).
        '''
        i =  id(obj)
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
            return _claskey(t,   _old_style), _instkey(t)
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
    __slots__ = ('name', 'ref', 'typ')

    def __init__(self, name, ref, typ=0):
        self.name = name
        self.ref  = ref
        self.typ  = typ  # see Asized.format


class _Slots(tuple):
    '''Wrapper class for __slots__ attribute at
       class instances to account for the size
       of the __slots__ tuple/list containing
       references to the attribute values.
    '''
    pass


# kinds of _Typedefs
_i = _intern
_t = (_kind_static, _kind_dynamic, _kind_derived, _kind_ignored, _kind_inferred) = (
        _i('static'), _i('dynamic'), _i('derived'), _i('ignored'), _i('inferred'))
_all_kinds = _set(*_t)
del _i, _t


class _Typedef(object):
    '''Type definition class.
    '''
    __slots__ = {
        'base': 0,     # basic size in bytes
        'item': 0,     # item size in bytes
        'leng': None,  # or _len_...() function
        'refs': None,  # or _..._refs() function
        'both': None,  # both data and code if True, code only if False
        'kind': None,  # _kind_... value
        'type': None}  # original type

    def __init__(self, **kwds):
        self.reset(**kwds)

    def __lt__(self, unused):  # for Python 3.0
        return True

    def __repr__(self):
        return repr(self.args())

    def __str__(self):
        t = [str(self.base), str(self.item)]
        for f in (self.leng, self.refs):
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
        return (self.base, self.item, self.leng, self.refs,
                self.both, self.kind, self.type)

    def dup(self, other=None, **kwds):
        '''Duplicate attributes of dict or other typedef.
        '''
        if other is None:
            d = _dict_typedef.kwds()
        else:
            d =  other.kwds()
        d.update(kwds)
        self.reset(**d)

    def flat(self, obj, mask=0):
        '''Return the aligned flat size.
        '''
        s = self.base
        if self.leng and self.item > 0:  # include items
            s += self.leng(obj) * self.item
        if _getsizeof:  # _getsizeof prevails
            s = _getsizeof(obj, s)
        if mask:  # align
            s = (s + mask) & ~mask
        return s

    def format(self):
        '''Return format dict.
        '''
        c = n = ''
        if not self.both:
            c = ' (code only)'
        if self.leng:
            n = ' (%s)' % _nameof(self.leng)
        return _kwds(base=self.base, item=self.item, leng=n,
                     code=c,         kind=self.kind)

    def kwds(self):
        '''Return all attributes as keywords dict.
        '''
        # no dict(refs=self.refs, ..., kind=self.kind) in Python 2.0
        return _kwds(base=self.base, item=self.item,
                     leng=self.leng, refs=self.refs,
                     both=self.both, kind=self.kind, type=self.type)

    def save(self, t, base=0, heap=False):
        '''Save this typedef plus its class typedef.
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
        '''Set one or more attributes.
        '''
        if kwds:  # double check
            d = self.kwds()
            d.update(kwds)
            self.reset(**d)
        if safe_len and self.item:
            self.leng = _len

    def reset(self, base=0, item=0, leng=None, refs=None,
                                    both=True, kind=None, type=None):
        '''Reset all specified attributes.
        '''
        if base < 0:
            raise ValueError('invalid option: %s=%r' % ('base', base))
        else:
            self.base = base
        if item < 0:
            raise ValueError('invalid option: %s=%r' % ('item', item))
        else:
            self.item = item
        if leng in _all_lengs:  # XXX or _callable(leng)
            self.leng = leng
        else:
            raise ValueError('invalid option: %s=%r' % ('leng', leng))
        if refs in _all_refs:  # XXX or _callable(refs)
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


_typedefs = {}  # [key] = _Typedef()


def _typedef_both(t, base=0, item=0, leng=None, refs=None, kind=_kind_static, heap=False):
    '''Add new typedef for both data and code.
    '''
    v = _Typedef(base=_basicsize(t, base=base), item=_itemsize(t, item),
                 refs=refs, leng=leng,
                 both=True, kind=kind, type=t)
    v.save(t, base=base, heap=heap)
    return v  # for _dict_typedef


def _typedef_code(t, base=0, refs=None, kind=_kind_static, heap=False):
    '''Add new typedef for code only.
    '''
    v = _Typedef(base=_basicsize(t, base=base),
                 refs=refs,
                 both=False, kind=kind, type=t)
    v.save(t, base=base, heap=heap)
    return v  # for _dict_typedef

# static typedefs for data and code types
_typedef_both(complex)
_typedef_both(float)
_typedef_both(list,     refs=_seq_refs, leng=_len_list, item=_sizeof_Cvoidp)  # sizeof(PyObject*)
_typedef_both(tuple,    refs=_seq_refs, leng=_len,      item=_sizeof_Cvoidp)  # sizeof(PyObject*)
_typedef_both(property, refs=_prop_refs)
_typedef_both(type(Ellipsis))
_typedef_both(type(None))

# _Slots is a special tuple, see _Slots.__doc__
_typedef_both(_Slots, item=_sizeof_Cvoidp,
                      leng=_len_slots,  # length less one
                      refs=None,  # but no referents
                      heap=True)  # plus head

# dict, dictproxy, dict_proxy and other dict-like types
_dict_typedef = _typedef_both(dict,        item=_sizeof_CPyDictEntry, leng=_len_dict, refs=_dict_refs)
try:  # <type dictproxy> only in Python 2.x
    _typedef_both(Types.DictProxyType,     item=_sizeof_CPyDictEntry, leng=_len_dict, refs=_dict_refs)
except AttributeError:  # XXX any class __dict__ is <type dict_proxy> in Python 3.0?
    _typedef_both(type(_Typedef.__dict__), item=_sizeof_CPyDictEntry, leng=_len_dict, refs=_dict_refs)
# other dict-like classes and types may be derived or inferred,
# provided the module and class name is listed here (see functions
# adict, _isdictclass and _infer_dict for further details)
_dict_classes = {'UserDict': ('IterableUserDict',  'UserDict'),
                 'weakref' : ('WeakKeyDictionary', 'WeakValueDictionary')}
try:  # <type module> is essentially a dict
    _typedef_both(Types.ModuleType, base=_dict_typedef.base,
                                    item=_dict_typedef.item + _sizeof_CPyModuleObject,
                                    leng=_len_module, refs=_module_refs)
except AttributeError:  # missing
    pass

# newer or obsolete types
try:
    from array import array  # array type
    _typedef_both(array, leng=_len_array, item=_sizeof_Cbyte)
except ImportError:  # missing
    pass

try:  # bool has non-zero __itemsize__ in 3.0
    _typedef_both(bool)
except NameError:  # missing
    pass

try:  # ignore basestring
    _typedef_both(basestring, leng=None)
except NameError:  # missing
    pass

try:
    if isbuiltin(buffer):  # Python 2.2
        _typedef_both(type(buffer('')), item=_sizeof_Cbyte, leng=_len)  # XXX len in bytes?
    else:
        _typedef_both(buffer,           item=_sizeof_Cbyte, leng=_len)  # XXX len in bytes?
except NameError:  # missing
    pass

try:
    _typedef_both(bytearray, item=_sizeof_Cbyte, leng=_len_bytearray)  # PYCHOK bytearray new in 2.6, 3.0
except NameError:  # missing
    pass
try:
    if type(bytes) is not type(str):  # bytes is str in 2.6 # PYCHOK bytes new in 2.6, 3.0
      _typedef_both(bytes, item=_sizeof_Cbyte, leng=_len)  # PYCHOK bytes new in 2.6, 3.0
except NameError:  # missing
    pass
try:  # XXX like bytes
    _typedef_both(str8, item=_sizeof_Cbyte, leng=_len)  # PYCHOK str8 new in 2.6, 3.0?
except NameError:  # missing
    pass

try:
    _typedef_both(enumerate, refs=_enum_refs)
except NameError:  # missing
    pass

try:  # Exception is type in Python 3.0
    _typedef_both(Exception, refs=_exc_refs)
except:  # missing
    pass  # PYCHOK OK

try:
    _typedef_both(file, refs=_file_refs)
except NameError:  # missing
    pass

try:
    _typedef_both(frozenset, item=_sizeof_Csetentry, leng=_len_set, refs=_seq_refs)
except NameError:  # missing
    pass
try:
    _typedef_both(set,       item=_sizeof_Csetentry, leng=_len_set, refs=_seq_refs)
except NameError:  # missing
    pass

try:  # not callable()
    _typedef_both(Types.GetSetDescriptorType)
except AttributeError:  # missing
    pass

try:  # if long exists, it is multi-precision ...
    _typedef_both(long, item=_sizeof_Cdigit, leng=_len_int)
    _typedef_both(int)  # ... and int is fixed size
except NameError:  # no long, only multi-precision int in Python 3.0
    _typedef_both(int,  item=_sizeof_Cdigit, leng=_len_int)

try:  # not callable()
    _typedef_both(Types.MemberDescriptorType)
except AttributeError:  # missing
    pass

try:
    from collections import namedtuple  # function
    _Namedtuple = namedtuple('_Namedtuple', 'x')  # verbose=True
    _typedef_both(_Namedtuple, refs=_seq_refs, leng=_len, item=_sizeof_Cvoidp)  # sizeof(PyObject*)
    del _Namedtuple
except ImportError:
    namedtuple = None

try:
    _typedef_both(type(NotImplemented))  # == Types.NotImplementedType
except NameError:  # missing
    pass

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
    _typedef_both(slice, item=_sizeof_Cvoidp, leng=_len_slice)  # XXX worst-case itemsize?
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
                                         item=_sizeof_Cvoidp, leng=_len)
except ImportError:  # missing
    pass

try:
    from struct import Struct  # only in Python 2.5 and 3.0
    _typedef_both(Struct, item=_sizeof_Cbyte, leng=_len_struct)  # len in bytes
except ImportError:  # missing
    pass

try:
    _typedef_both(Types.TracebackType, refs=_tb_refs)
except AttributeError:  # missing
    pass

try:
    _typedef_both(unicode, leng=_len_unicode, item=_sizeof_Cunicode)
    _typedef_both(str,     leng=_len,         item=_sizeof_Cbyte)  # 1-byte char
except NameError:  # str is unicode
    _typedef_both(str,     leng=_len_unicode, item=_sizeof_Cunicode)

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
_typedef_code(object,     kind=_kind_ignored)
_typedef_code(super,      kind=_kind_ignored)
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
    if t.type and t.leng:
        try:  # create an (empty) instance
            s.append(t.type())
        except TypeError:
            pass
for t in s:
    try:
        i = iter(t)
        _typedef_both(type(i), leng=_len_iter, refs=_iter_refs, item=0)  # no itemsize!
    except (KeyError, TypeError):  # ignore non-iterables, duplicates, etc.
        pass
del i, s, t


def _typedef(obj, derive=False, infer=False):
    '''Create a new typedef for an object.
    '''
    t =  type(obj)
    v = _Typedef(base=_basicsize(t, obj=obj),
                 kind=_kind_dynamic, type=t)
#   _printf('new %r %r/%r %s', t, _basicsize(t), _itemsize(t), _repr(dir(obj)))
    if ismodule(obj):  # handle module like dict
        v.dup(item=_dict_typedef.item + _sizeof_CPyModuleObject,
              leng=_len_module,
              refs=_module_refs)
    elif isframe(obj):
        v.set(base=_basicsize(t, base=_sizeof_CPyFrameObject, obj=obj),
              item=_itemsize(t),
              leng=_len_frame,
              refs=_frame_refs)
    elif iscode(obj):
        v.set(base=_basicsize(t, base=_sizeof_CPyCodeObject, obj=obj),
              item=_sizeof_Cvoidp,
              leng=_len_code,
              refs=_co_refs,
              both=False)  # code only
    elif _callable(obj):
        if isclass(obj):  # class or type
            v.set(refs=_class_refs,
                  both=False)  # code only
            if getattr(obj, '__module__', None) in _builtin_modules:
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
    elif getattr(obj, '__module__', None) in _builtin_modules:
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
    total  = 0      # total size
    high   = 0      # largest size
    number = 0      # number of (unique) objects
    objref = None   # largest object (weakref)
    weak   = False  # objref is weakref(object)

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
        return _kwds(avg=_SI2(a),         high=_SI2(self.high),
                     lengstr=_lengstr(o), obj=_repr(o, clip=clip),
                     plural=p,            total=t)

    def update(self, obj, size):
        '''Update this profile.
        '''
        self.number += 1
        self.total  += size
        if self.high < size:  # largest
            self.high = size
            try:  # prefer using weak ref
                self.objref, self.weak = Weakref.ref(obj), True
            except TypeError:
                self.objref, self.weak = obj, False


# public classes

class Asized(object):
    '''Store the results of an  asized object
       in these 4 attributes:

       size - total size of the object
       flat - flat size of the object
       name - name or repr of the object
       refs - tuple containing an instance
              of  Asized for each referent
    '''
    strf = (    '%s',  # default name format
            '[K] %s',  # dict key, see _dict_refs
            '[V] %s')  # dict value, see _dict_refs

    def __init__(self, size, flat, refs=(), name=None):
        self.size = size  # total size
        self.flat = flat  # flat size
        self.name = name  # name, repr or None
        self.refs = tuple(refs)

    def __str__(self):
        return 'size %r, flat %r, refs[%d], name %r' % (
                self.size, self.flat, len(self.refs), self.name)

    def format(self, named):
        '''Format name from _NamedRef instance.
        '''
        return self.strf[named.typ] % named.name

    def formatf(self, format='%(name)s size=%(size)d flat=%(flat)d',
                      depth=-1, order_by='size', tab='    ', indent=''):
        '''Format the size information of the object and recursively
           of all sized referents into a single, multi-line string.

        :param format: Specifies the format per instance with 'name',
                       'size' and 'flat' as valid interpolation parameters.
        :param depth: Recursion level for referents to be printed.
        :param order_by: Control sort order of referents.  Valid options
                         are 'name', 'size' and 'flat'.
        :param tab: Indentation string.
        '''
        rev = order_by in ('size', 'flat')

        def _by(x):
            return getattr(x, order_by)

        s = indent + (format % self.__dict__)
        if depth and self.refs:
            depth -= 1
            indent += tab
            rs = [s]
            for r in _sorted(self.refs, key=_by, reverse=rev):
                rs.append(r.formatf(format=format, depth=depth,
                                    order_by=order_by, tab=tab,
                                    indent=indent))
            s = '\n'.join(rs)
        return s


class Asizer(object):
    '''Sizer state and options.
    '''
    _align_    = 8
    _all_      = False
    _clip_     = 80
    _code_     = False
    _derive_   = False
    _detail_   = 0  # for Asized only
    _file_     = None  # print stream
    _infer_    = False
    _limit_    = 100
    _stats_    = 0

    _cutoff    = 0  # in percent
    _depth     = 0  # recursion depth
    _duplicate = 0
    _excl_d    = None  # {}
    _ign_d     = _kind_ignored
    _incl      = ''  # or ' (incl. code)'
    _mask      = 7   # see _align_
    _missed    = 0   # due to errors
    _profile   = False
    _profs     = None  # {}
    _seen      = None  # {}
    _total     = 0   # total size

    def __init__(self, **opts):
        '''See method  reset for the available options.
        '''
        self._excl_d = {}
        self.reset(**opts)

    def _clear(self):
        '''Clear state.
        '''
        self._all_      = False
        self._depth     = 0   # recursion depth
        self._duplicate = 0
        self._incl      = ''  # or ' (incl. code)'
        self._missed    = 0   # due to errors
        self._profile   = False
        self._profs     = {}
        self._seen      = {}
        self._total     = 0   # total size
        for k in _keys(self._excl_d):
            self._excl_d[k] = 0

    def _nameof(self, obj):
        '''Return the object's name.
        '''
        return _nameof(obj, '') or self._repr(obj)

    def _prepr(self, obj):
        '''Like prepr().
        '''
        return _prepr(obj, clip=self._clip_)

    def _printf(self, *args):
        '''Print to the pre-set stream, if any.
        '''
        if self._file_:
            _printf(*args, **{'file': self._file_})
        else:
            _printf(*args)

    def _prof(self, key):
        '''Get _Prof object.
        '''
        p = self._profs.get(key, None)
        if not p:
            self._profs[key] = p = _Prof()
        return p

    def _repr(self, obj):
        '''Like repr().
        '''
        return _repr(obj, clip=self._clip_)

    def _sizer(self, obj, deep, sized):
        '''Size an object, recursively.
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
                    if deep < self._limit_ and not (deep and ismodule(obj)):
                        # add sizes of referents
                        r, z, d = v.refs, self._sizer, deep + 1
                        if self._all_:  # for 'all' referents
                            r = _getreferents(obj)
                            if r:
                                t = id(r)
                                if t in self._seen:
                                    for o in r:  # no sum(<generator_expression>) in Python 2.2
                                        s += z(o, d, None)
                                else:  # exclude container
                                    self._seen[t] = 0
                                    for o in r:  # no sum(<generator_expression>) in Python 2.2
                                        s += z(o, d, None)
                                    del self._seen[t]
                        elif r:  # and _callable(r):
                            if sized and deep < self._detail_:
                                # use named referents
                                for o in r(obj, True):
                                    if isinstance(o, _NamedRef):
                                        t = z(o.ref, d, sized)
                                        t.name = t.format(o)
                                    else:
                                        t = z(o, d, sized)
                                        t.name = self._nameof(o)
                                    rs.append(t)
                                    s += t.size
                            else:  # no sum(<generator_expression>) in Python 2.2
                                for o in r(obj, False):
                                    s += z(o, d, None)
                        # recursion depth
                        if self._depth < d:
                            self._depth = d
            self._seen[i] += 1
        except RuntimeError:  # XXX RecursionLimitExceeded:
            self._missed += 1
        if sized:
            s = sized(s, f, name=self._nameof(obj), refs=rs)
        return s

    def _sizes(self, objs, sized=None):
        '''Return the size or an Asized instance for each
           given object and the total size.  The total
           includes the size of duplicates only once.
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
            s = _sum([i.size for i in _values(s)])  # [] for Python 2.2  # PYCHOK OK
        else:
            s = _sum(_values(s))
        self._total += s  # accumulate
        return s, tuple(t)

    def asized(self, *objs, **opts):
        '''Size each object and return an Asized instance with
           size information and referents up to the given detail
           level (and with modified options, see method  set).

           If only one object is given, the return value is the
           Asized instance for that object.
        '''
        if opts:
            self.set(**opts)
        if self._all_:
            raise KeyError('invalid option: %s=%r' % ('all', self._all_))
        _, t = self._sizes(objs, Asized)
        if len(t) == 1:
            t = t[0]
        return t

    def asizeof(self, *objs, **opts):
        '''Return the combined size of the given objects
           (with modified options, see also method  set).
        '''
        if opts:
            self.set(**opts)
        s, _ = self._sizes(objs, None)
        return s

    def asizesof(self, *objs, **opts):
        '''Return the individual sizes of the given objects
           (with modified options, see also method  set).
        '''
        if opts:
            self.set(**opts)
        _, t = self._sizes(objs, None)
        return t

    def exclude_refs(self, *objs):
        '''Exclude any references to the specified objects from sizing.

           While any references to the given objects are excluded, the
           objects will be sized if specified as positional arguments
           in subsequent calls to methods  asizeof and  asizesof.
        '''
        for o in objs:
            self._seen.setdefault(id(o), 0)

    def exclude_types(self, *objs):
        '''Exclude the specified object instances and types from sizing.

           All instances and types of the given objects are excluded,
           even objects specified as positional arguments in subsequent
           calls to methods  asizeof and  asizesof.
        '''
        for o in objs:
            for t in _keytuple(o):
                if t and t not in self._excl_d:
                    self._excl_d[t] = 0

    def print_profiles(self, w=0, cutoff=0):
        '''Print the profiles above cutoff percentage.

               w=0      -- indentation for each line
               cutoff=0 -- minimum percentage printed
        '''
        # get the profiles with non-zero size or count
        t = [(v, k) for k, v in _items(self._profs) if v.total > 0 or v.number > 1]
        if (len(self._profs) - len(t)) < 9:  # just show all
            t = [(v, k) for k, v in _items(self._profs)]
        if t:
            p, s = self._printf, ''
            if self._total:
                s = ' (% of grand total)'
                c = max(cutoff, self._cutoff)
                c = int(c * 0.01 * self._total)
            else:
                c = 0
            p('%s%*d profile%s:  total%s, average, and largest flat size%s:  largest object',
               linesep, w, len(t), _plural(len(t)), s, self._incl)
            r = len(t)
            for v, k in _sorted(t, reverse=True):
                s = 'object%(plural)s:  %(total)s, %(avg)s, %(high)s:  %(obj)s%(lengstr)s' % v.format(self._clip_, self._total)
                p('%*d %s %s', w, v.number, self._prepr(k), s)
                r -= 1
                if r > 1 and v.total < c:
                    c = max(cutoff, self._cutoff)
                    p('%+*d profiles below cutoff (%.0f%%)', w, r, c)
                    break
            z = len(self._profs) - len(t)
            if z > 0:
                p('%+*d %r object%s', w, z, 'zero', _plural(z))

    def print_stats(self, objs=(), opts={}, sized=(), sizes=(), stats=3.0):
        '''Print the statistics for the results returned by and options
           passed to method or function asized, asizeof and asizesof.

               w=0       -- indentation for each line
               objs=()   -- optional, list of objects
               opts={}   -- optional, dict of options used
               sized=()  -- optional, tuple of  Asized instances returned
               sizes=()  -- optional, tuple of sizes returned
               stats=3.0 -- stats level and cutoff percentage

           A positive value for  stats prints up to 8 statistics, (1)
           a summary of the number of objects sized and seen, (2) a
           simple profile of the sized objects by type and (3+) up
           to 6 tables showing the static, dynamic, derived, ignored,
           inferred and dict types used, found respectively installed.

           The fractional part of the  stats value (x 100) is the
           cutoff percentage for simple profiles.  Objects below
           the cutoff value are not reported.
        '''
        p = self._printf
        s = min(opts.get('stats', stats) or 0, self._stats_)
        if s > 0:  # print stats
            t = self._total + self._missed + _sum(_values(self._seen))
            w = len(str(t)) + 1
            t = c = ''
            o = _kwdstr(**opts)
            if o and objs:
                c = ', '
            # print header line(s)
            if sized and objs:
                n = len(objs)
                if n > 1:
                    p('%sasized(...%s%s) ...', linesep, c, o)
                    for i in range(n):  # no enumerate in Python 2.2.3
                        p('%*d: %s', w-1, i, sized[i])
                else:
                    p('%sasized(%s): %s', linesep, o, sized)
            elif sizes and objs:
                p('%sasizesof(...%s%s) ...', linesep, c, o)
                for z, o in zip(sizes, objs):
                    p('%*d bytes%s%s:  %s', w, z, _SI(z), self._incl, self._repr(o))
            else:
                if objs:
                    t = self._repr(objs)
                p('%sasizeof(%s%s%s) ...', linesep, t, c, o)
            # print summary
            self.print_summary(w=w, objs=objs)
            if s > 1:  # print profile
                c = int(s - int(s)) * 100
                self.print_profiles(w=w, cutoff=c)
                if s > 2:  # print typedefs
                    self.print_typedefs(w=w)

    def print_summary(self, w=0, objs=()):
        '''Print the summary statistics.

               w=0     -- indentation for each line
               objs=() -- optional, list of objects
        '''
        p = self._printf
        p('%*d bytes%s%s', w, self._total, _SI(self._total), self._incl)
        if self._mask:
            p('%*d byte aligned', w, self._mask + 1)
        p('%*d byte sizeof(void*)', w, _sizeof_Cvoidp)
        n = len(objs or ())
        if n > 0:
            d = self._duplicate or ''
            if d:
                d = ', %d duplicate' % self._duplicate
            p('%*d object%s given%s', w, n, _plural(n), d)
        t = _sum([1 for t in _values(self._seen) if t != 0])  # [] for Python 2.2
        p('%*d object%s sized', w, t, _plural(t))
        if self._excl_d:
            t = _sum(_values(self._excl_d))
            p('%*d object%s excluded', w, t, _plural(t))
        t = _sum(_values(self._seen))
        p('%*d object%s seen', w, t, _plural(t))
        if self._missed > 0:
            p('%*d object%s missed', w, self._missed, _plural(self._missed))
        if self._depth > 0:
            p('%*d recursion depth', w, self._depth)

    def print_typedefs(self, w=0):
        '''Print the types and dict tables.

               w=0 -- indentation for each line
        '''
        p = self._printf
        for k in _all_kinds:
            # XXX Python 3.0 doesn't sort type objects
            t = [(self._prepr(a), v) for a, v in _items(_typedefs) if v.kind == k and (v.both or self._code_)]
            if t:
                p('%s%*d %s type%s:  basicsize, itemsize, _len_(), _refs()',
                   linesep, w, len(t), k, _plural(len(t)))
                for a, v in _sorted(t):
                    p('%*s %s:  %s', w, '', a, v)
        # dict and dict-like classes
        t = _sum([len(v) for v in _values(_dict_classes)])  # [] for Python 2.2
        if t:
            p('%s%*d dict/-like classes:', linesep, w, t)
            for m, v in _items(_dict_classes):
                p('%*s %s:  %s', w, '', m, self._prepr(v))

    def set(self, align=None, all=None, code=None, detail=None,
                  file=None, limit=None, stats=None):
        '''Set some options.  Any options not set
           remain the same as the previous setting.

               align=8    -- size alignment
               all=False  -- all (GC) objects and referents
               code=False -- incl. (byte)code size
               detail=0   -- Asized refs level
               file=None  -- output stream for printing
               limit=100  -- recursion limit
               stats=0.0  -- print stats and cutoff percentage

           See function  asizeof for a more detailed description
           of these options.
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
        if all is not None:
            self._all_ = all
        if code is not None:
            self._code_ = code
            if code:  # incl. (byte)code
                self._incl = ' (incl. code)'
        if detail is not None:
            self._detail_ = detail
        if file is not None:  # and hasattr(file, 'write'):
            self._file_ = file
        if limit is not None:
            self._limit_ = limit
        if stats is not None:
            self._stats_ = s = int(stats)
            self._cutoff = (stats - s) * 100
            if s > 1:  # profile types
                self._profile = True
            else:
                self._profile = False

    def _get_duplicate(self):
        '''Number of duplicate objects.
        '''
        return self._duplicate
    duplicate = property(_get_duplicate, doc=_get_duplicate.__doc__)

    def _get_missed(self):
        '''Number of objects missed due to errors.
        '''
        return self._missed
    missed = property(_get_missed, doc=_get_missed.__doc__)

    def _get_total(self):
        '''Total size accumulated so far.
        '''
        return self._total
    total = property(_get_total, doc=_get_total.__doc__)

    def reset(self, align=8, all=False, clip=80, code=False,  # PYCHOK expected
                    derive=False, detail=0, file=None, ignored=True,
                    infer=False, limit=100, stats=0):
        '''Reset options, state, etc.

           The available options and default values are:

               align=8      -- size alignment
               all=False    -- all (GC) objects and referents
               clip=80      -- clip repr() strings
               code=False   -- incl. (byte)code size
               derive=False -- derive from super type
               detail=0     -- Asized refs level
               file=None    -- output stream for printing
               ignored=True -- ignore certain types
               infer=False  -- try to infer types
               limit=100    -- recursion limit
               stats=0.0    -- print stats and cutoff percentage

           See function  asizeof for a more detailed description
           of these options.
        '''
        # options
        self._align_  = align
        self._clip_   = clip
        self._code_   = code
        self._derive_ = derive
        self._detail_ = detail  # for Asized only
        self._file_   = file
        self._infer_  = infer
        self._limit_  = limit
        self._stats_  = stats
        if ignored:
            self._ign_d = _kind_ignored
        else:
            self._ign_d = None
        # clear state
        self._clear()
        self.set(align=align, all=all, code=code, stats=stats)


# public functions

def adict(*classes):
    '''Install one or more classes to be handled as dict.
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
    '''Return a tuple containing an  Asized instance for each
       object passed as positional argment using the following
       options.  See function  asizeof for a more detailed
       description.

           align=8      -- size alignment
           all=False    -- all (GC) objects and referents
           clip=80      -- clip repr() strings
           code=False   -- incl. (byte)code size
           derive=False -- derive from super type
           detail=0     -- Asized refs level
           file=None    -- output stream for printing
           ignored=True -- ignore certain types
           infer=False  -- try to infer types
           limit=100    -- recursion limit
           stats=0.0    -- print stats and cutoff percentage

       Set  detail to the desired referents level (recursion depth).

       If only one object is given, the return value is the
       Asized instance for that object.  Otherwise, the length
       of the returned tuple equals the number of given objects.
    '''
    t = _objs(objs, **opts)
    if t:
        _asizer.reset(**opts)
        s = _asizer.asized(*t)
        _asizer.print_stats(objs=t, opts=opts, sized=s)
        _asizer._clear()
    else:
        s = ()
    return s


def asizeof(*objs, **opts):
    '''Return the combined size in bytes of all objects passed
       as positional argments.

       The available options and defaults are the following.

            align=8      -- size alignment
            all=False    -- all (GC) objects and referents
            clip=80      -- clip ``repr()`` strings
            code=False   -- incl. (byte)code size
            derive=False -- derive from super type
            file=None    -- output stream for printing
            ignored=True -- ignore certain types
            infer=False  -- try to infer types
            limit=100    -- recursion limit
            stats=0.0    -- print stats and cutoff percentage

       Set  align to a power of 2 to align sizes.  Any value less
       than 2 avoids size alignment.

       All current GC objects are sized if  all is True and if no
       positional arguments are supplied.  Also, if  all is True
       all GC referents are used instead of the limited ones.

       A positive  clip value truncates all repr() strings to at
       most  clip characters.

       The (byte)code size of callable objects like functions,
       methods, classes, etc. is included only if  code is True.

       If  derive is True, new types are handled like an existing
       (super) type provided there is one and only of those.

       By default, certain base types like object are ignored for
       sizing.  Set  ignored to False to force all ignored types
       in the size of objects.

       Use option  file to specify an output stream for printing,
       different than the default  sys.stdout.

       By default certain base types like object, super, etc. are
       ignored.  Set  ignored to False to include those.

       If  infer is True, new types are inferred from attributes
       (only implemented for dict types on callable attributes
       as get, has_key, items, keys and values).

       Set  limit to a positive value to accumulate the sizes of
       the referents of each object, recursively up to the limit.
       Using  limit zero returns the sum of the flat [1] sizes of
       the given objects.  High  limit values may cause runtime
       errors and miss objects for sizing.

       A positive value for  stats prints up to 8 statistics, (1)
       a summary of the number of objects sized and seen, (2) a
       simple profile of the sized objects by type and (3+) up
       to 6 tables showing the static, dynamic, derived, ignored,
       inferred and dict types used, found respectively installed.

       The fractional part of the  stats value (x 100) is the
       cutoff percentage for simple profiles.  Objects below
       the cutoff value are not reported.

       [1] See the documentation of this module for the definition
           of flat size.
    '''
    t = _objs(objs, **opts)
    if t:
        _asizer.reset(**opts)
        s = _asizer.asizeof(*t)
        _asizer.print_stats(objs=t, opts=opts)
        _asizer._clear()
    else:
        s = 0
    return s


def asizesof(*objs, **opts):
    '''Return a tuple containing the size in bytes of all objects
       passed as positional argments using the following options.
       See function  asizeof for a more detailed description.

           align=8      -- size alignment
           all=False    -- all (GC) objects and referents
           clip=80      -- clip ``repr()`` strings
           code=False   -- incl. (byte)code size
           derive=False -- derive from super type
           file=None    -- output stream for printing
           ignored=True -- ignore certain types
           infer=False  -- try to infer types
           limit=100    -- recursion limit
           stats=0.0    -- print stats and cutoff percentage

       The length of the returned tuple equals the number of
       given objects.
    '''
    t = _objs(objs, **opts)
    if t:
        _asizer.reset(**opts)
        s = _asizer.asizesof(*t)
        _asizer.print_stats(objs=t, opts=opts, sizes=s)
        _asizer._clear()
    else:
        s = ()
    return s


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


def basicsize(obj, **opts):
    '''Return the basic size of an object (in bytes).

       Valid options and defaults are:

           derive=False -- derive type from super type
           infer=False  -- try to infer types
           save=False   -- save typedef if new
    '''
    v = _typedefof(obj, **opts)
    if v:
        v = v.base
    return v


def flatsize(obj, align=0, **opts):
    '''Return the flat size of an object (in bytes),
       optionally aligned to a given power of 2.

       See function  basicsize for a description of
       the other options.  See the documentation of
       this module for the definition of flat size.
    '''
    v = _typedefof(obj, **opts)
    if v:
        if align > 1:
            m = align - 1
            if (align & m) != 0:
                raise ValueError('invalid option: %s=%r' % ('align', align))
        else:
            m = 0
        v = v.flat(obj, m)
    return v


def itemsize(obj, **opts):
    '''Return the item size of an object (in bytes).

       See function  basicsize for a description of
       the options.
    '''
    v = _typedefof(obj, **opts)
    if v:
        v = v.item
    return v


def leng(obj, **opts):
    '''Return the length of an object (in items).

       See function  basicsize for a description
       of the options.
    '''
    v = _typedefof(obj, **opts)
    if v:
        v = v.leng
        if v and _callable(v):
            v = v(obj)
    return v


def refs(obj, all=False, **opts):
    '''Return (a generator for) specific referents of an
       object.

       If all is True return the GC referents.

       See function  basicsize for a description of the
       options.
    '''
    v = _typedefof(obj, **opts)
    if v:
        if all:  # == True
            v = _getreferents(obj)
        else:
            v = v.refs
            if v and _callable(v):
                v = v(obj, False)
    return v


if __name__ == '__main__':

    argv, MAX = sys.argv, sys.getrecursionlimit()

    def _print_asizeof(obj, infer=False, stats=0):
        a = [_repr(obj),]
        for d, c in ((0, False), (MAX, False), (MAX, True)):
            a.append(asizeof(obj, limit=d, code=c, infer=infer, stats=stats))
        _printf(" asizeof(%s) is %d, %d, %d", *a)

    def _print_functions(obj, name=None, align=8, detail=MAX, code=False, limit=MAX,
                              opt='', **unused):
        if name:
            _printf('%sasizeof functions for %s ... %s', linesep, name, opt)
        _printf('%s(): %s', ' basicsize', basicsize(obj))
        _printf('%s(): %s', ' itemsize',  itemsize(obj))
        _printf('%s(): %r', ' leng',      leng(obj))
        _printf('%s(): %s', ' refs',     _repr(refs(obj)))
        _printf('%s(): %s', ' flatsize',  flatsize(obj, align=align))  # , code=code
        _printf('%s(): %s', ' asized',           asized(obj, align=align, detail=detail, code=code, limit=limit))
#       _printf('%s(): %s', '.asized',   _asizer.asized(obj, align=align, detail=detail, code=code, limit=limit))

    def _bool(arg):
        a = arg.lower()
        if a in ('1', 't', 'y', 'true', 'yes', 'on'):
            return True
        elif a in ('0', 'f', 'n', 'false', 'no', 'off'):
            return False
        else:
            raise ValueError('bool option expected: %r' % arg)

    def _opts(*opts):
        '''Return True if any oof the given options
           was present in the command line arguments.
        '''
        for o in opts + ('-', '--'):
            if o in argv:
                return True
        return False

    _without = '-without' in argv

    if '-im' in argv or '-import' in argv:
        # import and size modules given as args

        def _aopts(argv, **opts):
            '''Get argv options as typed values.
            '''
            i = 1
            while argv[i].startswith('-'):
                k = argv[i].lstrip('-')
                if 'import'.startswith(k):
                    i += 1
                elif k in opts:
                    t = type(opts[k])
                    if t is bool:
                        t = _bool
                    i += 1
                    opts[k] = t(argv[i])
                    i += 1
                else:
                    raise NameError('invalid option: %s' % argv[i])
            return opts, i

        opts, i = _aopts(argv, align=8, clip=80, code=False, derive=False, detail=MAX, limit=MAX, stats=0)
        while i < len(argv):
            m, i = argv[i], i + 1
            if m == 'eval' and i < len(argv):
                o, i = eval(argv[i]), i + 1
            else:
                o = __import__(m)
            s = asizeof(o, **opts)
            _printf("%sasizeof(%s) is %d", linesep, _repr(o, opts['clip']), s)
            _print_functions(o, **opts)
        argv = []

    elif len(argv) < 2 or _opts('-h', '-help'):
        d = {'-all':               'all=True example',
             '-basic':             'basic examples',
             '-C':                 'Csizeof values',
             '-class':             'class and instance examples',
             '-code':              'code examples',
             '-dict':              'dict and UserDict examples',
#            '-gc':                'gc examples',
             '-gen[erator]':       'generator examples',
             '-glob[als]':         'globals examples, incl. asized()',
             '-h[elp]':            'print this information',
             '-im[port] <module>': 'imported module example',
             '-int | -long':       'int and long examples',
             '-iter[ator]':        'iterator examples',
             '-loc[als]':          'locals examples',
             '-pair[s]':           'key pair examples',
             '-slots':             'slots examples',
             '-stack':             'stack examples',
             '-sys':               'sys.modules examples',
             '-test [-without]':   'test flatsize() vs sys.getsizeof()',
             '-type[def]s':        'type definitions',
             '- | --':             'all examples'}
        if namedtuple:
            d['-named[tuple] [-without]'] = 'namedtuple example'
        w = -max([len(o) for o in _keys(d)])  # [] for Python 2.2
        t = _sorted(['%*s -- %s' % (w, o, t) for o, t in _items(d)])  # [] for Python 2.2
        t = '\n     '.join([''] + t)
        _printf('usage: %s <option> ...\n%s\n', argv[0], t)

    class C:
        pass

    class D(dict):
        _attr1 = None
        _attr2 = None

    class E(D):
        def __init__(self, a1=1, a2=2):  # PYCHOK OK
            self._attr1 = a1  # PYCHOK OK
            self._attr2 = a2  # PYCHOK OK

    class P(object):
        _p = None

        def _get_p(self):
            return self._p
        p = property(_get_p)  # PYCHOK OK

    class O:  # old style
        a = None
        b = None

    class S(object):  # new style
        __slots__ = ('a', 'b')

    class T(object):
        __slots__ = ('a', 'b')

        def __init__(self):
            self.a = self.b = 0

    if _opts('-all'):  # all=True example
        _printf('%sasizeof(limit=%s, code=%s, %s) ... %s', linesep, 'MAX', True, 'all=True', '-all')
        asizeof(limit=MAX, code=True, stats=MAX, all=True)

    if _opts('-basic'):  # basic examples
        _printf('%sasizeof(%s) for (limit, code) in %s ... %s', linesep, '<basic_objects>', '((0, False), (MAX, False), (MAX, True))', '-basic')
        for o in (None, True, False,
                  1.0, 1.0e100, 1024, 1000000000,
                  '', 'a', 'abcdefg',
                  {}, (), []):
            _print_asizeof(o, infer=True)

    if _opts('-C'):  # show all Csizeof values
        _sizeof_Cdouble  = calcsize('d')  # PYCHOK OK
        _sizeof_Csize_t  = calcsize('Z')  # PYCHOK OK
        _sizeof_Cssize_t = calcsize('z')  # PYCHOK OK
        t = [_ for _ in locals().items() if _[0].startswith('_sizeof_')]
        _printf('%s%d C sizes: (in bytes) ... -C', linesep, len(t))
        for n, v in _sorted(t):
            _printf(' sizeof(%s): %r', n[len('_sizeof_'):], v)

    if _opts('-class'):  # class and instance examples
        _printf('%sasizeof(%s) for (limit, code) in %s ... %s', linesep, '<non-callable>', '((0, False), (MAX, False), (MAX, True))', '-class')
        for o in (C(), C.__dict__,
                  D(), D.__dict__,
                  E(), E.__dict__,
                  P(), P.__dict__, P.p,
                  O(), O.__dict__,
                  S(), S.__dict__,
                  S(), S.__dict__,
                  T(), T.__dict__):
            _print_asizeof(o, infer=True)

    if _opts('-code'):  # code examples
        _printf('%sasizeof(%s) for (limit, code) in %s ... %s', linesep, '<callable>', '((0, False), (MAX, False), (MAX, True))', '-code')
        for o in (C, D, E, P, S, T,  # classes are callable
                  type,
                 _co_refs, _dict_refs, _inst_refs, _len_int, _seq_refs, lambda x: x,
                (_co_refs, _dict_refs, _inst_refs, _len_int, _seq_refs),
                 _typedefs):
            _print_asizeof(o)

    if _opts('-dict'):  # dict and UserDict examples
        _printf('%sasizeof(%s) for (limit, code) in %s ... %s', linesep, '<Dicts>', '((0, False), (MAX, False), (MAX, True))', '-dict')
        try:
            import UserDict  # no UserDict in 3.0
            for o in (UserDict.IterableUserDict(), UserDict.UserDict()):
                _print_asizeof(o)
        except ImportError:
            pass

        class _Dict(dict):
            pass

        for o in (dict(), _Dict(),
                  P.__dict__,  # dictproxy
                  Weakref.WeakKeyDictionary(), Weakref.WeakValueDictionary(),
                 _typedefs):
            _print_asizeof(o, infer=True)

#   if _opts('-gc'):  # gc examples
#       _printf('%sasizeof(limit=%s, code=%s, *%s) ...', linesep, 'MAX', False, 'gc.garbage')
#       from gc import collect, garbage  # list()
#       asizeof(limit=MAX, code=False, stats=1, *garbage)
#       collect()
#       asizeof(limit=MAX, code=False, stats=2, *garbage)

    if _opts('-gen', '-generator'):  # generator examples
        _printf('%sasizeof(%s, code=%s) ... %s', linesep, '<generator>', True, '-gen[erator]')

        def gen(x):
            i = 0
            while i < x:
                yield i
                i += 1
        a = gen(5)
        b = gen(50)
        asizeof(a, code=True, stats=1)
        asizeof(b, code=True, stats=1)
        asizeof(a, code=True, stats=1)

    if _opts('-glob', '-globals'):  # globals examples
        _printf('%sasizeof(%s, limit=%s, code=%s) ... %s', linesep, 'globals()', 'MAX', False, '-glob[als]')
        asizeof(globals(), limit=MAX, code=False, stats=1)
        _print_functions(globals(), 'globals()', opt='-glob[als]')

        _printf('%sasizesof(%s, limit=%s, code=%s) ... %s', linesep, 'globals(), locals()', 'MAX', False, '-glob[als]')
        asizesof(globals(), locals(), limit=MAX, code=False, stats=1)
        asized(globals(), align=0, detail=MAX, limit=MAX, code=False, stats=1)

    if _opts('-int', '-long'):  # int and long examples
        try:
            _L5d  = long(1) << 64
            _L17d = long(1) << 256
            t = '<int>/<long>'
        except NameError:
            _L5d  = 1 << 64
            _L17d = 1 << 256
            t = '<int>'

        _printf('%sasizeof(%s, align=%s, limit=%s) ... %s', linesep, t, 0, 0, '-int')
        for o in (1024, 1000000000,
                  1.0, 1.0e100, 1024, 1000000000,
                  MAX, 1 << 32, _L5d, -_L5d, _L17d, -_L17d):
            _printf(' asizeof(%s) is %s (%s + %s * %s)', _repr(o), asizeof(o, align=0, limit=0),
                                                         basicsize(o), leng(o), itemsize(o))

    if _opts('-iter', '-iterator'):  # iterator examples
        _printf('%sasizeof(%s, code=%s) ... %s', linesep, '<iterator>', False, '-iter[ator]')
        o = iter('0123456789')
        e = iter('')
        d = iter({})
        i = iter(_items({1:1}))
        k = iter(_keys({2:2, 3:3}))
        v = iter(_values({4:4, 5:5, 6:6}))
        l = iter([])
        t = iter(())
        asizesof(o, e, d, i, k, v, l, t, limit=0, code=False, stats=1)
        asizesof(o, e, d, i, k, v, l, t, limit=9, code=False, stats=1)

    if _opts('-loc', '-locals'):  # locals examples
        _printf('%sasizeof(%s, limit=%s, code=%s) ... %s', linesep, 'locals()', 'MAX', False, '-loc[als]')
        asizeof(locals(), limit=MAX, code=False, stats=1)
        _print_functions(locals(), 'locals()', opt='-loc[als]')

    if _opts('-named', '-namedtuple') and namedtuple:
        NtA = namedtuple('a', 'x')  # class-like
        NtB = namedtuple('b', 'x, y')  # class-like

        ntA = NtA(1)
        ntB = NtB(1, 2)
        assert _isnamedtuple(ntA) and _isnamedtuple(ntB)

        tA = (30000,)
        tB = (20000, 30000)

        listA = [NtA(i) for i in range(10000)]  # PYCHOK expected
        listB = [NtB(i, i+10000) for i in range(10000, 20000)]
        listC = [(i+20000) for i in range(10000)]

        g = _getsizeof
        if _without:
            _getsizeof = None  # zap _getsizeof for flatsize()
        for z, t in ((asizeof, 'asizeof'),
                     (flatsize, 'flatsize'),
                     (_getsizeof, 'sys.getsizeof')):
            if z:
                _printf('\n%s(%s) ...', t, 'namedtuple')
                _printf('  ntA = %s  tA = %s', z(ntA), z(tA))
                _printf('  ntB = %s  tB = %s', z(ntB), z(tB))
                _printf('listA = %s', z(listA))
                _printf('listB = %s', z(listB))
                _printf('listC = %s  30000 = %s', z(listC), z(30000))
            else:
                _printf('\n%s(%s) N/A', t, 'namedtuple')
        _getsizeof = g
        del NtA, ntA, tA, NtB, ntB, tB, listA, listB, listC, z, t

    if _opts('-pair', '-pairs'):  # key pair examples
        # <http://jjinux.blogspot.com/2008/08/python-memory-conservation-tip.html>
        _printf('%sasizeof(%s) vs asizeof(%s) ... %s', linesep, 'dict[i][j]', 'dict[(i,j)]', '-pair[s]')
        n = m = 200

        p = {}  # [i][j]
        for i in range(n):
            q = {}
            for j in range(m):
                q[j] = None
            p[i] = q
        p = asizeof(p, stats=1)

        t = {}  # [(i,j)]
        for i in range(n):
            for j in range(m):
                t[(i,j)] = None
        t = asizeof(t, stats=1)

        _printf('%sasizeof(dict[i][j]) is %s of asizeof(dict[(i,j)])', linesep, _p100(p, t))

    if _opts('-slots'):  # slots examples
        _printf('%sasizeof(%s, code=%s) ... %s', linesep, '<__slots__>', False, '-slots')

        class Old:
            pass  # m = None

        class New(object):
            __slots__ = ('n',)

        class Sub(New):  # PYCHOK OK
            __slots__ = {'s': ''}  # duplicate!
            def __init__(self):  # PYCHOK OK
                New.__init__(self)

        # basic instance sizes
        o, n, s = Old(), New(), Sub()
        asizesof(o, n, s, limit=MAX, code=False, stats=1)
        # with unique min attr size
        o.o = 'o'
        n.n = 'n'
        s.n = 'S'
        s.s = 's'
        asizesof(o, n, s, limit=MAX, code=False, stats=1)
        # with duplicate, intern'ed, 1-char string attrs
        o.o = 'x'
        n.n = 'x'
        s.n = 'x'
        s.s = 'x'
        asizesof(o, n, s, 'x', limit=MAX, code=False, stats=1)
        # with larger attr size
        o.o = 'o'*1000
        n.n = 'n'*1000
        s.n = 'n'*1000
        s.s = 's'*1000
        asizesof(o, n, s, 'x'*1000, limit=MAX, code=False, stats=1)

    if _opts('-stack'):  # stack examples
        _printf('%sasizeof(%s, limit=%s, code=%s) ... %s', linesep, 'stack(MAX)', 'MAX', False, '')
        asizeof(stack(MAX), limit=MAX, code=False, stats=1)
        _print_functions(stack(MAX), 'stack(MAX)', opt='-stack')

    if _opts('-sys'):  # sys.modules examples
        _printf('%sasizeof(limit=%s, code=%s, *%s) ... %s', linesep, 'MAX', False, 'sys.modules.values()', '-sys')
        asizeof(limit=MAX, code=False, stats=1, *sys.modules.values())
        _print_functions(sys.modules, 'sys.modules', opt='-sys')

    if _opts('-type', '-types', '-typedefs'):  # show all basic _typedefs
        t = len(_typedefs)
        w = len(str(t)) * ' '
        _printf('%s%d type definitions: basic- and itemsize (leng), kind ... %s', linesep, t, '-type[def]s')
        for k, v in _sorted([(_prepr(k), v) for k, v in _items(_typedefs)]):  # [] for Python 2.2 # PYCHOK OK
            s = '%(base)s and %(item)s%(leng)s, %(kind)s%(code)s' % v.format()
            _printf('%s %s: %s', w, k, s)

    if _opts('-test'):
        # compare the results of flatsize() *without* or *with* using
        # sys.getsizeof() with the accurate sizes from sys.getsizeof()
        # but expect differences for sequences as dicts, lists, sets,
        # tuples, etc.  while this is no proof for the accuracy of
        # flatsize() on Python2 builds without sys.getsizeof(), it does
        # show that flatsize() produces reasonable and usable results
        _printf('%sflatsize() vs sys.getsizeof() ... %s', linesep, '-test')
        t, g, e = [], _getsizeof, 0
        if g:
            for v in _values(_typedefs):
                t.append(v.type)
                try:  # creating one instance
                    if v.type.__module__ not in ('io',):  # avoid 3.0 RuntimeWarning
                        t.append(v.type())
                except (AttributeError, RuntimeError, SystemError, TypeError, ValueError):  # ignore errors
                    pass
            t.extend(({1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8},
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      ['1', '2', '3'], [0] * 100,
                      '12345678',
                      'x' * 1001,
                      (1, 2, 3, 4, 5, 6, 7, 8),
                      ('1', '2', '3'),
                      (0,) * 100,
                      _Slots((1, 2, 3, 4, 5, 6, 7, 8)),
                      _Slots(('1', '2', '3')),
                      _Slots((0,) * 100),
                      0,
                      1 << 8,
                      1 << 16,
                      1 << 32,
                      1 << 64,
                      1 << 128,
                      complex(0, 1),
                      True, False))
            if _without:
                _getsizeof = None  # zap _getsizeof for flatsize()
            for o in t:
                a = flatsize(o)
                s = sys.getsizeof(o, 0)  # 0 as default # PYCHOK expected
                if a != s:
                    # flatsize approximates the length of sequences
                    # (sys.getsizeof(bool) on 3.0b3 is not correct)
                    if type(o) in (dict, list, set, frozenset, tuple) or (
                       type(o) in (bool,) and sys.version_info[0] == 3):
                        x = 'expected failure'
                    else:
                        x = 'FAILED %r' % _typedefof(o)
                        e += 1
                else:
                    x = 'passed'
                _printf('flatsize() %s vs sys.getsizeof() %s for %s: %s, %s',
                         a, s, _nameof(type(o)), _repr(o), x)
            _getsizeof = g  # restore
        n = len(t)

        # double check that classes with __slots__
        # are sub-classes of new style object class
        for c, o in globals().copy().items():
            if isclass(o) and hasattr(o, '__slots__'):
                n += 1
                if not _issubclass(o, object):  # in o.__bases__
                    _printf('%s.%s FAILED: no (%s) base', c, '__slots__', 'object')
                    e += 1

        p = 'Python %s' % sys.version.split()[0]
        if e:
            _printf('%s%d of %d tests failed or %s on %s', linesep, e, n, _p100(e, n), p)
        elif g:
            _printf('no unexpected failures in %d tests on %s', n, p)
        else:
            _printf('no sys.%s() in this %s', 'getsizeof', p)


# License file from an earlier version of this source file follows:

# --------------------------------------------------------------------
#       Copyright (c) 2002-2009 -- ProphICy Semiconductor, Inc.
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
