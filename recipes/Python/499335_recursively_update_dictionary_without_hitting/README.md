## recursively update a dictionary without hitting "Python recursion limit" 
Originally published: 2006-12-19 04:41:35 
Last updated: 2006-12-21 10:28:56 
Author: Robin Bryce 
 
This function recursively walks the items and values of two dict like objects. At each level when a key exists in both, and each value is a dict, then the destination dict is updated from the source dict usiing the builtin dict.update method. After the operation all keys and values from the source, at any level, will be referenced in the destination.