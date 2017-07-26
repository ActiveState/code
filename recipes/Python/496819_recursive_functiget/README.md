## A recursive function to get permutation of a list  
Originally published: 2006-06-23 14:00:51  
Last updated: 2006-06-30 00:03:39  
Author: Wensheng Wang  
  
I saw a lot of implementations that doesn't work on list with repeated items.\nFor example: [3,3,"hello","hello"]\nThis recipe show such function that works on any list.\n(update 6/29/06) added generator version permu2(xs).