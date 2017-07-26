>>> from itertools import groupby
>>> [(k, len(list(g))) for k, g in groupby(sorted(myList))]
[('1', 4), ('2', 1), ('3', 2), ('4', 1)]
