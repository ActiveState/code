from itertools import *
from collections import deque

# First a naive approach. At each generation we pop the first element and append
# it to the back. This is highly memmory deficient.
def rotations(it):
    """ rotations([0,1,2]) --> [[0, 1, 2], [1, 2, 0], [2, 0, 1]] """
    l = list(it)
    for i in range(len(l)):
        yield iter(l)
        l = l[1:]+[l[0]]

# A much better approach would seam to be using a deque, which rotates in O(1),
# However this does have the negative effect, that generating the next rotation
# before the current has been iterated through, will result in a RuntimeError
# because the deque has mutated during iteration.
def rotations(it):
    """ rotations([0,1,2]) --> [[0, 1, 2], [1, 2, 0], [2, 0, 1]] """
    l = deque(it)
    for i in range(len(l)):
        yield iter(l)
        l.rotate()

# The trick is to use subsets of infinite lists. First we define the function tails,
# which is standard in many functal languages.
# Because of the way tee is implemented in itertools, the below implementation will
# use memory only propertional to the offset difference between the generated
# iterators.
def tails(it):
    """ tails([1,2,3,4,5]) --> [[1,2,3,4,5], [2,3,4,5], [3,4,5], [4,5], [5], []] """
    while True:
        tail, it = tee(it)
        yield tail
        next(it)

# We can now define two new rotations functions.
# The first one is very similar to the above, but since we never keep all list
# elements, we need an extra length parameter.
def rotations(it, N):
    """ rotations([0,1,2]) --> [[0, 1, 2], [1, 2, 0], [2, 0, 1]] """
    return (islice(rot,N) for rot in islice(tails(cycle(it)),N))

# The above works fine for things like:
# >>> for rot in rotations(range(4), 4):
# ...     print (list(rot))
# ... 
# [0, 1, 2, 3]
# [1, 2, 3, 0]
# [2, 3, 0, 1]
# [3, 0, 1, 2]
#
# But that is not really where it shines, since the lists are iterated one after
# another, and so the tails memory usage becomes linear.
# 
# In many cases tails and infinite lists lets us get away with an even simpler
# rotaions function:
def rotations(it, N):
    """ rotations([0,1,2]) --> [[0, 1, 2], [1, 2, 0], [2, 0, 1]] """
    return islice(tails(cycle(it)),N)

# This one works great for instances where we are topcut anyway:
# >>> for rot in rotations(range(4), 4):
# ...     print (list(zip(range(4), rot)))
# ... 
# [(0, 0), (1, 1), (2, 2), (3, 3)]
# [(0, 1), (1, 2), (2, 3), (3, 0)]
# [(0, 2), (1, 3), (2, 0), (3, 1)]
# [(0, 3), (1, 0), (2, 1), (3, 2)]
