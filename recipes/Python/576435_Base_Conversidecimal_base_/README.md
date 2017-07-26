## Base Conversion decimal to base = len(map)  
Originally published: 2008-08-20 11:54:00  
Last updated: 2008-08-20 05:01:39  
Author: Mark Zitnik  
  
This code enable decimal base conversion according map length and a different char set.

Example:

* map = ['0','1'] base 2 10 -> 1010
* map = ['a','b'] base 2 10 -> baba
* map = ['a','b','c','d','e','f','g','h','i','j','k','l'] base 12 10 -> k
* map = ['a','b','c','d','e','f','g','h','i','j','k','l'] base 12 100 -> ie

this simple method can be used in web sites to hide a well known decimal sequence like user ids.
