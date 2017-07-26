# Simple series generator with
# multiple generators & decorators.
# Author : Anand B Pillai

def myfunc(**kwds):

    def func(f):
        cond = kwds['condition']
        proc = kwds['process']
        num = kwds['number']

        x = 0
        for item in f():
            
            if cond and cond(item):
                if proc: item = proc(item)
                yield item
                x += 1
                
            if x==num:
                break

    return func

def series(condition=None, process=None, number=10):

    @myfunc(condition=condition,process=process,number=number)    
    def wrapper():
        x = 1
        while 1:
            yield x
            x += 1

    return wrapper
