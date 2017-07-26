###Sorted dictionary

Originally published: 2010-01-09 19:54:56
Last updated: 2010-01-20 17:11:59
Author: Jan Kaliszewski

A simple implementation of a dictionary which always (when applicable) returns keys, values, items (key-value pairs) sorted by keys (inserting/removing order doesn't matter and only keys are important; so please note that it is something different than OrderedDict in Python 3.1/2.7 or Django's SortedDict).