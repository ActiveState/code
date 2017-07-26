## Sort extremely large and/or binary files in Python

Originally published: 2008-02-18 18:46:39
Last updated: 2008-02-18 18:46:39
Author: Jeremy Mortis

This recipe can be used to sort very large files (millions of records) in Python.  No record termination character is required, hence a record may contain embedded binary data, newlines, etc.  You can specify how many temporary files to use and where they are located.