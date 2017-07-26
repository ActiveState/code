class Listlike:
    def __init__(self):
        self.list = [1, 2, 3, 4, 5]
    def __getitem__(self, index):
        return self.list[index]
    def __len__(self):
        return len(self.list)

>>> listlike = Listlike()
>>> list(listlike)
[1, 2, 3, 4, 5]
