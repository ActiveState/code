class FieldCmp:    
    def __init__(self, fields, rev = 0):
        self.fields = fields
        if rev:
            self.rev = -1
        else:
            self.rev = 1
            
    def cmp(self, s1, s2):
        for field in self.fields:
            f1 = s1.__dict__[field]
            f2 = s2.__dict__[field]
            if f1 < f2:
                return -1 * self.rev
            elif f1 > f2:
                return self.rev
                
        return 0
        
        
if __name__ == '__main__':
    class Struct:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        def __repr__(self):
            return repr((self.a, self.b, self.c))
            
    l = [Struct(10, 20, 20), Struct(10, 10, 20), Struct(30, 20, 30)]
    
    ll = l[:]
    fc = FieldCmp(['a'])
    ll.sort(fc.cmp)
    print ll
            
    ll = l[:]
    fc = FieldCmp(['a'], 1)
    ll.sort(fc.cmp)
    print ll

    ll = l[:]
    fc = FieldCmp(['a', 'b'])
    ll.sort(fc.cmp)
    print ll

    ll = l[:]
    fc = FieldCmp(['a', 'b'], 1)
    ll.sort(fc.cmp)
    print ll
