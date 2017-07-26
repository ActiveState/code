# -*- coding: utf-8 -*-

'''
Provide a simple and efficient mask tool for the id of an object.\n
Always used in url against a spider.
'''

_KEY = 9878676540

_BOX = ['a', 'b', 'h', 't', 'n', 's', 'p', 'q', 'l', 'x']

def mask(n):
    _id = int(n)^_KEY
    _id = [int(i) for i in list(str(_id))]
    return ''.join(map(lambda i: _BOX[i], _id))

def unmask(s):
    try:
        _s = map(lambda l: _BOX.index(l), list(s))
        _n = int(''.join(map(str, _s)))
        return _n^_KEY
    except:
        return s

>>> id = 717
>>> mask(id)
'xlqlpqqhtt'
>>> unmask('xlqlpqqhtt')
717
