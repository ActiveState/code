## Manage hashes in database files.  
Originally published: 2012-03-18 11:45:09  
Last updated: 2012-03-24 14:40:24  
Author: eysi   
  
This module can be used to calculate file hashes, store them in a database file
and retrieve them at a later date.

It uses the files modify time stamp to know if it can use the hash stored in
the db or if it has to re-calculate it. So the user will not have to worry
about the hash being incorrect if the file changes in between runs.
