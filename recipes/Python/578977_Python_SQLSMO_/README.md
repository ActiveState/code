## Python SQLSMO Originally published: 2014-12-06 02:48:48 
Last updated: 2015-03-28 16:58:11 
Author: Jorge Besada 
 
I needed a Python library equivalent to the SQL Server Management Objects (SMO) and did not find it, so I created my own version. It does not follow the standard SMO objects names. So far it has a set of basic functionality: to make backups, restores with move, sync logins for restored databases, check disk space. I included a good sized testing harness to get you going. This version uses sqlcmd for connectivity. I use this SQLSMO library as an imported module in several of my Python applications.\nIt has been tested with SQL 2012 and SQL 2014, it should function with versions down to 2005.