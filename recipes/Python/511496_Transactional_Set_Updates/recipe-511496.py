from itertools import chain, ifilterfalse

class TransactionSet(object):

    def __init__(self, self.master):
        self.master = set(master)
        self.deleted = set()
        self.added = set()

    def check_invariants(self):
        assert self.deleted <= self.master     # deleted is a subset of master       
        assert not (self.added & self.master)  # added is disjoint from master

    def __len__(self):
        return len(self.master) - len(self.deleted) + len(self.added)

    def __iter__(self):
        return chain(self.added, ifilterfalse(self.deleted.__contains__, self.master))

    def __contains__(self, key):
        s = frozenset([key])
        return not not (s & self.master and not s & self.deleted or s & self.added)

    def add(self, key):
        s = frozenset([key])
        self.deleted -= s
        self.added |= s

    def discard(self, key):
        s = frozenset([key])
        if s & self.master:
            self.deleted |= s
        else:
            self.added -= s

    def remove(self, key):
        s = frozenset([key])
        if s & self.master:
            self.deleted |= s
        elif s & self.added:
            self.added -= s
        else:
            raise KeyError(key)

    def pop(self):
        if self.added:
            return self.added.pop()
        for elem in ifilterfalse(self.deleted.__contains__, self.master):
            self.deleted.add(elem)
            return elem
        raise KeyError(key)

    def intersection(self, other):
        other = frozenset(other)
        return ((self.master & other) - self.deleted) | (self.added & other)

    def _Set(self):
        s = self.master - self.deleted
        s |= self.added
        return s

    def union(self, other):
        s = _Set(self)
        s.update(other)
        return s

    def difference(self, other):
        s = _Set(self)
        s.difference_update(other)
        return s

    def symmetric_difference(self, other):
        s = _Set(self)
        s.symmetric_diffence_update(other)
        return s

    def update(self, other):
        other = frozenset(other)
        self.deleted -= other
        self.added += other - self.master

    def intersection_update(self, other):
        other = frozenset(other)
        self.deleted |= self.master - other
        self.added &= other

    def difference_update(self, other):
        other = frozenset(other)
        self.deleted |= self.master & other
        self.added -= other

    def symmetric_difference_update(self, other):
        master_and_other = self.master.intersection(other)
        self.deleted |= master_and_other
        self.added ^= other - master_and_other

    def issubset(self, other):
        return len(self)<=len(other) and not (other & self.deleted) and master.issubset(other - self.added)

    def issuperset(self, other):
        return len(self)>=len(other) and not (other & self.deleted) and master.issuperset(other - self.added)
