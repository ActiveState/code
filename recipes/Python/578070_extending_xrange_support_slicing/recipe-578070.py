def read_xrange(xrange_object):
    '''returns the xrange object's start, stop, and step'''
    start = xrange_object[0]
    if len(xrange_object) > 1:
       step = xrange_object[1] - xrange_object[0]
    else:
        step = 1
    stop = xrange_object[-1] + step
    return start, stop, step
    
class Xrange(object):
    ''' creates an xrange-like object that supports slicing and indexing.
    ex: a = Xrange(20)
    a.index(10)
    will work
    
    Also a[:5]
    will return another Xrange object with the specified attributes
    
    Also allows for the conversion from an existing xrange object
    '''
    def __init__(self, *inputs):
        # allow inputs of xrange objects
        if len(inputs) == 1:
            test, = inputs
            if type(test) == xrange:
                self.xrange = test
                self.start, self.stop, self.step = read_xrange(test)
                return
        
        # or create one from start, stop, step
        self.start, self.step = 0, None
        if len(inputs) == 1:
            self.stop, = inputs
        elif len(inputs) == 2:
            self.start, self.stop = inputs
        elif len(inputs) == 3:
            self.start, self.stop, self.step = inputs
        else:
            raise ValueError(inputs)
            
        self.xrange = xrange(self.start, self.stop, self.step)
    
    def __iter__(self):
        return iter(self.xrange)
        
    def __getitem__(self, item):
        if type(item) is int:
            if item < 0:
                item += len(self)
            
            return self.xrange[item]
        
        if type(item) is slice:
            # get the indexes, and then convert to the number
            start, stop, step = item.start, item.stop, item.step
            start = start if start != None else 0 # convert start = None to start = 0
            if start < 0:
                start += start
            start = self[start]
            if start < 0: raise IndexError(item)
            step = (self.step if self.step != None else 1) * (step if step != None else 1)
            stop = stop if stop is not None else self.xrange[-1]
            if stop < 0:
                stop += stop
                
            stop = self[stop]
            stop = stop
            
            if stop > self.stop:
                raise IndexError
            if start < self.start:
                raise IndexError
            return Xrange(start, stop, step)
    
    def index(self, value):
        error = ValueError('object.index({0}): {0} not in object'.format(value))
        index = (value - self.start)/self.step
        if index % 1 != 0:
            raise error
        index = int(index)
        
        
        try:
            self.xrange[index]
        except (IndexError, TypeError):
            raise error
        return index
                                  
    def __len__(self):
        return len(self.xrange)
