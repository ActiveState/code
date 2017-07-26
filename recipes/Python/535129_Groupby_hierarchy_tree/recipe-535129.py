from operator import itemgetter
from itertools import groupby

def groupby2(cols, lst, lev=0):
    if not cols:
        return str(list(lst))
    keyfun = itemgetter(cols[0])
    srted  = sorted(list(lst), key=keyfun)
    output = ""
    for key, iter in groupby(srted, key=keyfun):
        output += "\n"+"   "*lev+"%10s:"%key
        output += groupby2(cols[1:], iter, lev+1)
    return output
