###Associating multiple values with each key in a dictionary.

Originally published: 2001-03-09 18:37:31
Last updated: 2001-03-09 18:37:31
Author: Michael Chermside

A normal dictionary performs a mapping of the form: key -> value. Suppose you want a dictionary which maps each key to multiple values: key -> [value*]. Here's an easy and efficient way to achieve it. We rely on the setdefault() method of dictionarys both initialize the list of values for this key if necessary, and give us the list at the same time.