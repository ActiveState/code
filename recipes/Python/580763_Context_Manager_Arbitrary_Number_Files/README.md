## Context Manager for an Arbitrary Number of Files in Python  
Originally published: 2017-03-13 13:19:23  
Last updated: 2017-03-13 13:27:50  
Author: Alfe   
  
The pattern using `with` together with `open()` to automatically close a file after leaving the context is well known.  To open a fixed number you can simply nest these statements or use the comma notation.  For having a context which represents an arbitrary number of open files you can use the `ExitStack` class, but only for Python 3.3+.\n\nFor other Python versions I'm using the following class which I named `Files`.  The presented implementation is only for reading files (for keeping it clear).  Extending it for having various file modes should not pose a problem.