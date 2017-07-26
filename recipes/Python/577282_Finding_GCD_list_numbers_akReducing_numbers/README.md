## Finding the GCD of a list of numbers (a.k.a. Reducing numbers in a list)  
Originally published: 2010-07-06 18:52:55  
Last updated: 2010-07-06 18:52:55  
Author: Stephen Akiki  
  
http://akiscode.com/articles/gcd_of_a_list.shtml\n\nThis python code snippet allows you to find the GCD of a list of numbers, after this it is a simple matter of diving all the numbers in the list by the GCD to reduce it.\n\n\nWhy this works...\n\n\n\nThe GCD of a list of numbers [a, b, c] is GCD(GCD(a, b), c).  The reduce function does exactly this and thus gives you the GCD of all the numbers in the list.\n