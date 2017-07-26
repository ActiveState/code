'''Module for running simple proxies.

This module provides a single class that can build
proxy objects capable of being started and stopped.'''

__version__ = '1.0'

import select as _select
import socket as _socket
import sys as _sys
import thread as _thread

################################################################################

class Proxy:

    'Proxy(bind, connect) -> Proxy'

    FAMILY = _socket.AF_INET
    TYPE = _socket.SOCK_STREAM
    BUFFERSIZE = 2 ** 12

    def __init__(self, bind, connect):
        'Initialize the Proxy object.'
        self.__bind = bind
        self.__connect = connect
        self.__status = False
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Proxy object.'
        self.__lock.acquire()
        self.__status = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__proxy, ())
        self.__lock.release()

    def stop(self):
        'Stop the Proxy object.'
        self.__lock.acquire()
        self.__status = False
        self.__lock.release()

    def __proxy(self):
        'Private class method.'
        proxy = _socket.socket(self.FAMILY, self.TYPE)
        proxy.bind(self.__bind)
        proxy.listen(5)
        while True:
            client = proxy.accept()[0]
            self.__lock.acquire()
            if not self.__status:
                proxy.close()
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            server = _socket.socket(self.FAMILY, self.TYPE)
            server.connect(self.__connect)
            _thread.start_new_thread(self.__serve, (client, server))

    def __serve(self, client, server):
        'Private class method.'
        pairs = {client: server, server: client}
        while pairs:
            read, write, error = _select.select(pairs.keys(), [], [])
            for socket in read:
                string = socket.recv(self.BUFFERSIZE)
                if string:
                    pairs[socket].sendall(string)
                else:
                    pairs[socket].shutdown(_socket.SHUT_WR)
                    socket.shutdown(_socket.SHUT_RD)
                    del pairs[socket]
        client.close()
        server.close()

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
