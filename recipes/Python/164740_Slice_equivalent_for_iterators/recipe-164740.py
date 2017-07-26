import sys
def iterslice(sequence, start=None, stop=None, step=1):
    if step == 0:
        raise ValueError, "Attempt to use 0 as step value"
    if stop is None:
        stop = sys.maxint*cmp(step,0)
    elif stop<0: 
        try:
            stop = max(len(sequence)+stop,0)
        except TypeError:
            raise TypeError, "Negative slice index on unsized sequence"
    if start is None:
        if step>0: 
            start = 0
        else:
            try:
                start = len(sequence)-1
            except TypeError:
                raise TypeError, ("Unable to start from the end of an "
                                  "unsized sequence")
    elif start<0: 
        try:
            start = max(len(sequence)+start,0)
        except TypeError:
            raise TypeError, "Negative slice index on unsized sequence"
    try:
        for i in xrange(start, stop, step):
                yield sequence[i]
    except IndexError:
        return
    except TypeError:
        if step<0:
            raise TypeError, ("Attempt to use negative step on an "
                              "unindexable sequence")
        #check if the sequence support iterator protocol
        itr = iter(sequence)
        try:
            for i in xrange(start):
                itr.next()
            while start<stop:
                yield itr.next()
                for i in xrange(step-1):
                    itr.next()
                start+=step
        except StopIteration:
            return
        
#
# sample
#      
X = [chr(x) for x in range(100)]
print list(iterslice(X,10,20))
print list(iterslice(iter(X),10,20))
print X[10:20]
