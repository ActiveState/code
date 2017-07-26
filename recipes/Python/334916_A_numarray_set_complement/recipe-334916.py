#!/usr/bin/env python

import numarray

def complement(ind_arr, n):
    """
    Find the complement of the set of indices in ind_arr from
    arange(n)
    """

    mat = numarray.ones(n)
    numarray.put(mat, ind_arr, 0)
    out = numarray.nonzero(mat)
    return out[0]


if __name__ == "__main__":
    orig_arr = numarray.arange(10) + 0.2
    indices = numarray.array([1, 3, 5])
    comp = complement(indices, len(orig_arr))
    comp_arr = numarray.take(orig_arr, comp)
    print "orig_arr: ", orig_arr
    print "indices: ", indices
    print "complement indices: ", comp
    print "complement elements: ", comp_arr
