## ActiveState recipe importer  
Originally published: 2011-11-23 02:25:43  
Last updated: 2011-11-23 02:27:51  
Author: nosklo   
  
Finally! This code allows you to import any activestate recipe right into your code!

Example:

    >>> from activestate.recipe194373 import mreplace
    >>> print mreplace('ectave steta racipas rock!', ('a', 'e'), ('e', 'a'))
    active state recipes rock!

Save this as **activestate.py**