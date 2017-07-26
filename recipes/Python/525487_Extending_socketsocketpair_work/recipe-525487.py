from socket import *
import threading

try:
    pairfamily = AF_UNIX
except NameError:
    pairfamily = AF_INET

def SocketPair(family=pairfamily, type_=SOCK_STREAM, proto=IPPROTO_IP):
    """Wraps socketpair() to support Windows using local ephemeral ports"""
    try:
        sock1, sock2 = socketpair(family, type_, proto)
        return (sock1, sock2)
    except NameError:
        listensock = socket(family, type_, proto)
        listensock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        listensock.bind( ('localhost', 0) )
        iface, ephport = listensock.getsockname()
        listensock.listen(1)

        sock1 = socket(family, type_, proto)
        connthread = threading.Thread(target=pairConnect, args=[sock1, ephport])
        connthread.setDaemon(1)
        connthread.start()
        sock2, sock2addr = listensock.accept()
        listensock.close()
        return (sock1, sock2)

def pairConnect(sock, port):
    sock.connect( ('localhost', port) )
