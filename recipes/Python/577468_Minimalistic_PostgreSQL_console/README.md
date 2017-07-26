## Minimalistic PostgreSQL console shell 
Originally published: 2010-11-25 15:24:26 
Last updated: 2011-11-30 13:43:28 
Author: ccpizza  
 
Primitive shell for running PostgreSQL quieries from console. Make sure you set the right connection settings in the script.\n\nAll queries are executed in autocommit mode.\n\nExample command line usage:\n\n    pg.py select * from mytable where oidh=1\n\n\nThe script recognizes a number of magic keywords:\n\n    pg.py show databases\n    pg.py show schemas\n    pg.py describe <table_name>