"""For data stored by a sorted key, perform a merge join over parallel
iteration through multiple data sources.

Author: Joel Nothman, me@joelnothman.com

Some sequences to join:
>>> fathers = [
...     ('Abe', 'Jim'),
...     ('Benny', 'John'),
...     ('David', 'Jacob'),
...     ('Evan', 'Jonas'),
... ]
>>> mothers = [
...     ('Abe', 'Michelle'),
...     ('Benny', 'Mary'),
...     ('Caleb', 'Madeline'),
...     ('Evan', 'Marna'),
... ]
>>> phones = [
...     ('Benny', '000-000-0002'),
...     ('David', '000-000-0004'),
... ]

We wish to retrieve row data combining each of these columns:

>>> for t in merge_join(fathers, mothers, phones):
...     print t
('Abe', 'Jim', 'Michelle', None)
('Benny', 'John', 'Mary', '000-000-0002')
('Caleb', None, 'Madeline', None)
('David', 'Jacob', None, '000-000-0004')
('Evan', 'Jonas', 'Marna', None)

"""

def _first_iter_vals(iters):
    """Generate the first values of each iterator."""
    for it in iters:
        try:
            yield it.next()
        except StopIteration:
            yield None


def _merge_join_next(iters, cur_pairs):
    """Generate the values of the next tuple (key, v1, ..., vn) by finding the
    minimum key available, and returning the corresponding values where
    available while advancing the respective iterators."""

    # Find the next key, or quit if all keys are None
    try:
        min_key = min(p[0] for p in cur_pairs if p)
    except ValueError:
        return

    # Yield the key as the first tuple element
    yield min_key

    for i, (it, p) in enumerate(zip(iters, cur_pairs)):
        try:
            k, v = p
        except TypeError:
            # p is None => the iterator has stopped
            yield None
            continue

        if k != min_key:
            # No data for this key
            yield None
            continue

        # Yes data for this key: yield it
        yield v

        # Update cur_pairs for this iterator
        try:
            cur_pairs[i] = it.next()
        except StopIteration:
            cur_pairs[i] = None


def merge_join(*iters):
    """Given a series of n iterators whose data are of form ``(key, value)``,
    where the keys are sorted and unique for each iterator, generates tuples
    ``(key, val_1, val_2, ..., val_n)`` for all keys, where ``val_i`` is the
    value corresponding to ``key`` in the ``i``th iterator, or None if no such
    pair exists for the ``i``th iterator."""

    iters = [iter(it) for it in iters]
    cur_pairs = list(_first_iter_vals(iters))
    while True:
        tup = tuple(_merge_join_next(iters, cur_pairs))
        if not tup:
            return
        yield tup

if __name__ == "__main__":
    import doctest
    doctest.testmod()
