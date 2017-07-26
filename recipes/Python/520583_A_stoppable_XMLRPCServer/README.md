## A stoppable XMLRPCServer 
Originally published: 2007-05-17 02:04:48 
Last updated: 2007-05-17 02:04:48 
Author: Eli Golovinsky 
 
SimpleXMLRPCServer is too simple. It's serve_forever function doesn't allow it to be incorporated into anything that needs to be gracefully stopped at some point. This code extends SimpleXMLRPCServer with the server_until_stopped and stop_serving functions.