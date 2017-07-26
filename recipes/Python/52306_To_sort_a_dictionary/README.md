## "To sort a dictionary"

Originally published: 2001-03-26 11:26:34
Last updated: 2001-04-08 19:35:01
Author: Alex Martelli

Dictionaries can't be sorted -- a mapping has no ordering! -- so, when you feel the need to sort one, you no doubt want to sort its *keys* (in a separate list).  Sorting (key,value) pairs (items) is simplest, but not fastest.