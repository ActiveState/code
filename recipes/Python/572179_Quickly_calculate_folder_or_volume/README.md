## Quickly calculate folder or volume size 
Originally published: 2008-05-01 11:45:38 
Last updated: 2008-05-01 19:41:45 
Author: Higinio Cachola 
 
This recipe uses the win32file.FindFilesW() function to efficiently calculate total size of a folder or volume, and additionally handles cases where a cutoff size is desired or errors are encountered along the path.