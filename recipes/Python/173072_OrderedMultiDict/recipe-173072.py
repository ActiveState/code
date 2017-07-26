# Written in 2003 by Andrew Dalke, Dalke Scientific Software, LLC.
# This software has been released to the public domain.  No
# copyright is asserted.

from __future__ import generators

# Implementation inheritence -- not asserting a class hierarchy here
#
# If there is a class hierarchy, OrderedMultiDict is a child of
# UnorderedMultiDict because it makes stronger but not different
# guarantees on how the data works, at least data-wise.
# Performance-wise, Ordered has a slower (O(n)) than Unordered (O(1)).
# Convince me otherwise and I'll change.  Besides, hierarchies are
# overrated.
class _BaseMultiDict:
    def __str__(self):
        """shows contents as if this is a dictionary

        If multiple values exist for a given key, use the last
        one added.
        """
        d = {}
        for k in self.data:
            d[k] = self.data[k][-1]
        return str(d)
    def __len__(self):
        """the number of unique keys"""
        return len(self.data)

    def __getitem__(self, key):
        """value for a given key

        If more than one value exists for the key, use one added most recently
        """
        return self.data[key][-1]

    def get(self, key, default = None):
        """value for the given key; default = None if not present
        
        If more than one value exists for the key, use the one added
        most recently.
        """
        return self.data.get(key, [default])[-1]
    
    def __contains__(self, key):
        """check if the key exists"""
        return key in self.data

    def keys(self):
        """unordered list of unique keys"""
        return self.data.keys()

    def values(self):
        """unordered list of values

        If more than one value exists for a given key, use the value
        added most recently.
        """
        return [x[-1] for x in self.data.values()]
    
    def items(self):
        """unordered list of key/value pairs

        If more than one value exists for a given key, use the value
        added most recently.
        """
        return [(k, v[-1]) for k, v in self.data.items()]

    def getall(self, key):
        """Get all values for a given key

        Multiple values are returned in input order.
        If the key does not exists, returns an empty list.
        """
        return self.data[key]

    def __iter__(self):
        """iterate through the list of unique keys"""
        return iter(self.data)

    
class OrderedMultiDict(_BaseMultiDict):
    """Store key/value mappings.

    Acts like a standard dictionary with the following features:
       - duplicate keys are allowed;

       - input order is preserved for all key/value pairs.

    >>> od = OrderedMultiDict([("Food", "Spam"), ("Color", "Blue"),
    ...                        ("Food", "Eggs"), ("Color", "Green")])
    >>> od["Food"]
    'Eggs'
    >>> od.getall("Food")
    ['Spam', 'Eggs']
    >>> list(od.allkeys())
    ['Food', 'Color', 'Food', 'Color']
    >>>

    The order of keys and values(eg, od.allkeys() and od.allitems())
    preserves input order.

    Can also pass in an object to the constructor which has an
    allitems() method that returns a list of key/value pairs.

    """
    def __init__(self, multidict = None):
        self.data = {}
        self.order_data = []
        if multidict is not None:
            if hasattr(multidict, "allitems"):
                multidict = multidict.allitems()
            for k, v in multidict:
                self[k] = v
    def __eq__(self, other):
        """Does this OrderedMultiDict have the same contents and order as another?"""
        return self.order_data == other.order_data
    def __ne__(self, other):
        """Does this OrderedMultiDict have different contents or order as another?"""
        return self.order_data != other.order_data
    
    def __repr__(self):
        return "<OrderedMultiDict %s>" % (self.order_data,)

    def __setitem__(self, key, value):
        """Add a new key/value pair

        If the key already exists, replaces the existing value
        so that d[key] is the new value and not the old one.

        To get all values for a given key, use d.getall(key).
        """
        self.order_data.append((key, value))
        self.data.setdefault(key, []).append(value)

    def __delitem__(self, key):
        """Remove all values for the given key"""
        del self.data[key]
        self.order_data[:] = [x for x in self.order_data if x[0] != key]

    def allkeys(self):
        """iterate over all keys in input order"""
        for x in self.order_data:
            yield x[0]
    def allvalues(self):
        """iterate over all values in input order"""
        for x in self.order_data:
            yield x[1]
    def allitems(self):
        """iterate over all key/value pairs in input order"""
        return iter(self.order_data)


    
class UnorderedMultiDict(_BaseMultiDict):
    """Store key/value mappings.

    Acts like a standard dictionary with the following features:
       - duplicate keys are allowed;

       - input order is preserved for all values of a given
           key but not between different keys.

    >>> ud = UnorderedMultiDict([("Food", "Spam"), ("Color", "Blue"),
    ...                          ("Food", "Eggs"), ("Color", "Green")])
    >>> ud["Food"]
    'Eggs'
    >>> ud.getall("Food")
    ['Spam', 'Eggs']
    >>>

    The order of values from a given key (as from ud.getall("Food"))
    is guaranteed but the order between keys (as from od.allkeys()
    and od.allitems()) is not.

    Can also pass in an object to the constructor which has an
    allitems() method that returns a list of key/value pairs.

    """
    def __init__(self, multidict = None):
        self.data = {}
        if multidict is not None:
            if hasattr(multidict, "allitems"):
                multidict = multidict.allitems()
            for k, v in multidict:
                self[k] = v

    def __eq__(self, other):
        """Does this UnorderedMultiDict have the same keys, with values in the same order, as another?"""
        return self.data == other.data

    def __ne__(self, other):
        """Does this UnorderedMultiDict NOT have the same keys, with values in the same order, as another?"""
        return self.data != other.data

    def __repr__(self):
        return "<UnorderedMultiDict %s>" % (self.data,)

    def __setitem__(self, key, value):
        """Add a new key/value pair

        If the key already exists, replaces the existing value
        so that d[key] is the new value and not the old one.

        To get all values for a given key, use d.getall(key).
        """
        self.data.setdefault(key, []).append(value)

    def __delitem__(self, key):
        """Remove all values for the given key"""
        del self.data[key]

    def allkeys(self):
        """iterate over all keys in arbitrary order"""
        for k, v in self.data.iteritems():
            for x in v:
                yield k

    def allvalues(self):
        """iterate over all values in arbitrary order"""
        for v in self.data.itervalues():
            for x in v:
                yield x

    def allitems(self):
        """iterate over all key/value pairs, in arbitrary order

        Actually, the keys are iterated in arbitrary order but all
        values for that key are iterated at sequence of addition
        to the UnorderedMultiDict.

        """
        for k, v in self.data.iteritems():
            for x in v:
                yield (k, x)
