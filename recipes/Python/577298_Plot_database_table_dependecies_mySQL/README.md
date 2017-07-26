## Plot database table dependecies for a mySQL database

Originally published: 2010-07-09 12:00:09
Last updated: 2010-07-10 08:14:09
Author: Noufal Ibrahim

The following snippet will output a spec suitable for the graphviz dot program. It will go through the database specified and for all the tables that start with any of the names in `table_prefixes`, it will create a dependency graph. A dependency in this context is when a field of one table has a foreign key reference to another. The edges are labelled with the actual field names. \n\nIt can be used like this\n\n    python deps.py | dot -Tpng | display\n\nThis requires the InnoDB engine (i.e. something that honours foreign keys. MyISAM doesn't do so).