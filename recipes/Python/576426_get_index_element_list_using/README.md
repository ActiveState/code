## get index of element in list using identityOriginally published: 2008-08-16 19:32:28 
Last updated: 2008-08-16 19:41:37 
Author: nosklo  
 
my_list.index(element) returns the index of the element using common comparision (as in == or __eq__() or __cmp__()). If you need to find an element on the list using identity comparing (is) then this function can do it for you