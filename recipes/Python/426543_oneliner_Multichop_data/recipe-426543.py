>>> a,bite = "supercalifragalisticexpialidocious",3
>>> [(a[d:d+bite]) for d in range(len(a)-bite) if d%bite==0]

[('s', 'u', 'p'), ('e', 'r', 'c'), ('a', 'l', 'i'), ('f', 'r', 'a'), ('g', 'a', 'l'), ('i', 's', 't'), ('i', 'c', 'e'), ('x', 'p', 'i'), ('a', 'l', 'i'), ('d', 'o', 'c'), ('i', 'o', 'u')]

>>> # or on a list
>>> b =['sup', 'erc', 'ali', 'fra', 'gal', 'ist', 'ice', 'xpi', 'ali', 'doc', 'iou']
>>> 
>>> [(b[d:d+bite]) for d in range(len(b)-bite) if d%bite==0]
[['sup', 'erc', 'ali'], ['fra', 'gal', 'ist'], ['ice', 'xpi', 'ali']]
