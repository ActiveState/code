class YieldResult(BaseException):pass

def greduce(func, strm):
    '''    
    Reduce generator. 
    @param func: function of two arguments. Unlike reduce the function passed
                 into the generator may not need to return a value but modify
                 its first argument inplace like list.extend.
    @param strm: list of values passed into func. strm can be updated using 
                 greduce.send(l) where l is another list.
    '''
    res = None
    while 1:
        try:
            try:
                if res is None:
                    res, v = strm[:2]
                    del strm[0:2]
                else:
                    v = strm[0]
                    del strm[0]
            except (ValueError, IndexError):
                l = yield
            else:
                out = func(res, v)
                res = out if out is not None else res
                l = yield res
            if l:
                strm.extend(l)
                yield
        except YieldResult:
            yield res            



def reduced(stream_red):
    '''
    reduced() is complementary to the greduce generator. 
    Use this function to keep the current value of the reduced stream. This
    is analog to reduce(lst) where reduce() is Pythons builtin reduce and lst
    is a list.    
    '''
    res = stream_red.next()
    if res is None:
        res = stream_red.throw(YieldResult)
        stream_red.next()
        return res
    for item in stream_red:
        if item is None:
            break
        else:
            res = item
    return res

#
# Example 1
#

>>> stm = greduce(lambda x,y: x+y,[1,2,3])
>>> stm.next()
3
>>> stm.next()
6
>>> stm.next()     # yields None if nothing is left to reduce
>>> stm.send([4])  # send new list into stm ...
>>> stm.next()     # ...and continue.
10

#
# Example 2
#

>>> def maps(f): 
...     return lambda x, y: x+[f(y)] if isinstance(x, list) else [f(x),f(y)]

>>> stm = greduce(maps(lambda x:x+10),[1,2,3,4])
>>> reduced(stm)  # this is the aequivaent to map(lambda x:x+10, [1,2,3,4])
[11, 12, 13, 14]
>>> reduced(stm) == reduced(stm)  # nothing else should be expected
True
>>> stm.send([5,6])
>>> reduced(stm)        
[11, 12, 13, 14, 15, 16]

#
# Example 3
#

>>> stm = greduce(list.extend,[[1,2],[3,4]])  # inplace manipulation
>>> reduced(stm)                              # works!
[1, 2, 3, 4]
>>> stm.send([[5,6]])
>>> reduced(stm)
[1, 2, 3, 4, 5, 6]
