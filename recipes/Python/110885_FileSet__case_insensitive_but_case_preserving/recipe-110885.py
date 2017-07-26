class FileSet:
    def __init__(self, *args):
        self._dict = {}
        for arg in args:
            self.add(arg)

    def __repr__(self):
        return "<FileSet %s at %x>" % (self._dict.values(), id(self))

    def add(self, file):
        self._dict[string.upper(file)] = file

    def remove(self, file):
        del self._dict[string.upper(file)]

    def contains(self, file):
        return string.upper(file) in self._dict.keys()

    def __getitem__(self, index):
        key = self._dict.keys()[index]
        return self._dict[key]

    def __len__(self):
        return len(self._dict)

    def items(self):
        return self._dict.values()
