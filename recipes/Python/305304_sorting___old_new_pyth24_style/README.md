## sorting  -- old to new python 2.4 style (heapq,bisect,list.sort keywords,itemgetter)  
Originally published: 2004-09-17 13:35:44  
Last updated: 2006-09-13 12:28:57  
Author: John Nielsen  
  
Python 2.4 has added a new feature to handle the problem where you needed to do
a sort based off of part of the data. In effect, it has simplified the Schwartzian Transform
(which I learned many years ago from an perl article
written by Randall Schwartz). The following code will start with the older style
python sorting approaches, and then show the bisect and heapq modules, and
finally the key,cmp,reverse methods newly added to sort. The sort method of the
list is an in-place sort. There is also a new sorted() function which
returns a copy of the list sorted for you.