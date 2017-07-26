    def lazyDSU_sort(seq, keys, warn=False):
        """Return sorted seq, breaking ties by applying keys only when needed.

        If ``warn`` is True then an error will be raised if there were no
        keys remaining to break ties.

        Examples
        ========

        Here, sequences are sorted by length, then sum:

        >>> seq, keys = [[[1, 2, 1], [0, 3, 1], [1, 1, 3], [2], [1]], [
        ...    lambda x: len(x),
        ...    lambda x: sum(x)]]
        ...
        >>> lazyDSU_sort(seq, keys)
        [[1], [2], [1, 2, 1], [0, 3, 1], [1, 1, 3]]

        If ``warn`` is True, an error will be raised if there were not
        enough keys to break ties:

        >>> lazyDSU_sort(seq, keys, warn=True)
        Traceback (most recent call last):
        ...
        ValueError: not enough keys to break ties


        Notes
        =====

        The decorated sort is one of the fastest ways to sort a sequence for
        which special item comparison is desired: the sequence is decorated,
        sorted on the basis of the decoration (e.g. making all letters lower
        case) and then undecorated. If one wants to break ties for items that
        have the same decorated value, a second key can be used. But if the
        second key is expensive to compute then it is inefficient to decorate
        all items with both keys: only those items having identical first key
        values need to be decorated. This function applies keys successively
        only when needed to break ties.
        """
        from collections import defaultdict
        d = defaultdict(list)
        keys = list(keys)
        f = keys.pop(0)
        for a in seq:
            d[f(a)].append(a)
        seq = []
        for k in sorted(d.keys()):
            if len(d[k]) > 1:
                if keys:
                    d[k] = lazyDSU_sort(d[k], keys, warn)
                elif warn:
                  raise ValueError('not enough keys to break ties')
                seq.extend(d[k])
            else:
                seq.append(d[k][0])
        return seq
