# Guyon Morée
# http://gumuz.looze.net/

import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
 
# Threaded mix-in
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass
 
# Example class to be published
class TestObject:
    def pow(self, x, y):
        return pow(x, y)
 
    def add(self, x, y) :
        return x + y
 
    def divide(self, x, y):
        return float(x) / float(y)
 
 
# Instantiate and bind to localhost:8080
server = AsyncXMLRPCServer(('', 8080), SimpleXMLRPCRequestHandler)
 
# Register example object instance
server.register_instance(TestObject())
 
# run!
server.serve_forever()
