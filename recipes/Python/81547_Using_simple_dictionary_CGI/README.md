## Using a simple dictionary for CGI parameters

Originally published: 2001-10-13 09:51:15
Last updated: 2001-10-13 09:51:15
Author: Richie Hindle

Rather than using Python's cgi.FieldStorage class, a simple dictionary is enough for 99% of CGI scripts.  This recipe shows you how to convert a FieldStorage object into a simple dictionary.