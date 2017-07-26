## PyDbLite, a small in-memory database engine  
Originally published: 2006-06-02 13:21:13  
Last updated: 2011-07-18 19:36:04  
Author: Pierre Quentel  
  
A small, fast, in-memory database management program

The database object supports the iterator protocol, so that requests can be expressed with list comprehensions or generator expressions instead of SQL. The equivalent of :

    cursor.execute("SELECT name FROM table WHERE age=30")
    rows = cursor.fetchall()

is :

    rows = table(age=30)

The module stores data in a cPickled file. Records are indexed by a unique record identifier, that can be used for direct access. Since operations are processed in memory they are extremely fast, nearly as fast as SQLite in the few tests I made, and MUCH faster than other pure-Python modules such as Gadfly or KirbyBase. An index can be created on a field to even speed up selections

Concurrency control is supported by a version number set for each record

Complete documentation is [here](http://www.pydblite.net)