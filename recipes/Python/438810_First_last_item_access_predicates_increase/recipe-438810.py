def first(seq, pred=None):
    """Return the first item in seq for which the predicate is true.
    
    If the predicate is None, return the first item regardless of value.

    If no items satisfy the predicate, return None.
    """
    if pred is None:
        pred = lambda x: True
    for item in seq:
        if pred(item):
            return item
    return None

def last(seq, pred=None):
    """Return the last item in seq for which the predicate is true.
    
    If the predicate is None, return the last item regardless of value.

    If no items satisfy the predicate, return None.
    """
    if pred is None:
        pred = lambda x: True
    for item in reversed(seq):
        if pred(item):
            return item
    return None

# Just get the first item :)
# >>> seq = 'abc'
# >>> first(seq)
# 'a'

# Get the first item greater than 10
# >>> seq = [1, 2, 4, 12, 13, 15, 17]
# >>> first(seq, lambda x: x > 10)
# 12

# Get the last non-None/False/empty item
# >>> seq = ["one", "two", "three", "", None]
# >>> last(seq, bool)
# 'three'
