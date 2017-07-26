## using xmlrpc with authenticated proxy server 
Originally published: 2007-07-03 23:42:04 
Last updated: 2007-07-03 23:42:04 
Author: Vaibhav Bhatia 
 
To access an XML-RPC server through a proxy which requires authentication, you need to define a custom transport. the custom transport mentioned in the python docs, allows only proxy server's which do not require authentication. (http://docs.python.org/lib/xmlrpc-client-example.html). Have tried to use urllib which has support for proxy server and added the headers required for authentication. Idea to use urllib was taken from this thread (http://mail.python.org/pipermail/python-list/2001-July/098183.html)