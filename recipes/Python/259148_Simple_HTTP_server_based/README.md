## Simple HTTP server based on asyncore/asynchatOriginally published: 2004-01-01 10:31:00 
Last updated: 2005-10-16 08:26:59 
Author: Pierre Quentel 
 
A simple HTTP Server, intended to be as simple as the standard module SimpleHTTPServer, built upon the asyncore/asynchat modules (uses non-blocking sockets). Provides a Server (copied from medusa http_server) and a RequestHandler class. RequestHandler handles both GET and POST methods and inherits SimpleHTTPServer.SimpleHTTPRequestHandler\n\nIt can be easily extended by overriding the handle_data() method in the RequestHandler class