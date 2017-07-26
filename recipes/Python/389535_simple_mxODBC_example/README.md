## simple mx.ODBC exampleOriginally published: 2005-02-25 07:16:43 
Last updated: 2005-02-25 07:16:43 
Author: John Nielsen 
 
Mx.odbc is cross platform and very fast, I have used it to go through a few hundred thousand rows of an access database in seconds where pure ADO would take 30 min (or 3 min if you use the ADO type library). Here is a simple example of how to talk to a database, in this case an access file, get the columns of a table and get data from the table.