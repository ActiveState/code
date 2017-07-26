## Walk a directory tree using a generatorOriginally published: 2002-01-04 16:54:27 
Last updated: 2002-01-05 01:01:38 
Author: Tom Good 
 
This is a new implementation of directory walking inspired by Fredrik Lundh's directoryWalker.py (see http://aspn.activestate.com/ASPN/Mail/Message/541112 ).  This code uses a generator instead of a class, so it requires Python 2.2 or above.