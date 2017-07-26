def divide(iterable, parts):
    ''' Partitions an iterable into parts number of lists. '''
    items = list(iterable)

    seqs = [[] for _ in xrange(parts)]
    while items:
        for i in xrange(parts):
            if not items:
                break
        
            seqs[i].append(items.pop())
        
    return seqs
