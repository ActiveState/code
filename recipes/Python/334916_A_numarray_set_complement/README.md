## A numarray set complement

Originally published: 2004-11-09 09:07:31
Last updated: 2004-11-13 00:59:19
Author: Gerry Wiener

This recipe finds the complement of a set of indices from a specific arange(n) array. Suppose, for example, you are given a linear array with 10 elements and you want to extract the elements from this array that have indices other than [1, 3, 5]. You can then use this recipe to first find the complement of [1, 3, 5], and you can then use numarray.take() to extract the elements of interest.