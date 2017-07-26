#!/usr/bin/env python
class chainfunc(list):
    def __init__(self):
        self.res = []
    def append(self, func, *args, **kw):
        super(self.__class__, self).append([func,args,kw])
    def __call__(self):
        for (fn, args, kw) in self:
            retval = (fn.__name__, fn(*args, **kw))
            self.res.append(retval)
            yield retval

    def ANDoperation(self):
        state = reduce(lambda x,y: x and y, [bool for id,bool in self.res])
        return state
    and_operation = property(fget=ANDoperation)

    def ORoperation(self):
        state = reduce(lambda x,y: x or y, [bool for id,bool in self.res])
        return state
    or_operation = property(fget=ORoperation)

# some sample functions

def t1(name,i):
    print name
    print i
    return True

def t2(id,i=False):
    print id
    print i
    return i

if __name__ == '__main__':
    cf = chainfunc()
    cf.append(t1,'hello',2)
    cf.append(t2,'ab_1',False)
    cf.append(t2,'ab_2',True)
    gen = cf()

    # execute all functions
    for i in range(len(cf)):
        print "Function name= %s, function State=%s, "%gen.next()
        print "AND operation =%s, OR operation=%s\n"%(cf.and_operation, cf.or_operation)
