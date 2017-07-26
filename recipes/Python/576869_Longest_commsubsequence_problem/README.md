## Longest common subsequence problem solver  
Originally published: 2009-08-06 05:11:22  
Last updated: 2009-08-06 06:36:56  
Author: Shao-chuan Wang  
  
Longest common subsequence problem is a good example of dynamic programming, and also has its significance in biological applications.

For more information about LCS, please see:
http://en.wikipedia.org/wiki/Longest_common_subsequence_problem

Also, here, I use a 'cached' decorator to keep core algorithm neat. 
You can see how great the decorator could be. :)

Also note that, this recipe is just a demonstration of LCS and the usage of a python decorator. However, the memory is not used very efficiently. If the problem is very large-scaled, it may lead to stack overflow or memory error. 

So, do not use this recipe to deal with large-scaled problems. ;)