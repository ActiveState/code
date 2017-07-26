###Reading large files from zip archive

Originally published: 2009-08-17 10:19:20
Last updated: 2009-08-17 10:24:40
Author: Volker S.

The standard zipfile module provides only a method to extract the entire content of a file from within a zip-file.\nThis extension adds a generator method to iterate over the lines in a file, avoiding the memory problems.\n