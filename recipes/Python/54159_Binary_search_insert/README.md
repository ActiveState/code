## Binary search and insert in Python  
Originally published: 2001-04-20 20:05:40  
Last updated: 2001-04-25 05:09:37  
Author: Noah Spurrier  
  
This demonstrates a simple binary search through sorted data.
A binary search is a basic algorithm provided by bisect in Python.
The binary search can be summarized by two lines of code:
   list.sort()
   item_insert_point = bisect.bisect (list, item)