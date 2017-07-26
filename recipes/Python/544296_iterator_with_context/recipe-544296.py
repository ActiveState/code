import collections
class itercontext:
    '''an iterator that allows accessing previous and next elements'''
    def __init__(self,it,countprevious,countcomingnext):
        '''initializes the iterator
        it: the underlying iterator
        countprevious: number of elements to keep after being visited
        countcomingnext: number of elements to look ahead
        '''
        self.iter=iter(it)
        # current element
        self.current=None
        self.existcurrent=False
        # list of previous and next elements
        self.comingnext=collections.deque()
        self.previous=collections.deque()
        self.countprevious=countprevious
        try:
            for i in range(countcomingnext):
                self.comingnext.append(self.iter.next())
        except StopIteration:
            pass
    
    def __iter__(self):
        return self
    def next(self):
        try:
            self.comingnext.append(self.iter.next())
        except StopIteration:
            pass # if the underlying iterator is exhausted, empty comingnext
        if len(self.comingnext)==0:
            raise StopIteration # if no more item ahead, stop
        if self.existcurrent: self.previous.append(self.current)
        self.current=self.comingnext.popleft()
        self.existcurrent=True
        if len(self.previous)>self.countprevious:
            self.previous.popleft()
        return self.current
    
    def getComingnext(self):
        return self.comingnext
    def getPrevious(self):
        return self.previous
    def listcomingnext(self):
        return list(self.comingnext)
    def listprevious(self):
        return list(self.previous)
