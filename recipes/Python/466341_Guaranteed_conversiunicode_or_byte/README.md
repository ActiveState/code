## Guaranteed conversion to unicode or byte string  
Originally published: 2006-01-23 22:14:48  
Last updated: 2006-01-23 22:14:48  
Author: Wai Yip Tung  
  
Python's built in function str() and unicode() return a string representation of the object in byte string and unicode string respectively. This enhanced version of str() and unicode() can be used as handy functions to convert between byte string and unicode. This is especially useful in debugging when mixup of the string types is suspected.