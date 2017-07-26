## urrlib2 opener for SSL proxy (CONNECT method)Originally published: 2005-11-16 06:26:42 
Last updated: 2005-11-16 15:04:54 
Author: Alessandro Budai 
 
This small module builds an urllib2 opener that can be used to make a connection through a proxy using the http CONNECT method (that can be used to proxy SSLconnections).\nThe current urrlib2 seems to not support this method.