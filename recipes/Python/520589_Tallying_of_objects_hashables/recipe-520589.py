from sys import version_info as pyver


class Tally:
    """ 
    A tally or histogram class

    Counts the occurances of objects (hashables only) given to it.
    The number of seen samples is stored in the object's samples 
    instance variable.

    """
    def __init__(self):
        self.samples = 0L
        self.values = {}

    def incr(self, k, amount = 1):
        """
        Increase count for k
        """
        self.samples += 1
        self.values[k] = self.values.get(k, 0) + amount

    def decr(self, k, amount = 1):
        """
        Decrease count for k
        """
        self.samples += 1
        self.values[k] = self.values.get(k, 0) - amount

    def val(self, k):
        """
        Return count for k
        """
        return self.values.get(k, 0)

    def getkeys(self):
        """
        Return all histogram keys
        """
        return self.values.keys()

    def counts(self, desc = False):
        '''
        Return list of keys, sorted by values.
        If desc is True, return a descending sort.
        '''
        if (pyver[0] < 2) or (pyver[0] == 2 and pyver[1] < 4):
            # This is for Python versions <2.4
            i = map(lambda items: list(items), self.values.items())
            map(lambda rev: rev.reverse(), i)
            i.sort()
            if desc:
                i.reverse()
            return i

        else:
            # This only works with Python >=2.4 but is much
            # faster than the code above.

            return sorted(( list(reversed(items)) \
                for items in self.values.iteritems() ), reverse = desc)
