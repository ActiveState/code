## Manage hashes in database files.  
Originally published: 2012-03-20 01:08:15  
Last updated: 2012-03-20 01:08:15  
Author: cathy park  
  
This module can be used to calculate file hashes, store them in a database file\nand retrieve them at a later date.\n\nIt uses the files modify time stamp to know if it can use the hash stored in\nthe db or if it has to re-calculate it. So the user will not have to worry\nabout the hash being incorrect if the file changes in between runs.\n