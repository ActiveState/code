class Ring:
    def __init__(self, l):
        if not len(l):
            raise "ring must have at least one element"
        self._data = l

    def __repr__(self):
        return repr(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        return self._data[i]

    def turn(self):
        last = self._data.pop(-1)
        self._data.insert(0, last)

    def first(self):
        return self._data[0]

    def last(self):
        return self._data[-1]
