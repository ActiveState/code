# Example from PEP 265 - Sorting Dictionaries By Value
#    Counting occurences of letters

d = {'a':2, 'b':23, 'c':5, 'd':17, 'e':1}

# operator.itemgetter is new in Python 2.4
#  `itemgetter(index)(container)` is equivalent to `container[index]`
from operator import itemgetter

# Items sorted by key
#   The new builtin `sorted()` will return a sorted copy of the input iterable.
print sorted(d.items())

# Items sorted by key, in reverse order
#   The keyword argument `reverse` operates as one might expect
print sorted(d.items(), reverse=True)

# Items sorted by value
#    The keyword argument `key` allows easy selection of sorting criteria
print sorted(d.items(), key=itemgetter(1))

# In-place sort still works, and also has the same new features as sorted
items = d.items()
items.sort(key = itemgetter(1), reverse=True)
print items
