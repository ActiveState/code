import SimpleXMLRPCServer
import string,socket

accessList=(
    '127.0.0.1',
    '192.168.0.15'
    )

class Server(SimpleXMLRPCServer.SimpleXMLRPCServer):
    def __init__(self,*args):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self,(args[0],args[1]))
        
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SimpleXMLRPCServer.SimpleXMLRPCServer.server_bind(self)

    def verify_request(self,request, client_address):
        if client_address[0] in accessList:
            return 1
        else:
            return 0
        
class xmlrpc_registers:
    def __init__(self):
        self.python_string = string
        
    def add(self, x, y):
        return x + y

    def mult(self,x,y):
        return x*y

    def div(self,x,y):
        return x//y

if __name__ == "__main__":
    server = Server('',8000)
    server.register_instance(xmlrpc_registers())
    server.serve_forever()
