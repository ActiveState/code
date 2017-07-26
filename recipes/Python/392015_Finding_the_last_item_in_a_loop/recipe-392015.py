"""
Example (and doctest):

>>> for n, islast in iter_islast(range(4)):
...   if islast:
...       print "last but not least:",
...   print n
... 
0
1
2
last but not least: 3

>>> list(iter_islast(''))
[]
>>> list(iter_islast('1'))
[('1', True)]
>>> list(iter_islast('12'))
[('1', False), ('2', True)]
>>> list(iter_islast('123'))
[('1', False), ('2', False), ('3', True)]
>>>
"""

def iter_islast(iterable):
    """ iter_islast(iterable) -> generates (item, islast) pairs

Generates pairs where the first element is an item from the iterable
source and the second element is a boolean flag indicating if it is the
last item in the sequence.
"""

    it = iter(iterable)
    prev = it.next()
    for item in it:
        yield prev, False
        prev = item
    yield prev, True
