class groupby(dict):
    def __init__(self, seq, key=lambda x:x):
        for value in seq:
            k = key(value)
            self.setdefault(k, []).append(value)
    __iter__ = dict.iteritems

# -------------------------- Examples -----------------------------------

>>> letters = 'abracadabra'
>>> [g for k, g in groupby(letters)]                # grouped
[['a', 'a', 'a', 'a', 'a'], ['r', 'r'], ['b', 'b'], ['c'], ['d']]
>>> [k for k, g in groupby(letters)]                # uniq
['a', 'r', 'b', 'c', 'd']
>>> [(k, len(g)) for k, g in groupby(letters)]      # uniq -c
[('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)]
>>> [k for k, g in groupby(letters) if len(g) > 1]  # uniq -d
['a', 'r', 'b']

>>> data = [('becky', 'girl', 5), ('john', 'boy', 10), ('sue', 'girl', 10)]
>>> for k, g in groupby(data, key=lambda r: r[1]):
...     print k
...     for record in g:
...         print "   ", record
...
boy
    ('john', 'boy', 10)
girl
    ('becky', 'girl', 5)
    ('sue', 'girl', 10)
