"""Act as a proxy for the Foo instance in this thread's context."""

from ThreadLocalStorage import currentContext


class FooProxy:

    """Act as a proxy for the Foo instance in this thread's context.
    
    This is based on the ThreadLocalStorage module.
    
    """

    def __getattr__(self, attr):
        return getattr(currentContext().foo, attr)

    def __setattr__(self, attr, value):
        setattr(currentContext().foo, attr, value)
