def two_finger(iterable):
    """
    >>> sequence = [1, 3, 9, 5, 22, 11]
    >>> for item, next in two_finger(sequence):
    ...     print item, next
    ... 
    1 3
    3 9
    9 5
    5 22
    22 11
    """
    iterator = iter(iterable)
    item = iterator.next()
    while True:
        try:
            next = iterator.next()
            yield item, next
            item = next
        except StopIteration:
            return
