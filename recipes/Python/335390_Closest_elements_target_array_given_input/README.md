###Closest elements in a target array for a given input array

Originally published: 2004-11-12 12:29:20
Last updated: 2004-11-12 12:29:20
Author: Gerry Wiener

    Find the set of elements in input_array that are closest to\n    elements in target_array.  Record the indices of the elements in\n    target_array that are within tolerance, tol, of their closest\n    match. Also record the indices of the elements in target_array\n    that are outside tolerance, tol, of their match.\n\n    For example, given an array of observations with irregular\n    observation times along with an array of times of interest, this\n    routine can be used to find those observations that are closest to\n    the times of interest that are within a given time tolerance.