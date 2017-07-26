## Simple HTTP processor for urllib2, or ClientCookie to track HTTP request and responses similar to the Firefox extension LiveHTTPHeadersOriginally published: 2005-09-19 11:53:35 
Last updated: 2005-09-19 23:51:30 
Author: John Pywtorak 
 
Say you need to make sure the HTTP headers to and from the server are right?  Or you just want to track them like using Firefox and LiveHTTPHeaders.  Use this custom processor to watch them.  Note that I used the ClientCookie package, but this should work with urllib2 without ClientCookie.  It should also be adaptable to Python 2.4's cookielib.