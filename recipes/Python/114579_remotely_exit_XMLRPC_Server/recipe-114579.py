from SimpleXMLRPCServer import *

class MyServer(SimpleXMLRPCServer):

    def serve_forever(self):
	self.quit = 0
	while not self.quit:
	    self.handle_request()


def kill():
    server.quit = 1
    return 1
    

server = MyServer(('127.0.0.1', 8000))
server.register_function(kill)

server.serve_forever()
