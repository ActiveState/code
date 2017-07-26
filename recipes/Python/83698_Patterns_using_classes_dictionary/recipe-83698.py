class Base:
        def __init__(self,v):
                self.v=v

class StaticHash(Base):
        def __hash__(self):
                if not hasattr(self,"hashvalue"):
                        self.hashvalue=hash(self.v)
                return self.hashvalue

class ImmutableHash(Base):
        def __init__(self,v):
                self.__dict__["protect"]=[]
                Base.__init__(self,v)

        def __hash__(self):
                self.protect.append("v")
                return hash(self.v)
        def __setattr__(self,k,v):
                if k in self.protect:
                        raise NameError,"%s is protected." % k
                else:
                        self.__dict__[k]=v

class ValueIdentity(ImmutableHash):
        def __cmp__(self,x):
                if self.v==x.v:
                        return 0
                if self.v<x.v:
                        return -1
                return 1

if __name__=="__main__":
        ## SHASH:
        s1=StaticHash(1)
        s2=StaticHash(2)
        r={s1:1,s2:2}
        s2.v=3
        print r[s2]
        ## IHASH
        i1=ImmutableHash(1)
        i2=ImmutableHash(2)
        r={i1:1,i2:2}
        try:
                i1.v=100
        except NameError,v:
                print "NameError,",v
        ## VALUEID
        v1=ValueIdentity(1)
        v2=ValueIdentity(2)
        if v1==v2:
                print "ID1"
        v2.v=1
        if v1==v2:
                print "ID2"
        ## VALUEHASH
        r={v1:1}
        print r[v2]
