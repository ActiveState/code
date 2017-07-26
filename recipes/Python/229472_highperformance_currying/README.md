## high-performance currying with instancemethod  
Originally published: 2003-10-17 15:57:11  
Last updated: 2003-10-17 15:57:11  
Author: Alex Martelli  
  
instancemethod provides a way to perform currying such that the curried function runs much faster than one produced by closure (the second-fastest way).  [Currying is explained and covered in detail in other recipes]