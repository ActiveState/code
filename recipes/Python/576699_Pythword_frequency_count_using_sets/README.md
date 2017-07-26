###Python word frequency count using sets and lists

Originally published: 2009-03-26 23:00:54
Last updated: 2009-03-26 23:00:54
Author: nick 

This lists unique words and word frequencies occurring in a Python string. You can ignore or take account of letter case in distinguishing words, and you can pass it your own inclusion list of characters allowed in words (e.g. is "import123" the kind of word you want to list, or not? It might be if you're a programmer.) By default only alpha chars are allowed in words.\n\nAt first glance having the whole piece of text, and intermediate results, in memory at once is a problem for large files. But it's zippy: it found 1600 unique words in a 7M SQL script (472,000 words in original) in 20 seconds, and hardly notices a 4000-word document cut and pasted across from a word processor.\n\nWith a bit of extra work, the algorithm could be fed a very large file in chunks. Anyone?