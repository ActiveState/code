## Lazy Traversal of Directed Graphs

Originally published: 2006-11-06 12:26:11
Last updated: 2006-11-06 20:34:39
Author: Vincent Kraeutler

The os.path.walk routine that ships with the python standard library is limited to traversing the file system tree. A generic traversal for arbitrary (directed) graphs with support for recursion limits and other accumulated partial results seems useful.