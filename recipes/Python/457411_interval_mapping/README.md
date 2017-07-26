## An interval mapping data structure  
Originally published: 2005-11-22 07:53:24  
Last updated: 2006-01-18 08:09:18  
Author: Nicolas Lehuen  
  
This structure is a kind of dictionary which allows you to map data intervals to values. You can then query the structure for a given point, and it returns the value associated to the interval which contains the point. Boundary values don't need to be an integer ; indeed in the unit test I use a datetime object.