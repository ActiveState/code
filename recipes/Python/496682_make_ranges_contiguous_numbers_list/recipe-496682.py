def list2range(lst):
    '''make iterator of ranges of contiguous numbers from a list of integers'''

    tmplst = lst[:]
    tmplst.sort()
    start = tmplst[0]

    currentrange = [start, start + 1]

    for item in tmplst[1:]:
        if currentrange[1] == item:
            # contiguous
            currentrange[1] += 1
        else:
            # new range start
            yield tuple(currentrange)
            currentrange = [item, item + 1]

    # last range
    yield tuple(currentrange)



if __name__ == '__main__':
    # test routine
    a = [1,2,3,4,5,6,7,8,10,11,12,23,24,25,26]
    b = [(1,9), (10,13), (23, 27)]
    c = list(list2range(a))

    if b != c:
        print 'failed!'
    else:
        print 'succeed!'
    print c
