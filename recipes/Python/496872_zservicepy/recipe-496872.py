'''Module for networked function calls.

This module provides two server classes and a single client
class that can be used for function calls across a network.'''

__version__ = 1.0

################################################################################

import cPickle
import Queue
import socket
import thread
import z_string
import z_sync

class Protocol:

    'Protocol() -> new Protocol object'

    SEND_SIZE = 1024
    RECV_SIZE = 4096

    def send(self, sock, obj):
        'Sends one Python object over a socket.'
        self.sendall(sock, '\x00'.join([z_string.string_code(string) for string in z_string.partition(cPickle.dumps(obj, -1), self.SEND_SIZE)]))

    def recv(self, sock):
        'Receives one Python object over a socket.'
        return cPickle.loads(''.join([z_string.code_string(code) for code in self.recvall(sock).split('\x00')]))

    def sendall(self, sock, string):
        'Sends an entire string over a socket.'
        sock.sendall(string)
        sock.shutdown(socket.SHUT_WR)

    def recvall(self, sock):
        'Receives an entire string over a socket.'
        string = str()
        while True:
            buf = sock.recv(self.RECV_SIZE)
            if buf:
                string += buf
            else:
                sock.shutdown(socket.SHUT_RD)
                return string

################################################################################

class Client(Protocol):

    'Client(host, port) -> new Client'

    def __init__(self, host, port):
        'x.__init__(...) initializes x'
        self.address = host, port

    def __call__(self, name, *args, **kwargs):
        'Allows a client object to be called as a function.'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.address)
        self.send(sock, (name, args, kwargs))
        return self.recv(sock)

class Server(Protocol):

    'Server(host, port) -> new Server'

    def __init__(self, host, port):
        'x.__init__(...) initializes x'
        self.services = dict()
        thread.start_new_thread(self.server, (host, port))

    def server(self, host, port):
        'Acts as a server for receiving connections.'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        while True:
            thread.start_new_thread(self.client, (sock.accept()[0],))

    def client(self, sock):
        'Takes care of incoming connections.'
        name, args, kwargs = self.recv(sock)
        try:
            self.send(sock, self.services[name](*args, **kwargs))
        except:
            self.send(sock, None)

    def add_service(self, name, service):
        'Adds a new function that the server can execute.'
        self.services[name] = service

class Sync_Server(Server):

    'Sync_Server(host, port) -> new Sync_Server'

    def __init__(self, host, port):
        'x.__init__(...) initializes x'
        self.services = dict()
        self.queue = Queue.Queue()
        thread.start_new_thread(self.server, (host, port))
        thread.start_new_thread(self.processor, ())

    def client(self, sock):
        'Takes care of incoming connections.'
        name, args, kwargs = self.recv(sock)
        sync = z_sync.Sync(2)
        item = [name, args, kwargs, sync]
        self.queue.put(item)
        sync.sync()
        self.send(sock, item[4])

    def processor(self):
        'Processes clients\' requests in sequential order.'
        while True:
            item = self.queue.get()
            name, args, kwargs, sync = item
            try:
                item.append(self.services[name](*args, **kwargs))
            except:
                item.append(None)
            sync.sync()

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
