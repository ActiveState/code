from itertools import cycle
from collections import deque

def roundrobin(*iterables):
    q = deque(iter(it) for it in iterables)
    for itr in cycle(q):
        try:
            yield itr.next()
        except StopIteration:
            if len(q) > 0:
                q.pop()
            else:
                break

# EXAMPLE

for letter in roundrobin('ABC', 'DE', 'FGH'):
    print letter

# prints 'A', 'D', 'F', 'B', 'E', 'G', 'C', 'H'
