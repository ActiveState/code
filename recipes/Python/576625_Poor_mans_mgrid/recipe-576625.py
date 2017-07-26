'''
    Python 3 code.
    scipy.mgrid is a useful!
    This short implementation comes without installing numpy.


    Supports complex step.  "3j" means "three equi-spaced
    numbers from the span including the ends".

    >>> print(mgrid[1:2:3j])
    [1.0, 1.5, 2.0]


    Supports floating point step.

    >>> print(mgrid[1:2:0.5])
    [1.0, 1.5]


    does not support multi-dimensions,
    indicated by a tuple to scipy.mgrid

    >>> print(mgrid[1:2,3:5])
    Traceback (most recent call last):
      File "p.py", line 16, in __getitem__
        start,stop,step = s.start,s.stop,s.step
    AttributeError: 'tuple' object has no attribute 'start'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "p.py", line 18, in __getitem__
        raise TypeError('expected a slice')
    TypeError: expected a slice


    Deviates from scipy.mgrid.
    
    >>> mgrid[2:-1] # scipy.mgrid returns an empty list.
    [2, 1, 0]
'''

def convert_slice_to_list(Slice,list_length):
    '''
        A fun idiom.
        This gets python to deal with the "None"
        in slices like slice(None,None,3)
    '''
    return list(range(list_length))[Slice]

class poor_man_1D_mgrid:

    '''
        grid()[slice] emulates the scipy mgrid function for vectors.
    '''

    def __getitem__(self,s):
        try:
            start,stop,step = s.start,s.stop,s.step
        except:
            raise TypeError('expected a slice')
        start = start or 0
        step = step or 1
        L = stop-start
        if isinstance(step,complex):
            intervals = max(int(0.5+abs(step)),2)
            step = L/(intervals-1)
            halfway = start+L/2
            l,r = [],[]
            for i in range(int(intervals/2)):
                delta = step*i
                r.append(stop-delta)
                l.append(start+delta)
            if intervals & 1:
                l.append(l[-1]+(r[-1]-l[-1])/2)
            l.extend(reversed(r))
            return l
        if (L < 0) and (step == 1):
            step = -1
        if step*L < 0:
            raise ValueError('avoid infinite list')
        return [start+step*i for i in range(max(int(0.5+L/step),1))]

mgrid = poor_man_1D_mgrid()
