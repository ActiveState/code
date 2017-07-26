## Getting min/max in a sequence greater/less than some value 
Originally published: 2005-05-26 02:48:41 
Last updated: 2005-06-01 05:41:42 
Author: Edvard Majakari 
 
Sometimes it is useful to know what is the smallest value in a sequence\ngreater than (or equal to) some other value. Eg.\n\nmax_lt([2, 3, 5, 7, 11], 6) would be 5, because 5 is greatest value in the list\nwhich is also less than 6. Following the same lines method call\nmin_gt([3, 5, 6, 10, 12], 6) would return 10, because 10 is the smallest value in the list greater than  6. The following four simple methods implement min_gt, min_le, max_gt and max_ge, but the input must be sorted for them to work.\n\nHowever, Greg Jorgensen's suggestion is much more clever. No need for sorting, just use list comprehensions with min/max.