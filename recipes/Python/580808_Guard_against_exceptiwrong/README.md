## Guard against an exception in the wrong place  
Originally published: 2017-06-25 17:07:34  
Last updated: 2017-06-25 17:17:43  
Author: Steven D'Aprano  
  
Sometimes exception handling can obscure bugs unless you guard against a particular exception occurring in a certain place. One example is that [accidentally raising `StopIteration` inside a generator](https://www.python.org/dev/peps/pep-0479/) will halt the generator instead of displaying a traceback. That was solved by PEP 479, which automatically has such `StopIteration` exceptions change to `RuntimeError`. See the discussion below for further examples.

Here is a class which can be used as either a decorator or context manager for guarding against the given exceptions. It takes an exception (or a tuple of exceptions) as argument, and if the wrapped code raises that exception, it is re-raised as another exception type (by default `RuntimeError`).

For example:

    try:
        with exception_guard(ZeroDivisionError):
            1/0  # raises ZeroDivisionError
    except RuntimeError:
        print ('ZeroDivisionError replaced by RuntimeError')
    
    
    @exception_guard(KeyError)
    def demo():
        return {}['key']  # raises KeyError
    
    try:
        demo()
    except RuntimeError:
        print ('KeyError replaced by RuntimeError')

