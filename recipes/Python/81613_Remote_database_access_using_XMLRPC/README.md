## Remote database access using XML-RPC and SOAP.

Originally published: 2001-10-14 00:53:45
Last updated: 2001-11-01 00:42:22
Author: Graham Dumpleton

Shows how to remotely access a database via a web service supporting XML-RPC and SOAP protocols. The example uses the MySQLdb module, but should be easily customised to any database with Python module adhering to the Python DB API. The web service interface provides the ability to make a self contained query, or allows the creation of a distinct database cursor to service a series of queries or updates without other clients interfering. Cursors automatically expire and delete themselves after a set period of inactivity if not explicitly closed.