## Listing the package/patches dependencies of a binary on Solaris  
Originally published: 2008-07-30 04:28:26  
Last updated: 2008-07-30 04:30:44  
Author: Benjamin Sergeant  
  
Print (1) packages used by a binary, and (2) the list of installed patches
related to these packages. If you have a binary that works with Solaris 10 update N, but doesn't with Solaris 10 update N-2, run this script on both platform and it will help you to find the patches you're looking for.
 
(1) is retrieved:

 * By using pldd(pid) on the process you want to trace to get a list of loaded
   shared library 
 * By retrieving in the main /var/sadm/install/contents database
   the list of package related to these shared libraries

(2) is retrieved by parsing the output of the showrev -p command, given as
input of this script