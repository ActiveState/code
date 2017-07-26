## Sorting big files the Python 2.6 way

Originally published: 2009-05-14 19:05:38
Last updated: 2009-05-30 21:51:09
Author: Gabriel Genellina

This is just a rewrite of Recipe 466302 "Sorting big files the Python 2.4 way", taking advantage of heapq.merge, context managers, and other niceties of newer Python versions. It can be used to sort very large files (millions of records) in Python. No record termination character is required, hence a record may contain embedded binary data, newlines, etc. You can specify how many temporary files to use and where they are located.\n