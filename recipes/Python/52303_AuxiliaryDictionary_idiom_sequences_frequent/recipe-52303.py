# simple, naive, excellent... but perhaps slow!
def addUnique1(baseList, otherList):
    for item in otherList:
        if item not in baseList:
            baseList.append(item)

# may be faster if otherList is large:
def addUnique2(baseList, otherList):
    auxDict = {}
    for item in baseList:
        auxDict[item] = None
    for item in otherList:
        if not auxDict.has_key(item):
            baseList.append(item)
            auxDict[item] = None

# often better is to wrap the sequence, together
# with its auxiliary dictionary, in an object
# (using __contains__ to speed "in"-tests) --
# note the dictionary must be carefully maintained
# to stay "in sync" with the sequence!  Here's a
# version which does the syncing "just in time",
# when a membership test is actually required...:
import UserList
class FunkyList(UserList.UserList):
    def __init__(self, initlist=None):
        UserList.__init__(self, initlist)
        self._dict_ok = None
    def _sync_dict(self):
        if not self._dict_ok:
            self._dict = {}
            for item in self.data:
                self._dict[item] = None
            self._dict_ok = 1
    def __contains__(self, item):
        self._sync_dict()
        return self._dict.has_key(item)

    # the auxiliary, internal-use method that
    # resets the 'dictionary OK' flag then
    # delegates the actual operation
    def _delegate_modify(self, method, *args):
        self._dict_ok = None
        return method(self, *args)

    # patiently delegate each potentially membership-changing
    # method through the _delegate_modify one, so that _dict_ok 
    # gets reset whenever membership may have changed

    def __setitem__(self, *args)
        return self._delegate_modify(UserList.__setitem__, *args)
    def __delitem__(self, *args):
        return self._delegate_modify(UserList.__delitem__, *args)
    def __setslice__(self, *args):
        return self._delegate_modify(UserList.__setslice__, *args)
    def __delslice__(self, *args):
        return self._delegate_modify(UserList.__delslice__, *args)
    def __iadd__(self, *args):
        return self._delegate_modify(UserList.__iadd__, *args)
    def append(self, *args):
        return self._delegate_modify(UserList.append, *args)
    def insert(self, *args):
        return self._delegate_modify(UserList.insert, *args)
    def pop(self, *args):
        return self._delegate_modify(UserList.pop, *args)
    def remove(self, *args):
        return self._delegate_modify(UserList.remove, *args)
    def extend(self, *args):
        return self._delegate_modify(UserList.extend, *args)
