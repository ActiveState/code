#!/usr/bin/env python

import numarray


def find_closest(input_array, target_array, tol):
    """

    Find the set of elements in input_array that are closest to
    elements in target_array.  Record the indices of the elements in
    target_array that are within tolerance, tol, of their closest
    match. Also record the indices of the elements in target_array
    that are outside tolerance, tol, of their match.

    For example, given an array of observations with irregular
    observation times along with an array of times of interest, this
    routine can be used to find those observations that are closest to
    the times of interest that are within a given time tolerance.

    NOTE: input_array must be sorted! The array, target_array, does not have to be sorted.

    Inputs:
      input_array:  a sorted Float64 numarray
      target_array: a Float64 numarray
      tol:          a tolerance

    Returns:
      closest_indices:  the array of indices of elements in input_array that are closest to elements in target_array
      accept_indices:  the indices of elements in target_array that have a match in input_array within tolerance
      reject_indices:  the indices of elements in target_array that do not have a match in input_array within tolerance
    """

    input_array_len = len(input_array)
    closest_indices = numarray.searchsorted(input_array, target_array) # determine the locations of target_array in input_array
    acc_rej_indices = [-1] * len(target_array)
    curr_tol = [tol] * len(target_array)

    est_tol = 0.0
    for i in xrange(len(target_array)):
        best_off = 0          # used to adjust closest_indices[i] for best approximating element in input_array

        if closest_indices[i] >= input_array_len:
            # the value target_array[i] is >= all elements in input_array so check whether it is within tolerance of the last element
            closest_indices[i] = input_array_len - 1
            est_tol = target_array[i] - input_array[closest_indices[i]]
            if est_tol < curr_tol[i]:
                curr_tol[i] = est_tol
                acc_rej_indices[i] = i
        elif target_array[i] == input_array[closest_indices[i]]:
            # target_array[i] is in input_array
            est_tol = 0.0
            curr_tol[i] = 0.0
            acc_rej_indices[i] = i
        elif closest_indices[i] == 0:
            # target_array[i] is <= all elements in input_array
            est_tol = input_array[0] - target_array[i]
            if est_tol < curr_tol[i]:
                curr_tol[i] = est_tol
                acc_rej_indices[i] = i
        else:
            # target_array[i] is between input_array[closest_indices[i]-1] and input_array[closest_indices[i]]
            # and closest_indices[i] must be > 0
            top_tol = input_array[closest_indices[i]] - target_array[i]
            bot_tol = target_array[i] - input_array[closest_indices[i]-1]
            if bot_tol <= top_tol:
                est_tol = bot_tol
                best_off = -1           # this is the only place where best_off != 0
            else:
                est_tol = top_tol

            if est_tol < curr_tol[i]:
                curr_tol[i] = est_tol
                acc_rej_indices[i] = i

        if est_tol <= tol:
            closest_indices[i] += best_off

    accept_indices = numarray.compress(numarray.greater(acc_rej_indices, -1), acc_rej_indices)
    reject_indices = numarray.compress(numarray.equal(acc_rej_indices, -1), numarray.arange(len(acc_rej_indices)))
    return (closest_indices, accept_indices, reject_indices)

def test(input_array, target_array, tol):
    (closest_indices, accept_indices, reject_indices) = find_closest(input_array, target_array, tol)

    print "tol: ", tol
    print "input_array: ", input_array
    print "target_array: ", target_array
    print "input_array elts closest to target: ", numarray.take(input_array, closest_indices)
    print "their input_array indices: ", closest_indices
    print "indices of elts in target_array that are within tolerance of their closest match: ", accept_indices
    print "indices of elts in target_array that are outside tolerance of their closest match: ", reject_indices
    print "-" * 90

if __name__ == "__main__":

    input_array = numarray.array([0.8, 1.1, 1.6, 2.05, 3.95, 4.7])
    target_array = numarray.array([1.0, 2.0, 3.0, 4.0, 5.0])
    tol = 0.11
    test(input_array, target_array, tol)

    input_array = numarray.array([0.9, 0.95, 1.01, 1.1, 1.6, 1.9999, 2.001, 2.05, 3.95, 4.7])
    target_array = numarray.array([1.0, 2.0, 3.0, 4.0, 5.0])
    tol = 0.11
    test(input_array, target_array, tol)


    input_array = numarray.array([0.8, 1.1, 1.6, 2.05, 3.95, 4.7])
    l = [1.0, 2.0, 3.0, 4.0, 5.0]
    l.reverse()
    target_array = numarray.array(l)
    tol = 0.11
    test(input_array, target_array, tol)
