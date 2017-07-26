"""
>>> list(zip_pad([], [1], [1,2]))
[(None, 1, 1), (None, None, 2)]

>>> list(zip_pad([], [1], [1,2], pad=42))
[(42, 1, 1), (42, 42, 2)]

>>> list(zip_pad([], []))
[]

>>> list(zip_pad([1], [2]))
[(1, 2)]

>>> list(zip_pad([1,2], []))
[(1, None), (2, None)]

>>> list(zip_pad([1], [2]))
[(1, 2)]

>>> list(zip_pad([1,2], []))
[(1, None), (2, None)]

>>> list(zip_pad([1,2], [3,4]))
[(1, 3), (2, 4)]

>>> list(zip_pad([1,2], [10,20,30], [100,200,300,400]))
[(1, 10, 100), (2, 20, 200), (None, 30, 300), (None, None, 400)]
"""

from itertools import izip, chain

def zip_pad(*iterables, **kw):
    if kw:
        assert len(kw) == 1
        pad = kw["pad"]
    else:
        pad = None
    done = [len(iterables)-1]
    def pad_iter():
        if not done[0]:
            return
        done[0] -= 1
        while 1:
            yield pad
    iterables = [chain(seq, pad_iter()) for seq in iterables]
    return izip(*iterables)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
