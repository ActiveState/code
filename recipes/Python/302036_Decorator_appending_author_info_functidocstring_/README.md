## Decorator for appending author info to the function docstring (Python 2.4)  
Originally published: 2004-08-26 01:17:58  
Last updated: 2004-08-26 01:17:58  
Author: Dmitry Vasiliev  
  
Some examples:

<pre>
>>> @author("John")
... @author("Paul")
... def test():
...     "Test function"
...
>>> help(test)
Help on function test in module __main__:

test()
    Author: John
    Author: Paul
    Test function
</pre>