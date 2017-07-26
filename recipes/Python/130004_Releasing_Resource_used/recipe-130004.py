Python 2.2.1 (#34, Apr  9 2002, 19:34:33) [MSC 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from __future__ import generators
>>> def g():
...     for i in range(5):
...             yield i
...
>>> for x in g():
...     print x
...
0
1
2
3
4
>>> def acquireResource():
...     print 'Resource Acquired'
...
>>> def releaseResource():
...     print 'Resource Released'
...
>>> class GeneratorWrapper:
...     def __init__(self, generator):
...             self.generator = generator
...             acquireResource()
...     def __del__(self):
...             releaseResource()
...     def __iter__(self):
...             return self
...     def next(self):
...             return self.generator.next()
...
>>> def testNormalUse():
...     w = GeneratorWrapper(g())
...     for x in w:
...             print x
...
>>> testNormalUse()
Resource Acquired
0
1
2
3
4
Resource Released
>>> def testAbortedUse():
...     w = GeneratorWrapper(g())
...     for x in w:
...             print x
...             if x > 2:
...                     return
...
>>> testAbortedUse()
Resource Acquired
0
1
2
3
Resource Released
>>>
