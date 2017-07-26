from collections.abc import Sequence, MutableSequence


class ChainedListView(Sequence):
    """A view of a chain of lists, treated as a single immutable list."""
    def __init__(self, *lists):
        self.lists = list(lists)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join(self.lists))

    def __str__(self):
        return str(list(self))

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(item == other[i] for i, item in enumerate(self))

    def __ne__(self, other):
        return not (self == other)

    # XXX could use other comparisons

    def __len__(self):
        return sum(len(lst) for lst in self.lists)

    def get_list(self, index):
        """Return (list, index) for the sublist where index falls."""
        if isinstance(index, slice):
            # XXX needs support for slices
            raise NotImplementedError
        index_orig = index
        if index < 0:
            index = len(self) + index
        for lst in self.lists:
            if index < len(lst):
                return lst, index
            index = index - len(lst)
        raise IndexError(index_orig)

    def __getitem__(self, index):
        lst, index = self.get_list(index)
        return lst[index]


class ChainedList(ChainedListView, MutableSequence):
    """A chain of lists, treated as a single list.

    If insert_upper is False and an index falls on the first element
    of a sublist, the item will actually be added to the end of the
    preceding sublist.

    """
    def __init__(self, *lists, insert_upper=True):
        super(ChainedList, self).__init__(*lists)
        self.insert_upper = insert_upper

    def __setitem__(self, index, item):
        lst, index = self.get_list(index)
        lst[index] = item

    def __delitem__(self, index):
        lst, index = self.get_list(index)
        del lst[index]

    def insert(self, index, item):
        if index == len(self):
            lst, index = self.get_list(index-1)
            if self.insert_upper and lst is not self.lists[-1]:
                self.lists[self.lists.index(lst) + 1].append(item)
            else:
                lst.insert(index + 1, item)
            return

        # index < len(self)
        lst, index = self.get_list(index)
        if index == 0 and not self.insert_upper and lst is not self.lists[0]:
            self.lists[self.lists.index(lst) - 1].append(item)
        else:
            lst.insert(index, item)
