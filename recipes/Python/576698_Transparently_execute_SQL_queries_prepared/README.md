###Transparently execute SQL queries as prepared statements with Postgresql

Originally published: 2009-03-22 18:21:07
Last updated: 2009-03-23 07:30:07
Author: Michael Palmer

This recipe defines a mixin class for DBAPI cursors that gives them an 'executeps' method. This method transparently converts any SQL query into a prepared statement, which gets cached and executed instead of the original query.