import types, copy

SeqType = [types.DictType, types.ListType]

class IsChangedMixin:
    def __init__(self):
        self.ResetChanges()

    def ResetChanges(self):
        """ Create a snapshot of own namespace dictionary. Halfway between a
            shallow and a deep copy - recursively make shallow copies of all 
            lists and dictionaries but object instances are copied as-is. Such
            objects will have their own IsModified attribute if they need to be
            tested for modification
        """
        self._snapshot = self._CopyItem(self.__dict__)

    def _CopyItem(self, item):
        """ Return shallow copy of item. If item is a sequence, recursively
            shallow copy each member that is also a sequence
        """ 
        newitem = copy.copy(item)
        if type(newitem) is types.DictType:
            for key in newitem:
                if type(newitem[key]) in SeqType:
                    newitem[key] = self._CopyItem(newitem[key])
        elif type(newitem) is types.ListType:
            for k in range(len(newitem)):
                if type(newitem[k]) in SeqType:
                    newitem[k] = self._CopyItem(newitem[k])
        return newitem

    def IsModified(self):
        """ Return True if current namespace dictionary is different to snapshot
            Examine contained objects having an IsModified attribute
            and return True if any of them are True.
        """
        return  self._CheckSequence(self.__dict__, self._snapshot, checklen=False)

    def _CheckSequence(self, newseq, oldseq, checklen=True):
        """ Scan sequence comparing new and old values of individual items
            return True when the first difference is found.
            Compare sequence lengths if checklen is True. It is False on first 
            call because self.__dict__ has _snapshot as an extra entry 
        """
        if checklen and len(newseq) <> len(oldseq):
            return True
        if type(newseq) is types.DictType:
            for key in newseq:
                if key == '_snapshot':
                    continue
                if key not in oldseq:
                    return True
                if self._CheckItem(newseq[key], oldseq[key]):
                    return True
        else:
            for k in range(len(newseq)):
                if self._CheckItem(newseq[k], oldseq[k]):
                    return True
        return 0

    def _CheckItem(self, newitem, olditem):
        """ Compare the values of newitem and olditem.
            If item types are sequences, make recursive call to _CheckSequence.
            If item types are instances of objects with an IsModified attribute,                     
            return True if IsModified() is True,
            otherwise return True if items are different
        """
        if type(newitem) in SeqType:
            return self._CheckSequence(newitem, olditem)
        elif type(newitem) is types.InstanceType:
            if newitem is not olditem:      # not the same instance
                return True
            if hasattr(newitem, 'IsModified') and newitem.IsModified():
                return True
        elif newitem <> olditem:
            return True
        else:
            return False
