# First, as a demo, we'll demonstrate the idiom with a list:

# Code here that creates a list 'my_list'
if not my_list:
    # Code here for the case where the list is empty
else:
    # Code here for the case where the list is NOT empty


# Now, we'll demonstrate how to do the same thing for iterators:
# (note that this must be an ITERATOR, not an ITERABLE. So
# it won't work correctly if 'my_iter' is of type list, but
# works fine if we use 'my_iter = iter(list)'. For more on the
# distinction between iterators and iterables, see the docs.

import itertools

# code here that creates an iterator 'my_iter'
try:
    first = my_iter.next()
except StopIteration:
    # Code here for the case where the iterator is empty
else:
    my_iter = itertools.chain([first], my_iter)
    # Code here for the case where the iterator is NOT empty
