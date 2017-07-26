"""
object_snoop allows user to observe how Python expressions and statements are
translated into special method calls. object_snoop defines most special methods.
It simple print a trace and returns a fixed but sensible result. Users are
invited to build complex expressions to experiment how Python special methods work.

Reference:

Data model - Python v2.7 documentation
http://docs.python.org/reference/datamodel.html
"""

import inspect


class object_snoop(object):

    def __init__(self, name, truth=True):
        self.name = name
        self.truth = bool(truth)

    def __repr__(self):
        return '<%s>' % self.name

    # let __str__ and __unicode__ fallback to __repr__

    def trace(self, *args, **kwargs):
        """
        helper method to print "<name>.<func> [: <args> <kwargs>]"
        """
        caller_frame = inspect.stack()[1]
        caller_name = caller_frame[3]

        _name, _caller = self.name, caller_name
        _colon = _args = _kwargs = ""

        if args or kwargs:
            _colon = ' :'

        if len(args) == 1:
            _args = ' ' + str(args[0])
        elif args:
            _args = ' ' + str(args)

        if kwargs:
            _kwargs = ' ' + str(kwargs)

        print ("%(_name)s.%(_caller)s%(_colon)s%(_args)s%(_kwargs)s" % locals())


    # ------------------------------------------------------------------------
    # 1. Basic customization

    # Called when the instance is about to be destroyed
    def __del__(self): self.trace()

    # These are the so-called "rich comparison" methods,
    def __lt__(self, other): self.trace(other); return self.truth
    def __le__(self, other): self.trace(other); return self.truth
    def __eq__(self, other): self.trace(other); return self.truth
    def __ne__(self, other): self.trace(other); return self.truth
    def __gt__(self, other): self.trace(other); return self.truth
    def __ge__(self, other): self.trace(other); return self.truth

    # Called by comparison operations if rich comparison (see above) is not defined.
    def __cmp__(self, other):
        self.trace(other)
        return 1

    # Called by built-in function hash() and for operations on members of hashed collections
    def __hash__(self):
        self.trace()
        return 1

    # Called to implement truth value testing and the built-in operation bool()
    def __nonzero__(self):
        self.trace()
        return self.truth


    # ------------------------------------------------------------------------
    # 2. Customizing attribute access

    def __getattr__(self, name):
        self.trace(name)
        return 1

    def __setattr__(self, name, value):
        super(object_snoop,self).__setattr__(name, value)
        self.trace(name, value)

    def __delattr__(self, name):
        super(object_snoop,self).__delattr__(name)
        self.trace(name)


    # ------------------------------------------------------------------------
    # 4. Customizing instance and subclass checks


    # ------------------------------------------------------------------------
    # 5. Emulating callable objects

    def __call__(self, *args, **kwargs):
        self.trace(*args, **kwargs)


    # ------------------------------------------------------------------------
    # 6. Emulating container types

    def __len__     (self):             self.trace()            ; return 1
    def __getitem__ (self, key):        self.trace(key)         ; return 1
    def __setitem__ (self, key, value): self.trace(key, value)
    def __delitem__ (self, key):        self.trace(key)
    def __iter__    (self):             self.trace()            ; return iter([])
    def __reversed__(self):             self.trace()            ; return iter([])
    def __contains__(self, item):       self.trace(item)        ; return self.truth


    # ------------------------------------------------------------------------
    # 7. Additional methods for emulation of sequence types

    # Deprecated since version 2.0
    def __getslice__(self, i, j):           self.trace(i,j)         ; return self

    def __setslice__(self, i, j, sequence): self.trace(i,j,sequence)
    def __delslice__(self, i, j):           self.trace(i,j)


    # ------------------------------------------------------------------------
    # 8. Emulating numeric types

    # These methods are called to implement the binary arithmetic operations (+,
    # -, *, //, %, divmod(), pow(), **, <<, >>, &, ^, |).
    def __add__     (self, other): self.trace(other); return self
    def __sub__     (self, other): self.trace(other); return self
    def __mul__     (self, other): self.trace(other); return self
    def __floordiv__(self, other): self.trace(other); return self
    def __mod__     (self, other): self.trace(other); return self
    def __divmod__  (self, other): self.trace(other); return self
    def __pow__     (self, other): self.trace(other); return self
    def __lshift__  (self, other): self.trace(other); return self
    def __rshift__  (self, other): self.trace(other); return self
    def __and__     (self, other): self.trace(other); return self
    def __xor__     (self, other): self.trace(other); return self
    def __or__      (self, other): self.trace(other); return self
    def __div__     (self, other): self.trace(other); return self
    def __truediv__ (self, other): self.trace(other); return self


    # These methods are called to implement the binary arithmetic operations
    # with reflected (swapped) operands.
    def __radd__     (self, other): self.trace(other); return self
    def __rsub__     (self, other): self.trace(other); return self
    def __rmul__     (self, other): self.trace(other); return self
    def __rdiv__     (self, other): self.trace(other); return self
    def __rtruediv__ (self, other): self.trace(other); return self
    def __rfloordiv__(self, other): self.trace(other); return self
    def __rmod__     (self, other): self.trace(other); return self
    def __rdivmod__  (self, other): self.trace(other); return self
    def __rpow__     (self, other): self.trace(other); return self
    def __rlshift__  (self, other): self.trace(other); return self
    def __rrshift__  (self, other): self.trace(other); return self
    def __rand__     (self, other): self.trace(other); return self
    def __rxor__     (self, other): self.trace(other); return self
    def __ror__      (self, other): self.trace(other); return self


    # These methods are called to implement the augmented arithmetic assignments
    # (+=, -=, *=, /=, //=, %=, **=, <<=, >>=, &=, ^=, |=).
    def __iadd__     (self, other): self.trace(other); return self
    def __isub__     (self, other): self.trace(other); return self
    def __imul__     (self, other): self.trace(other); return self
    def __idiv__     (self, other): self.trace(other); return self
    def __itruediv__ (self, other): self.trace(other); return self
    def __ifloordiv__(self, other): self.trace(other); return self
    def __imod__     (self, other): self.trace(other); return self
    def __ipow__     (self, other): self.trace(other); return self
    def __ilshift__  (self, other): self.trace(other); return self
    def __irshift__  (self, other): self.trace(other); return self
    def __iand__     (self, other): self.trace(other); return self
    def __ixor__     (self, other): self.trace(other); return self
    def __ior__      (self, other): self.trace(other); return self


    # Called to implement the unary arithmetic operations (-, +, abs() and ~).
    def __neg__   (self): self.trace(); return self
    def __pos__   (self): self.trace(); return self
    def __abs__   (self): self.trace(); return self
    def __invert__(self): self.trace(); return self

    # Called to implement the built-in functions complex(), int(), long(), and float(), oct() and hex().
    def __complex__(self): self.trace(); return 1
    def __int__    (self): self.trace(); return 1
    def __long__   (self): self.trace(); return 1
    def __float__  (self): self.trace(); return 1.0
    def __oct__    (self): self.trace(); return 'o'
    def __hex__    (self): self.trace(); return 'x'

    # Called to implement operator.index().
    def __index__  (self): self.trace(); return self

    # Called to implement "mixed-mode" numeric arithmetic.
    def __coerce__(self, other): self.trace(other); return self


# define two dummy objects. r evaluates to True and s evaluates to False.
r = object_snoop('r', True)
s = object_snoop('s', False)
