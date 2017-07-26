## Encoding Unicode data for XML and HTML

Originally published: 2004-09-07 08:07:56
Last updated: 2004-09-08 13:57:04
Author: David Goodger

The "xmlcharrefreplace" encoding error handler was introduced in Python 2.3.  It is very useful when encoding Unicode data for HTML and other XML applications with limited (but popular) encodings like ASCII or ISO-Latin-1.  The following code contains a trivial function "encode_for_xml" that illustrates the "xmlcharrefreplace" error handler, and a function "_xmlcharref_encode" which emulates "xmlcharrefreplace" for Python pre-2.3.\n\nAn HTML demonstration is included.  Put the code into a file, run it with Python, and redirect the output to a .html file.  Open the output file in a browser to see the results.\n\nA variation of this code is used in the Docutils project.  The original idea for backporting "xmlcharrefreplace" to pre-2.3 Python was from Felix Wiemann.