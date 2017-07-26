## Importing any file without modifying sys.pathOriginally published: 2002-10-28 10:08:43 
Last updated: 2002-10-28 10:08:43 
Author: Walter Dörwald 
 
This recipe lets you import any file as a module. It's not required that the file is in the Python search path. This is done without having to modify sys.path (even temporarily)