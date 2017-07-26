## Closest elements in a target array for a given input array  
Originally published: 2004-11-12 12:29:20  
Last updated: 2004-11-12 12:29:20  
Author: Gerry Wiener  
  
    Find the set of elements in input_array that are closest to
    elements in target_array.  Record the indices of the elements in
    target_array that are within tolerance, tol, of their closest
    match. Also record the indices of the elements in target_array
    that are outside tolerance, tol, of their match.

    For example, given an array of observations with irregular
    observation times along with an array of times of interest, this
    routine can be used to find those observations that are closest to
    the times of interest that are within a given time tolerance.