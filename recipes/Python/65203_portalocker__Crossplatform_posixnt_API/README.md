## portalocker - Cross-platform (posix/nt) API for flock-style file locking.  
Originally published: 2001-06-14 11:18:48  
Last updated: 2008-05-16 21:12:08  
Author: Jonathan Feinberg  
  
Synopsis:\n\n   import portalocker\n   file = open("somefile", "r+")\n   portalocker.lock(file, portalocker.LOCK_EX)\n   file.seek(12)\n   file.write("foo")\n   file.close()