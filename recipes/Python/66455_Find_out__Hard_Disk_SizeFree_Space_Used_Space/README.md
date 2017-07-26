###To Find out the  Hard Disk Size,Free Space and Used Space of a Networked Computer

Originally published: 2001-07-31 12:39:56
Last updated: 2001-07-31 12:39:56
Author: Ratnakar Malla

This module , does not take any i/p file. It first does a net view\ncommand , and gets the list of computers in the domain. Connects\nto each computer , performs size check and returns the size of the\nharddisk. Please note that , the file and dir sizes are caluclated\nin DOS. Windows performs a sort of approximation. So there will be\nslight  variation in the amount of space reported by DOS and Windows.\nIf I am not wrong DOS gives u the best values.