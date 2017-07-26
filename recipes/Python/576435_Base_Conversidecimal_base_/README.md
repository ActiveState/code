## Base Conversion decimal to base = len(map) 
Originally published: 2008-08-20 11:54:00 
Last updated: 2008-08-20 05:01:39 
Author: Mark Zitnik 
 
This code enable decimal base conversion according map length and a different char set.\n\nExample:\n\n* map = ['0','1'] base 2 10 -> 1010\n* map = ['a','b'] base 2 10 -> baba\n* map = ['a','b','c','d','e','f','g','h','i','j','k','l'] base 12 10 -> k\n* map = ['a','b','c','d','e','f','g','h','i','j','k','l'] base 12 100 -> ie\n\nthis simple method can be used in web sites to hide a well known decimal sequence like user ids.\n