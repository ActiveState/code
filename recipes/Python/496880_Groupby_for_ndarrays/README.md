## Groupby for ndarrays.  
Originally published: 2006-07-11 15:19:09  
Last updated: 2006-07-11 15:19:09  
Author: Alexander Ross  
  
This is a groupby function for arrays.  Given a list of arrays and a `key` function, it will group each array based on the value of `key(args[0])`.  The returned arrays will be two dimensional.  The size of the first dimension is equal to the number of groups, and the size of the second dimension is equal to the size of the largest group.  All of the smaller groups are padded with the value of the keyword argument `fill_value`.\n\nThere's also a short recipe in here for functional composition.