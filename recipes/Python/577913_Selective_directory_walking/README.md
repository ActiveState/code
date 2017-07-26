## Selective directory walking  
Originally published: 2011-10-19 06:34:56  
Last updated: 2011-10-20 05:05:39  
Author: Nick Coghlan  
  
Python's os.walk() standard library iterator is useful if you want to walk an entire directory tree, but you're on your own when it comes to implementing name filtering and recursive depth limiting on top of it.

This recipe supports these features with an interface that is just as convenient as the underlying os.walk() API, while being significantly more powerful.