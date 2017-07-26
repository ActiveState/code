## Generic block iterator  
Originally published: 2007-06-02 06:17:03  
Last updated: 2008-01-17 03:55:45  
Author: George Sakkis  
  
A common task, especially in text processing, is to break some input sequence into chunks (lines, paragraphs, records, etc.) and process them one by one. The iterators of builtin strings and files can be considered such chunkers, breaking the object into characters and lines respectively. This recipe is a generic way to break any iterable into consecutive blocks, specified by a delimiter or a pair of (start,end) delimiters.