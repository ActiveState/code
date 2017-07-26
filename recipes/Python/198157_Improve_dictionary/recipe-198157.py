def sparsify(d):
    """Improve dictionary sparsity.

    The dict.update() method makes space for non-overlapping keys.
    Giving it a dictionary with 100% overlap will build the same
    dictionary in the larger space.  The resulting dictionary will
    be no more that 1/3 full.  As a result, lookups require less
    than 1.5 probes on average.

    Example:
    >>> import __builtin__
    >>> sparsify(__builtin__.__dict__)

    """

    e = d.copy()
    d.update(e)
