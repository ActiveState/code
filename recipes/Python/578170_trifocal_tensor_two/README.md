## trifocal tensor from two camera matrices  
Originally published: 2012-06-21 07:33:51  
Last updated: 2012-06-27 03:38:35  
Author: J W J  
  
Get the 3x3x3 (27 element) trifocal tensor from two 3x4 camera matrices.\n\n    T[i,j,k] = A[j,i]*B[k,4] - A[j,4]*B[k,i]\n