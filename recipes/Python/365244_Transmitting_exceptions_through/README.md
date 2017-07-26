## Transmitting exceptions through XML-RPCOriginally published: 2005-01-31 17:37:28 
Last updated: 2005-01-31 17:37:28 
Author: A.M. Kuchling 
 
Python's xmlrpclib only raises the xmlrpclib.Fault exception, but it can be convenient to allow more different kinds of exceptions to be raised.  This recipe provides a customized subclass of xmlrpclib.ServerProxy that looks for Fault exceptions where the message is of the form <exception name>:<message>, and raises the corresponding exception.