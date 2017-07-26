import itertools

def offsetter(iterable, offsets=(0, 1), longest=False):
    """
    Return offset element from an iterable.
    Pad offset element with None at boundaries.
    """

    # clone the iterable
    clones = itertools.tee(iterable, len(offsets))

    # set up the clone iterables
    iterables = []
    for offset, clone in zip(offsets, clones):
        if offset > 0:
            # fast forward the start
            clone = itertools.islice(clone, offset, None)
        elif offset < 0:
            # pad the front of the iterable
            clone = itertools.chain(itertools.repeat(None, -offset), clone)
        else:
            # nothing to do
            pass

        iterables.append(clone)

    if longest:
        return itertools.izip_longest(*iterables)
    else:
        return itertools.izip(*iterables)
