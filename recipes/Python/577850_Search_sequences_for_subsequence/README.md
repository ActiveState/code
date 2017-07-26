## Search sequences for sub-sequenceOriginally published: 2011-08-19 05:17:00 
Last updated: 2011-08-19 05:17:00 
Author: Steven D'Aprano 
 
The list and tuple index() method and ``in`` operator test for element containment, unlike similar tests for strings, which checks for sub-strings:\n\n    >>> "12" in "0123"\n    True\n    >>> [1, 2] in [0, 1, 2, 3]\n    False\n\n\nThese two functions, search and rsearch, act like str.find() except they operate on any arbitrary sequence such as lists:\n\n    >>> search([1, "a", "b", 2, 3], ["b", 2])\n    2\n\n\n