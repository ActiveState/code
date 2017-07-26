## To Find out the  Hard Disk Size,Free Space and Used Space of a Networked Computer  
Originally published: 2001-07-31 12:39:56  
Last updated: 2001-07-31 12:39:56  
Author: Ratnakar Malla  
  
This module , does not take any i/p file. It first does a net view
command , and gets the list of computers in the domain. Connects
to each computer , performs size check and returns the size of the
harddisk. Please note that , the file and dir sizes are caluclated
in DOS. Windows performs a sort of approximation. So there will be
slight  variation in the amount of space reported by DOS and Windows.
If I am not wrong DOS gives u the best values.