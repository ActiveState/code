## Decorator and context manager from a single API  
Originally published: 2010-06-25 17:16:54  
Last updated: 2010-06-27 15:15:01  
Author: Michael Foord  
  
Create objects that act as both context managers *and* as decorators, and behave the same in both cases.

Works with Python 2.4 - 2.7 and Python 3. The tests require unittest2 or Python 3.2 to run. (And because the tests use the with statement they won't work with Python 2.4.)

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

Both before and after methods are optional (but providing neither is somewhat pointless). See the tests for more usage examples.