def orderBy(sortlist, orderby=[], desc=[]):
    '''orderBy(sortlist, orderby, desc) >> List
    sortlist: list to be sorted
    orderby: list of field indexes
    desc: list of field indexes that are to be sorted descending'''      
    orderby.reverse()
    for i in orderby:
        sortlist.sort(lambda x, y: cmp(*[(x[i], y[i]), (y[i], x[i])][i in desc]))
    return sortlist
