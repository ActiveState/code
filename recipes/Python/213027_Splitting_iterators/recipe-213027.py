import copy

class _IDup(object):
        """Internal class used only to keep a reference on the actual iterator,
        and to do housekeeping."""

        def __init__(self,iterin):
                self.__iter = iterin
                self.__iterno = 0
                self.__iteritems = []
                self.__hasstopped = None

        def registerIter(self,oldno=-1):
                iterno = self.__iterno
                self.__iterno += 1
                if oldno == -1:
                        self.__iteritems.append([])
                else:
                        self.__iteritems.append(
                                copy.deepcopy(self.__iteritems[oldno])
                                )
                return iterno

        def getNext(self,iterno):
                if self.__iteritems[iterno]:
                        iteritem = self.__iteritems[iterno].pop(0)
                elif self.__hasstopped is not None:
                        raise self.__hasstopped
                else:
                        try:
                                iteritem = self.__iter.next()
                        except StopIteration, e:
                                self.__hasstopped = e
                                raise
                        for id, i in enumerate(self.__iteritems):
                                if id <> iterno:
                                        i.append(copy.deepcopy(iteritem))
                return iteritem

class _IDupped(object):
        """Duplicated Iterator class. Each iterator you get by calling isplit
        or split on a splitted iterator will be of this type."""

        def __init__(self,idup,oldno=-1):
                self.__idup = idup
                self.__iterno = idup.registerIter(oldno)

        def next(self):
                return self.__idup.getNext(self.__iterno)

        def split(self):
                """Split this iterator into two pieces. The original iterator
                is still callable, as is the sub-iterator."""

                return _IDupped(self.__idup,self.__iterno)

        def __iter__(self):
                return self

def isplit(iterin,splitno=2):
        idup = _IDup(iterin)
        iduppeds = []
        for i in range(splitno):
                iduppeds.append(_IDupped(idup))
        return tuple(iduppeds)

# Create first few iterators.
test = ["hello","how","are","you?"]
x, y = isplit(iter(test))

# Test print of iterator y.
print "First item of y."
print y.next()

# Create new iterator z after first element of y.
z = y.split()

# Print rest of the elements.
print "Rest in x."
for i in x:
        print i
print "Rest in y."
for i in y:
        print i
print "Rest in z."
for i in z:
        print i
