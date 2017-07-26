###Get attributes of an object in MS Active Directory

Originally published: 2004-09-03 14:41:32
Last updated: 2004-09-03 14:41:32
Author: John Nielsen

Sometimes it is useful to know what attributes are available to you for an object in active directory. You cannot ask the object directly for that, instead you need to use the schema of the object. All of this is done with python's COM support using win32com. By default only attributes that have values are returned.