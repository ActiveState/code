def tested(fun=None, pre=None, post=None, verbose=False, globs=None):
    ''' 
        >>> def my_pre(): print "this will be printed before running tests"
        ... 
        >>> def my_post(): print "this will be printed after running tests"
        ... 
        >>> @tested(pre=my_pre, post=my_post, verbose=True)
        ... def foo():
        ...     """ 
        ...         >>> foo()
        ...         True
        ...     """
        ...     return True
        >>> foo.test()
        this will be printed before running tests
        Finding tests in foo
        Trying:
            foo()
        Expecting:
            True
        ok
        this will be printed after running tests
    '''
    from sys import _getframe
    from doctest import run_docstring_examples
    
    if globs is None:
        globs = _getframe(1).f_locals
    if fun:
        def test():
            if callable(pre):
                pre()
            run_docstring_examples(fun, globs=globs, verbose=verbose, name=fun.__name__)
            if callable(post):
                post()
        fun.test = test
        return fun
    else:
        return lambda fun: tested(fun, pre=pre, post=post, verbose=verbose, globs=globs)
tested = tested(tested, verbose=True)
