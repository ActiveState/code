## Global database configuration and context aware connection pool extention for psycopg2 
Originally published: 2010-02-26 02:53:51 
Last updated: 2010-02-26 02:57:49 
Author: Valentine Gogichashvili 
 
This extention makes it possible to hold a global configuration of all needed database, and access this databases using a special context aware named connection pools. The context can help to automate transaction commits and rollbacks and return special connection cursors in the context. \nSee module and class docs for more information.