## Windows Dll (with pointers parameters) calling with ctypes and calldllOriginally published: 2003-02-16 12:42:27 
Last updated: 2004-11-07 16:53:38 
Author: Stefano Spinucci 
 
Code to call a Windows Dll """void FAR PASCAL hllapi(int FAR *, char FAR *, int FAR *, int FAR *)""" with ctypes (trivial) and calldll (a nightmare).