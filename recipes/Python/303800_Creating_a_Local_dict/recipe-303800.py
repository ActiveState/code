#####################################
# locals.py
# Author: Derrick Wallace
#####################################
import sys

__all__ = ['local_dict']
bad = ['__init__', '__new__', '__repr__']


class __dict( dict ):
    """
    Wrapper to mimic a local dict.
    """

    def __init__( self, *args ):
        dict.__init__( self, *args )

        for attr in dict.__dict__:
            if callable( dict.__dict__[attr] ) and ( not attr in bad ):
                exec( 'def %s(self, *args): return dict.%s(sys._getframe(1).f_locals, *args)'%( attr, attr ) )
                exec( '__dict.%s = %s'%( attr, attr ) )

    # Must implement a custom repr to prevent recursion
    def __repr__( self, *args ):
        if sys._getframe(1).f_code == sys._getframe().f_code:
            return '{...}'
        return dict.__repr__( sys._getframe(1).f_locals, *args )


local_dict = __dict()


## Example Use ####################################

>>> from forum.locals import local_dict as __dict__
>>> __dict__
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__dict__': {...}}
>>> __dict__['foo'] = 'bar'
>>> foo
'bar'
>>> def Test(a, b=2):
...     print __dict__
...
>>> Test(1)
{'a': 1, 'b': 2}
>>> class Spam:
...     def Test(self, a, b=2):
...         print __dict__
...
>>> s=Spam()
>>> s.Test(100)
{'a': 100, 'self': <__main__.Spam instance at 0x008FD120>, 'b': 2}
>>>
