## stupid trick: mimicking the python cgi library's FieldStorage() object for command line debugingOriginally published: 2015-06-18 19:49:26 
Last updated: 2015-06-18 20:46:32 
Author: Jon Crump 
 
create dictionary-like object that mimics the cgi.FieldStorage() object having both a `.value` property, and a `.getvalue()` method