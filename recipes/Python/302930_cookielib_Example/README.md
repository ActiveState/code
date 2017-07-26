## cookielib Example

Originally published: 2004-09-01 03:51:38
Last updated: 2004-12-28 11:26:41
Author: Michael Foord

cookielib is a library new to Python 2.4\nPrior to Python 2.4 it existed as ClientCookie, but it's not a drop in replacement - some of the function of ClientCookie has been moved into urllib2.\n\nThis example shows code for fetching URIs (with cookie handling - including loading and saving) that will work unchanged on :\na machine with python 2.4 (and cookielib)\na machine with ClientCookie installed\na machine with neither\n(Obviously on the machine with neither the cookies won't be handled or saved).\n\nWhere either cookielib or ClientCookie is available the cookies will be saved in a file.\nIf that file exists already the cookies will first be loaded from it.\nThe file format is a useful plain text format and the attributes of each cookie is accessible in the Cookiejar instance (once loaded).\n\nThis may be helpful to those just using ClientCookie as the ClientCookie documentation doesn't appear to document the LWPCookieJar class which is needed for saving and loading cookies.