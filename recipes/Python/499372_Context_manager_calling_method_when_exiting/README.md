## Context manager for calling a method when exiting a 'with' statementOriginally published: 2007-01-11 10:58:46 
Last updated: 2007-01-11 10:58:46 
Author: Brett Cannon 
 
Provides a context manager that allows the user to specify a method on the passed-in object to be called when the 'with' statement is exited.  This is a generalization of contextlib.closing.