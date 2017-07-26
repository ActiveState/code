class UserListSubclass(list):
    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))
    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)
    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))

# Subclass this class if you need to overwrite __getitem__ and have it called
# when accessing slices.
# If you subclass list directly, __getitem__ won't get called when accessing
# slices as in mylist[2:4].
