## Colorize Python source using the built-in tokenizerOriginally published: 2001-03-22 16:51:12 
Last updated: 2001-04-06 23:05:53 
Author: Jürgen Hermann 
 
This code is part of MoinMoin (http://moin.sourceforge.net/) and converts Python source code to HTML markup, rendering comments, keywords, operators, numeric and string literals in different colors.\n\nIt shows how to use the built-in keyword, token and tokenize modules to scan Python source code and re-emit it with no changes to its original formatting (which is the hard part).\n\nThe test code at the bottom of the module formats itself and launches a browser with the result.