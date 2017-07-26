from functools import reduce
from collections import deque
from operator import getitem, setitem

def nested_enumerate(lst):
    """An analogue of enumerate for nested lists. 

       Returns an iterator over the (index, element) pairs of `lst` where 
       `index` is a list of integers [x0, x1,.., xn] such that 
       `lst[x0][x1]...[xn]==element`

       
       >>> for i, e in nested_enumerate([0, [[[1, [2, [[[3]]]]]]], [[[4]]]]):
               print('%s %s'%(str(i), str(e)))
       [0] 0
       [1, 0, 0, 0] 1
       [1, 0, 0, 1, 0] 2
       [1, 0, 0, 1, 1, 0, 0, 0] 3
       [2, 0, 0, 0] 4
    """
    
    # initial, partial index of lst
    partial_index = deque([([i], e) for (i, e) in enumerate(lst)])
      
    while partial_index:
        index, obj = partial_index.popleft()
        if isinstance(obj, list):
            # if obj is a list then its elements require further indexing
            new_dimension = [(index+[i], e) for (i, e) in enumerate(obj)]
            partial_index.extendleft(reversed(new_dimension)) 
        else:
            # obj is fully indexed
            yield index, obj


# complementary functions #

def nested_getitem(lst, index):
    """Returns lst[index[0]]...[index[n]]"""
    return reduce(getitem, index, lst)


def nested_setitem(lst, index, value):
    """Equivalent to the statement lst[index[0]]...[index[n]]=value"""
    setitem(
        reduce(getitem, index[0:-1], lst), index[-1], value
    )


# quick test #

deeplist = [0, [[[1, [2, [[[3]]]]]]], [[[4]]]]

for index, element in nested_enumerate(deeplist):
    assert nested_getitem(deeplist, index)==element

# example usage: applying a function to each element in a nested list #

square = lambda x: x**2

for index, element in nested_enumerate(deeplist):
    nested_setitem(deeplist, index, square(element))

assert deeplist==[0, [[[1, [4, [[[9]]]]]]], [[[16]]]]

# not recommended, but demonstrates different ways of traversing a list
# (plus, we all love flatten, right? ;-)

def flatten(lst):
    return [e for (i, e) in nested_enumerate(lst)]

def flatten2(lst):
    return [nested_getitem(lst, i) for (i, e) in nested_enumerate(lst)]

assert flatten(deeplist)==flatten2(deeplist)==[0, 1, 4, 9, 16]

# sort elements based on their depth of nesting, with deepest first
depthfirst = [e for (i, e) in sorted(nested_enumerate(deeplist), key=lambda (i, e):-len(i))]

assert depthfirst == [9, 4, 1, 16, 0]
