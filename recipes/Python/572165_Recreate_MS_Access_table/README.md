## Recreate MS Access table in SQLite  
Originally published: 2008-04-23 13:44:57  
Last updated: 2008-07-01 16:22:39  
Author: K. Killebrew  
  
A function to create and load a table in SQLite from a Microsoft Jet table, using DAO.  Also recreates indexes.  Fetches and loads records in blocks with a default size of 1000 rows.