## Efficient database trees 
Originally published: 2004-04-28 03:32:24 
Last updated: 2004-04-28 10:48:08 
Author: Ben Young 
 
Sometimes it can be hard to work out a way of efficiently representing a tree in the database. Combining modified preorder tree traversal with a parent child model allows most common queries to be represented in a single sql query. This example uses MySQLdb, but can easy be changed to use any DBI compatable module.