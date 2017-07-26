## Pretty Printing of Database Cursor Contents

Originally published: 2001-10-11 19:48:37
Last updated: 2003-01-28 15:29:03
Author: Steve Holden

One of the problems of dealing with databases is presenting the result of a query when you may not know much about the data. This recipe uses the cursor's description attribute to try and provide appropriate headings, and optionally examines each output row to ensure column widths are adequate.