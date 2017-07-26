## General Class for interfacing with Windows .DLLs 
Originally published: 2002-08-27 12:23:31 
Last updated: 2002-08-27 12:23:31 
Author: Larry Bates 
 
When I wanted to use Python to call functions in Windows .DLL I was surprised that I had a difficult time locating the necessary information for making this happen.  This is a base class that you use to define your class (and methods for each function).  It uses Sam Rushings calldll, cstring and membuf modules but I think it will make interfacing with any DLL much easier for the beginner (especially for the first time).