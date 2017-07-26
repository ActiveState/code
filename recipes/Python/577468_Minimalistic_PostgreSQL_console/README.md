## Minimalistic PostgreSQL console shell  
Originally published: 2010-11-25 15:24:26  
Last updated: 2011-11-30 13:43:28  
Author: ccpizza   
  
Primitive shell for running PostgreSQL quieries from console. Make sure you set the right connection settings in the script.

All queries are executed in autocommit mode.

Example command line usage:

    pg.py select * from mytable where oidh=1


The script recognizes a number of magic keywords:

    pg.py show databases
    pg.py show schemas
    pg.py describe <table_name>