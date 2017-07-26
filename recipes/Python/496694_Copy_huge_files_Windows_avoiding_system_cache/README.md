## Copy huge files on Windows avoiding system cache misbehaviourOriginally published: 2006-05-10 18:06:55 
Last updated: 2006-05-10 18:06:55 
Author: Christos Georgiou 
 
This recipe uses pywin32 in order to copy files making use of the win32file.FILE_FLAG_SEQUENTIAL_SCAN, which makes much more efficient use of the system cache (only a few megabytes are consumed instead of caching the whole file).