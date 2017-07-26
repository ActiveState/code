## cookielib Example  
Originally published: 2004-09-01 03:51:38  
Last updated: 2004-12-28 11:26:41  
Author: Michael Foord  
  
cookielib is a library new to Python 2.4
Prior to Python 2.4 it existed as ClientCookie, but it's not a drop in replacement - some of the function of ClientCookie has been moved into urllib2.

This example shows code for fetching URIs (with cookie handling - including loading and saving) that will work unchanged on :
a machine with python 2.4 (and cookielib)
a machine with ClientCookie installed
a machine with neither
(Obviously on the machine with neither the cookies won't be handled or saved).

Where either cookielib or ClientCookie is available the cookies will be saved in a file.
If that file exists already the cookies will first be loaded from it.
The file format is a useful plain text format and the attributes of each cookie is accessible in the Cookiejar instance (once loaded).

This may be helpful to those just using ClientCookie as the ClientCookie documentation doesn't appear to document the LWPCookieJar class which is needed for saving and loading cookies.