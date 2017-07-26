"""A generic, multi-protocol asynchronous server

Usage :
- create a server on a specific host and port : server = Server(host,port)
- call the loop() function, passing it the server and the class used to 
manage the protocol (a subclass of ClientHandler) : loop(server,ProtocolClass)

An example of protocol class is provided, LengthSepBody : the client sends
the message length, the line feed character and the message body
"""

import cStringIO
import socket
import select

# the dictionary holding one client handler for each connected client
# key = client socket, value = instance of (a subclass of) ClientHandler
client_handlers = {}

# =======================================================================
# The server class. Creating an instance starts a server on the specified
# host and port
# =======================================================================
class Server:

    def __init__(self,host='localhost',port=80):
        self.host,self.port = host,port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind((host,port))
        self.socket.listen(5)

# =====================================================================
# Generic client handler. An instance of this class is created for each
# request sent by a client to the server
# =====================================================================
class ClientHandler:

    blocksize = 2048

    def __init__(self, server, client_socket, client_address):
        self.server = server
        self.client_address = client_address
        self.client_socket = client_socket
        self.client_socket.setblocking(0)
        self.host = socket.getfqdn(client_address[0])
        self.incoming = '' # receives incoming data
        self.writable = False
        self.close_when_done = True
 
    def handle_error(self):
        self.close()
        
    def handle_read(self):
        """Reads the data received"""
        try:
            buff = self.client_socket.recv(1024)
            if not buff:  # the connection is closed
                self.close()
            # buffer the data in self.incoming
            self.incoming += buff #.write(buff)
            self.process_incoming()
        except socket.error:
            self.close()

    def process_incoming(self):
        """Test if request is complete ; if so, build the response
        and set self.writable to True"""
        if not self.request_complete():
            return
        self.response = self.make_response()
        self.writable = True

    def request_complete(self):
        """Return True if the request is complete, False otherwise
        Override this method in subclasses"""
        return True
    
    def make_response(self):
        """Return the list of strings or file objects whose content will
        be sent to the client
        Override this method in subclasses"""
        return ["xxx"]

    def handle_write(self):
        """Send (a part of) the response on the socket
        Finish the request if the whole response has been sent
        self.response is a list of strings or file objects
        """
        # get next piece of data from self.response
        buff = ''
        while self.response and not buff:
            if isinstance(self.response[0],str):
                buff = self.response.pop(0)
            else:
                buff = self.response[0].read(self.blocksize)
                if not buff:
                    self.response.pop(0)
        if buff:
            try:
                self.client_socket.sendall(buff)
            except socket.error:
                self.close()
            if self.response:
                return
        # nothing left in self.response
        if self.close_when_done:
            self.close() # close socket
        else:
            # reset for next request
            self.writable = False
            self.incoming = ''
    
    def close(self):
        del client_handlers[self.client_socket]
        self.client_socket.close()

# ==============================================================
# A protocol with message length + line feed (\n) + message body
# This implementation just echoes the message body
# ==============================================================
class LengthSepBody(ClientHandler):

    def request_complete(self):
        """The request is complete if the separator is present and the
        number of bytes received equals the specified message length"""
        recv = self.incoming.split('\n',1)
        if len(recv)==1 or len(recv[1]) != int(recv[0]):
            return False
        self.msg_body = recv[1]
        return True

    def make_response(self):
        """Override this method to actually process the data"""
        return [self.msg_body]

# ============================================================================
# Main loop, calling the select() function on the sockets to see if new 
# clients are trying to connect, if some clients have sent data and if those
# for which the response is complete are ready to receive it
# For each event, call the appropriate method of the server or of the instance
# of ClientHandler managing the dialog with the client : handle_read() or 
# handle_write()
# ============================================================================
def loop(server,handler,timeout=30):
    while True:
        k = client_handlers.keys()
        # w = sockets to which there is something to send
        # we must test if we can send data
        w = [ cl for cl in client_handlers if client_handlers[cl].writable ]
        # the heart of the program ! "r" will have the sockets that have sent
        # data, and the server socket if a new client has tried to connect
        r,w,e = select.select(k+[server.socket],w,k,timeout)
        for e_socket in e:
            client_handlers[e_socket].handle_error()
        for r_socket in r:
            if r_socket is server.socket:
                # server socket readable means a new connection request
                try:
                    client_socket,client_address = server.socket.accept()
                    client_handlers[client_socket] = handler(server,
                        client_socket,client_address)
                except socket.error:
                    pass
            else:
                # the client connected on r_socket has sent something
                client_handlers[r_socket].handle_read()
        w = set(w) & set(client_handlers.keys()) # remove deleted sockets
        for w_socket in w:
            client_handlers[w_socket].handle_write()
