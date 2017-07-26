## Counting decorator  
Originally published: 2011-01-07 11:22:55  
Last updated: 2011-01-07 11:22:55  
Author: Noufal Ibrahim  
  
To be used as a decorator for a function that will maintain the number of times it was called. 
Here is an example use. 

    >>> def test():
    ...    print "Hello"
    ... 
    >>> test = counter(test)
    >>> test()
    Hello
    >>> test()
    Hello
    >>> test()
    Hello
    >>> test()
    Hello
    >>> test()
    Hello
    >>> test.invocations
    5
    >>> test()
    Hello
    >>> test.invocations
    6
    >>> 
