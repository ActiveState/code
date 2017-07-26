###Reverse engineer MS Access/Jet databases

Originally published: 2001-03-15 17:53:23
Last updated: 2004-09-16 19:24:51
Author: Matt Keranen

Reads the structure of a Jet (Microsoft Access .MDB) database file, and creates the SQL DDL necessary to recreate the structure.\n\nOriginally written to aid in migrating Jet databases to larger RDBMS systems, through E/R design tools, when the supplied "import" routines missed objects like indexes and FKs.\n\nA first experiment in Python, that became an often used tool.