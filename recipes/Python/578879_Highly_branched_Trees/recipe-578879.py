nmax = 20 # max number of branches per node

class Values:
    key = None
    def __init__(self, data):
        self.data = tuple(data)
        if len(data):
            self.key = data[0][0]
        
    def split(self):        
        l = self.data
        if len(l)<nmax:
            return (self,)
        n = nmax/2
        r = []
        while l:
            r.append(Values(l[:n]))
            l = l[n:]
        return tuple(r)
        
    def insert(self, key, value):
        for i, (k, v) in enumerate(self.data):
            if key<k:
                l = self.data[:i]+((key, value),)+self.data[i:]
                return Values(l)
            elif key == k:
                l = self.data[:i]+((key, value),)+self.data[i+1:]
                return Values(l)
        l = self.data+((key, value),)
        return Values(l)


class Node:
    def __init__(self, childs):
        assert childs
        self.data = tuple(childs)
        self.key = childs[0].key
        
    def split(self):
        l = self.data
        if len(l)<nmax:
            return (self,)
        n = nmax/2
        r = []
        while l:
            r.append(Node(l[:n]))
            l = l[n:]
        return tuple(r)
        
    def insert(self, key, value):
        last = None
        for i, child in enumerate(self.data):
            if key<child.key:
                if last is not None:
                    l = self.data[:i-1]+last.insert(key, value).split()+self.data[i:]
                else:
                    l = child.insert(key, value).split()+self.data[1:]
                return Node(l)
            last = child
        l = self.data[:-1]+last.insert(key, value).split()
        return Node(l)
        
