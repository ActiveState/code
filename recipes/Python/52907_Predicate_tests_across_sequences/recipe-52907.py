def every (pred, seq):
    """every takes a one argument predicate
    function and a sequence. Returns true
    if every element in seq returns true for
    predicate, else returns false.
    The predicate function should return true or false.
    """
    for i in seq:
        if not pred(i): return 0
    return 1

def any (pred, seq):
    """any takes a one argument predicate
    function and a sequence. Returns true
    if any element in seq returns true for
    predicate, else returns false.
    The predicate function should return true or false.
    """
    for i in seq:
        if pred(i): return 1
    return 0
