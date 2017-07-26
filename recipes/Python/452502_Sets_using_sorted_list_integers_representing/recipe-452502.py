from array import array

class VSort:
    
    def __init__(self):
        self.atoms = []
        self.unranks = array('L',[])
    
    def rank(self,x):
        a = self.atoms
        b = self.unranks
        n = len(a)
        i = self.bisect_left(x)
        if i == n or a[b[i]] != x:
            a.append(x)
            b.insert(i,n)
        return b[i]

    def bisect_left(self,x, lo=0, hi=None):
        a = self.atoms
        b = self.unranks
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            if a[b[mid]] < x: 
                lo = mid+1
            else: 
                hi = mid
        return lo
    
    def __contains__(self,x):
        a = self.atoms
        b = self.unranks
        n = len(a)
        i = self.bisect_left(x)
        return i < n and a[b[i]] == x
    
    def __len__(self):
        return len(self.atoms)
    
    def items(self):
        a = self.atoms
        b = self.unranks
        return [a[i] for i in b]
    
    def __iter__(self):
        return iter(self.items())
    
    def remove(self,x):
        a = self.atoms
        b = self.unranks
        n = len(a)
        i = self.bisect_left(x)
        y = b[i]
        if  i < n and a[y] == x:
            del a[y]
            del b[i]
            for j,k in enumerate(b):
                if k > y:
                    b[j] -= 1

U = VSort()

class Set:
    
    def __init__(self,seq):
        self.V = VSort()
        for x in seq:
            self.V.rank(U.rank(x))
    
    def __repr__(self):
        return 'Set(' + repr(self.items()) + ')'
    
    def __len__(self):
        return len(self.V)
    
    def __iter__(self):
        return iter(self.items())
    
    def items(self):
        V = VSort()
        for i in self.V:
            V.rank(U.atoms[i])
        return V.items()
    
    def union(self,other):
        return Set(self.items()+other.items())
    
    def __contains__(self,x):
        return U.rank(x) in self.V
    
    def add(self,x):
        self.V.rank(U.rank(x))
    
    def remove(self,x):
        self.V.remove(U.rank(x))
    
    def intersection(self,other):
        V = VSort()
        a = self.V
        b = other.V
        if len(a) > len(b):
            a,b = b,a
        for x in a:
            if x in b:
                V.rank(x)
        return Set([U.atoms[i] for i in V])
        
    def difference(self,other):
        V = VSort()
        for x in self.V:
            if x not in other.V:
                V.rank(x)
        return Set([U.atoms[i] for i in V])
        
def test():
    S1 = Set('adjhdjgfyhrfjhsdf')
    S2 = Set('12748134346')
    print S1.union(S2)
    print '1' in S1
    S1.add('1')
    print '1' in S1
    S1.remove('1')
    print '1' in S1
    S3 = Set('adj')
    print S1
    print S1.intersection(S3)
    print S1.difference(S3)
    S4 = Set([S1,S2,S3])
    print S4

if __name__=='__main__':
    test()
