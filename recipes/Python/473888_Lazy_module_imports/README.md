###Lazy module imports

Originally published: 2006-02-13 13:26:00
Last updated: 2006-02-14 18:51:46
Author: David Christian

The following recipe allows you to delay import module statements until the module is actually needed.  This can lead to a much faster startup time for large programs with lots of imports.  Installing is easy, just call importer.install().