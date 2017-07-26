'''Bunch utility class.

Developed at ESSS (http://esss.com.br) and provided under the MIT license.

@author: Bruno Oliveira 
@author: Fabio Zadrozny

Based on implementation by Alex Martelli (http://mail.python.org/pipermail
/python-list/2002-July/112007.html).

To use:

class Point(Bunch):
    x = 0
    y = 0

p0 = Point()
assert p0.x == 0
assert p0.y == 0

p1 = Point(x=10, y=20)
assert p1.x == 10
assert p1.y == 20

'''

import copy
from types import NoneType

#===============================================================================
# MetaBunch
#===============================================================================
class MetaBunch(type):
    """
    metaclass for new and improved "Bunch": implicitly defines 
    __slots__, __init__ and __repr__ from variables bound in class scope.

    An instance of metaMetaBunch (a class whose metaclass is metaMetaBunch)
    defines only class-scope variables (and possibly special methods, but
    NOT __init__ and __repr__!).  metaMetaBunch removes those variables from
    class scope, snuggles them instead as items in a class-scope dict named
    __defaults__, and puts in the class a __slots__ listing those variables'
    names, an __init__ that takes as optional keyword arguments each of
    them (using the values in __defaults__ as defaults for missing ones), and
    a __repr__ that shows the repr of each attribute that differs from its
    default value (the output of __repr__ can be passed to __eval__ to make
    an equal instance, as per the usual convention in the matter).
    """

    def __new__(cls, classname, bases, classdict):
        """ Everything needs to be done in __new__, since type.__new__ is
            where __slots__ are taken into account.
        """
        import inspect

        # define as local functions the __init__ and __repr__ that we'll
        # use in the new class

        def __init__(self, **kw):
            """ Simplistic __init__: first set all attributes to default
                values, then override those explicitly passed in kw.
            """
            for k, (value, copy_op) in self.__defaults__.iteritems():
                if k not in kw: #No need to set value to be overridden later on.
                    if copy_op is None:
                        #No copy op (immutable value)
                        setattr(self, k, value)
                    else:
                        setattr(self, k, copy_op(value))
            for k, value in kw.iteritems():
                setattr(self, k, value)

        def __repr__(self):
            """ 
            repr operator.
            """
            rep = ['%s=%r' % (k, getattr(self, k))
                for k in sorted(self.__defaults__)]
            return '%s(%s)' % (classname, ', '.join(rep))


        def __eq__(self, other):
            '''Basic __eq__.
            '''
            if not isinstance(other, type(self)):
                return False
            for attr in self.__defaults__:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True

        def __ne__(self, other):
            return not self == other

        # build the newdict that we'll use as class-dict for the new class
        newdict = dict(
            __slots__=classdict.pop('__slots__', []),
            __defaults__={},
            __init__=__init__,
            __repr__=__repr__,
            __eq__=__eq__,
            __ne__=__ne__,
        )

        # update the dafaults dict with the contents of the bases's defaults, so
        # they're properly initialized during __init__
        for base in bases:
            newdict['__defaults__'].update(getattr(base, '__defaults__', {}))


        for k, value in classdict.iteritems():
            if k.startswith('__') or inspect.isfunction(value) or \
                type(value) is property:
                # methods: copy to newdict
                newdict[k] = value
            else:
                # class variables, store name in __slots__ and name and
                # value as an item in __defaults__

                #Default for each value is deepcopy, but we may optimize that
                #(if the copy op is None, the value is considered immutable).
                copy_op = copy.deepcopy

                if value.__class__ in (
                    bool, int, float, long, str, NoneType
                    ):
                    copy_op = None
                else:
                    if value.__class__ in (tuple, frozenset):
                        if not value:
                            copy_op = None

                    if value.__class__ in (list, set, dict):
                        if not value:
                            copy_op = copy.copy


                newdict['__slots__'].append(k)
                newdict['__defaults__'][k] = (value, copy_op)

        # finally delegate the rest of the work to type.__new__
        return type.__new__(cls, classname, bases, newdict)



#===============================================================================
# Bunch
#===============================================================================
class Bunch(object):
    """ For convenience: inheriting from Bunch can be used to get
        the new metaclass (same as defining __metaclass__ yourself).
    """
    __metaclass__ = MetaBunch



#===============================================================================
# main
#===============================================================================
if __name__ == '__main__':
    class Point(Bunch):
        x = 0
        y = 0

    p0 = Point()
    assert p0.x == 0
    assert p0.y == 0

    p1 = Point(x=10, y=20)
    assert p1.x == 10
    assert p1.y == 20
