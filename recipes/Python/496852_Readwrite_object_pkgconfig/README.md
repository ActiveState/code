## Read/write object for pkg-config files  
Originally published: 2006-06-29 16:20:14  
Last updated: 2006-06-29 23:33:27  
Author: Christopher Dunn  
  
Here is a convenient way to create, parse, alter, and write .pc files.  Just pass PkgConfig() a file-like object, or None to start fresh.  Print the object to create a new .pc file.\n\nSome people might want even more functionality, but I chose not to hinder the flexibility of the class.