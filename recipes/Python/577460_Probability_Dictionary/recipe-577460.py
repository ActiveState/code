from numbers import Real

class ProbDict(dict):
    """A dictionary serving as a probability measure."""
    
    def __init__(self, items = None):
        """Create a dictionary from iters.

        If items can't be fed to a dictionary, it will be interpreted as a 
        collection of keys, and each value will default to value 1/n. Otherwise,
        the values are normalized to sum to one. Raises ValueError if
        some values are not numbers or are negative.

        Arguments:
        - `items`: argument with which to make dictionary

        """
        if items is None: return dict.__init__(self)
        try:
            # can fail if items is not iterable or not full of size 2 items:
            dict.__init__(self, items)
        except TypeError:
            try:
                # Let's assume items is a finite iterable full of keys
                vals = [1/len(items)] * len(items)
            except TypeError:
                # Apparently items has no length -- let's take it as the only
                # key and put all the probability on it.
                dict.__init__(self, (items, 1))
            else:
                # if items has a length, it can be iterated through with zip
                dict.__init__(self, zip(items, vals))
        else:
            # we've successfully made dic from key, value pairs in items, now let's 
            # normalize the dictionary, and check the values
            for v in self.values():
                if not isinstance(v, Real):
                    raise TypeError("Values must be nonnegative real numbers so I " +
                               "can properly normalize them. " + str(v) + " is not.")
                elif v < 0:
                    raise ValueError("Values must be nonnegative, unlike " + str(v))

            tot = sum(self.values())
            for k, v in self.items(): self[k] = v/tot

            

    def __setitem__(self, key, value):
        # Overridden to make sure dict is normalized.
        if not isinstance(value, Real) or value < 0 or value > 1:
            raise ValueError("Value must be a number between 0 and 1, unlike " +
                             str(i))
        try:
            r = (self[key] - value)/(1 - self[key])
            # r is the fraction of the remaining probability mass that
            # we're going to give up (take).
            for k in filter(key.__ne__, self):
                dict.__setitem__(self, k, self[k] * (1 + r))
            value = value if len(self) != 1 else 1
            if value:
                dict.__setitem__(self, key, value)
            else:
                # This is the purging stage!
                dict.__delitem__(self, key)
        except ZeroDivisionError:
            # self[key] = 1, so key has all the probability mass. We'll leave it
            # as is, since there's no sensible way of reducing it.
            pass

    def __delitem__(self, key):
        # Deleting frees up probability mass!
        self[key] = 0
        # Note that __setitem__ handles the deletion for us.

    def __missing__(self, key):
        # Accessing an inexistent key gives 0 rather than error, but
        # does not create key, val pair (unlike defaultdict)
        return 0
