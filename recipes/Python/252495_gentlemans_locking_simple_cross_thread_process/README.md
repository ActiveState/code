## gentleman's locking (simple cross thread and process locking)  
Originally published: 2003-12-04 09:14:48  
Last updated: 2003-12-04 09:14:48  
Author: John Nielsen  
  
Cross-platform locking that works across multiple threads and processes can be complicated. A simple solution is to use 2 level locking based off of mkdir (which  fails on all attempts except the first). It works across threads and processes (or even servers), since only one will get to do mkdir.