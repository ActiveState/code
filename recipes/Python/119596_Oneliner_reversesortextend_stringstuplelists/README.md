## "Oneliner" for reverse/sort/extend strings/tuple/lists NOT in placeOriginally published: 2002-04-04 16:40:10 
Last updated: 2002-04-07 03:51:55 
Author: H. Krekel 
 
If you like obfuscated but powerful Oneliners you will really enjoy this one.\nIt allows to use reverse, sort and extent "on the fly" with tuples, strings or list types.\nIt returns a new instance of the same type as the input type. Extending a tuple results in\na new tuple. Sorting a string results in a new string and so on. Thanks to Patrick\nMaupin since version 1.2 it handles Null-Strings and tuples correctly.\n\nThough the functionality can be expressed in a 290-character "Oneliner" i recommend\nthat you use the longer 15-line code (at the end) as it is more understandable and "pythonic".