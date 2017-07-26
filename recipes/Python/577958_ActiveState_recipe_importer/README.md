## ActiveState recipe importerOriginally published: 2011-11-23 02:25:43 
Last updated: 2011-11-23 02:27:51 
Author: nosklo  
 
Finally! This code allows you to import any activestate recipe right into your code!\n\nExample:\n\n    >>> from activestate.recipe194373 import mreplace\n    >>> print mreplace('ectave steta racipas rock!', ('a', 'e'), ('e', 'a'))\n    active state recipes rock!\n\nSave this as **activestate.py**