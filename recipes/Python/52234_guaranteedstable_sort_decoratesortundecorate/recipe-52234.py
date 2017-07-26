def stable_sorted_copy(alist, _indices=xrange(sys.maxint)):
    # the 'decorate' step: make a list such that each item
    # is the concatenation of sort-keys in order of decreasing
    # significance -- we'll sort this auxiliary-list
    decorated = zip(alist, _indices)

    # the 'sort' step: just builtin-sort the auxiliary list
    decorated.sort()

    # the 'undecorate' step: extract the items from the
    # decorated, and now correctly sorted, auxiliary list
    return [ item for item, index in decorated ]

def stable_sort_inplace(alist):
    # if "inplace" sorting is desired, simplest is to assign
    # to a slice-of-all-items of the original input list
    alist[:] = stable_sorted_copy(alist)
