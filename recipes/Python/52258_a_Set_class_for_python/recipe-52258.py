class Set:
    """A Set is a collection of items with no particular ordering,
    containing no dulicates."""
    def __init__(self, *args):
        self._dict = {}
        for arg in args:
            self.add(arg)

    def __repr__(self):
        import string
        return "%s(%s)" % (self.__class__.__name__,
                           string.join(map(repr, self._dict.values()), ', '))

    def extend(self, args):
        """Add several items at once."""
        for arg in args:
            self.add(arg)

    def add(self, item):
        """Add one item to the set."""
        self._dict[item] = item

    def remove(self, item):
        """Remove an item from the set."""
        del self._dict[item]

    def contains(self, item):
        """Check whether the set contains a certain item."""
        return self._dict.has_key(item)

    # Higher performance member-test for python 2.0 and above
    __contains__ = contains

    def __getitem__(self, index):
        """Support the 'for item in set:' protocol."""
        return self._dict.keys()[index]

    def __len__(self):
        """Return the number of items in the set."""
        return len(self._dict)

    def items(self):
        """Return a list containing all items."""
        return self._dict.keys()

# class Set()
