import socket
from select import select
from SimpleXMLRPCServer import SimpleXMLRPCServer

class XMLRPCServer(SimpleXMLRPCServer):
    """
    A variant of SimpleXMLRPCServer that can be stopped.
    """
    def __init__(self, *args, **kwargs):
        SimpleXMLRPCServer.__init__(self, *args, **kwargs)
        self.logRequests = 0
        self.closed = False
    
    def serve_until_stopped(self):
        self.socket.setblocking(0)
        while not self.closed:
            self.handle_request()        
            
    def stop_serving(self):
        self.closed = True
    
    def get_request(self):
        inputObjects = []
        while not inputObjects and not self.closed:
            inputObjects, outputObjects, errorObjects = \
                select([self.socket], [], [], 0.2)
            try:
                return self.socket.accept()
            except socket.error:
                raise
