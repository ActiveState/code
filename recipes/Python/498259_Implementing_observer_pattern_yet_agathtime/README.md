## Implementing the observer pattern yet again: this time with coroutines and the with statementOriginally published: 2006-11-10 16:38:01 
Last updated: 2006-11-10 16:38:01 
Author: Jim Baker 
 
Implements the observer design pattern via generator coroutines, wrapped up to use the new 'with' statement of Python 2.5.  Enables the loosely-coupled observation of any container implementing the dictionary protocol.