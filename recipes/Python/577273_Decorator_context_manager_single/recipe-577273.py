# (c) Michael Foord, 2010
# http://voidspace.org.uk/blog
'''
Create objects that act as both context managers *and* as decorators, and behave the same in both cases.

Works with Python 2.4 - 2.7 and Python 3. The tests require unittest2 or Python 3.2 to run.

Example:

from contextdecorator import ContextDecorator

class mycontext(ContextDecorator):

    def __init__(self, *args):
        """Normal initialiser"""

    def before(self):
        """
        Called on entering the with block or starting the decorated function.
        
        If used in a with statement whatever this method returns will be the
        context manager.
        """
    
    def after(self, *exc):
        """
        Called on exit. Arguments and return value of this method have
        the same meaning as the __exit__ method of a normal context
        manager.
        """

@mycontext('some', 'args')
def function():
    pass

with mycontext('some', 'args') as something:
    pass

See the tests for more usage examples.
'''

# Only needed for tests
from __future__ import with_statement

import sys

try:
    from functools import wraps
except ImportError:
    # Python 2.4 compatibility
    def wraps(original):
        def inner(f):
            f.__name__ = original.__name__
            return f
        return inner

# horrible reraise code for compatibility
# with Python 2 & 3
if sys.version_info >= (3,0):
    exec ("""
def _reraise(cls, val, tb):
    raise val
""")
else:
    exec ("""
def _reraise(cls, val, tb):
    raise cls, val, tb
""")


EXC = (None, None, None)

class ContextDecorator(object):
    before = None
    after = None
        
    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kw):
            if self.before is not None:
                self.before()
            
            exc = EXC
            try:
                result = f(*args, **kw)
            except Exception:
                exc = sys.exc_info()
            
            catch = False
            if self.after is not None:
                catch = self.after(*exc)
            
            if not catch and exc is not EXC:
                _reraise(*exc)
            return result
        return inner
            
    def __enter__(self):
        if self.before is not None:
            return self.before()
    
    def __exit__(self, *exc):
        catch = False
        if self.after is not None:
            catch = self.after(*exc)
        return catch


if __name__ == '__main__':
    import sys

    if sys.version_info >= (3, 2):
        import unittest as unittest2
    else:
        import unittest2
    
    class mycontext(ContextDecorator):
        started = False
        exc = None
        catch = False
    
        def before(self):
            self.started = True
            return self
    
        def after(self, *exc):
            self.exc = exc
            return self.catch


    class TestContext(unittest2.TestCase):

        def test_context(self):
            context = mycontext()
            with context as result:
                self.assertIs(result, context)
                self.assertTrue(context.started)
            
            self.assertEqual(context.exc, (None, None, None))
    
        def test_context_with_exception(self):
            context = mycontext()
        
            with self.assertRaisesRegexp(NameError, 'foo'):
                with context:
                    raise NameError('foo')
        
            context.exc = (None, None, None)
            context.catch = True
            with context:
                raise NameError('foo')
            self.assertNotEqual(context.exc, (None, None, None))
        
        def test_decorator(self):
            context = mycontext()
        
            @context
            def test():
                self.assertIsNone(context.exc)
                self.assertTrue(context.started)
            test()
            self.assertEqual(context.exc, (None, None, None))
    
        def test_decorator_with_exception(self):
            context = mycontext()
        
            @context
            def test():
                self.assertIsNone(context.exc)
                self.assertTrue(context.started)
                raise NameError('foo')
        
            with self.assertRaisesRegexp(NameError, 'foo'):
                test()
            self.assertNotEqual(context.exc, (None, None, None))

        def test_decorating_method(self):
            context = mycontext()
        
            class Test(object):
            
                @context
                def method(self, a, b, c=None):
                    self.a = a
                    self.b = b
                    self.c = c
        
            test = Test()
            test.method(1, 2)
            self.assertEqual(test.a, 1)
            self.assertEqual(test.b, 2)
            self.assertEqual(test.c, None)

            test.method('a', 'b', 'c')
            self.assertEqual(test.a, 'a')
            self.assertEqual(test.b, 'b')
            self.assertEqual(test.c, 'c')

    unittest2.main()
