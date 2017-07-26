def with_iter(iterable):
    """Wrap an iterable in a with statement, so it closes when consumed.

    >>> uplines = (line.upper() for line in with_iter(open(path, 'r')))
    >>> print('\n'.join(uplines))
    """
    with iterable:
        for item in iterable:
            yield item
