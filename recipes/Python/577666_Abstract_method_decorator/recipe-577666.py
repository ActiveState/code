def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__
    
    return default_abstract_method


if __name__ == '__main__':

    class A:
        @abstractmethod
        def foo(self, data): pass

    class B(A):
        def foo(self, data):
            self.data = data

    a = A()
    b = B()
    b.foo(5)
    
    exception_raised = False
    try:
        a.foo(3)
    except NotImplementedError:
        exception_raised = True

    assert exception_raised

    print 'OK'
