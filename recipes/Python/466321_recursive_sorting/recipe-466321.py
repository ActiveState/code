"""
recursive sort
"""

def rec_sort(iterable):
    # if iterable is a mutable sequence type
    # sort it
    try:
        iterable.sort()
    # if it isn't return item
    except:
        return iterable
    # loop inside sequence items
    for pos,item in enumerate(iterable):
        iterable[pos] = rec_sort(item)
    return iterable


if __name__ == '__main__':

    struct = [[1,2,3,[6,4,5]],[2,1,5],[4,3,2]]
    print rec_sort(struct)
