###Handling Deeply Nested/Recursive Data

Originally published: 2004-08-29 19:18:24
Last updated: 2006-04-26 06:15:08
Author: Simon Burton

Common python services such as pickle, deepcopy and comparison tests either fail entirely or do not scale for highly recursive data structures. This recipe presents a reversible "flatten" transformation that allows for such operations.