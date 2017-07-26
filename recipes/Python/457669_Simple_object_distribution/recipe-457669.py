# Object adaptor for the client
import communication
from socket import *

class ObjectAdaptor(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send(self, *args):
        communication.send(self.channel, args)

    def receive(self):
        return communication.receive(self.channel)

    def remoteInvoke(self, fun, *args):
        method = (fun.func_name, ) + args
        self.channel = socket(AF_INET, SOCK_STREAM, 0)
        self.channel.connect((self.ip, self.port))
        self.send(*method)
        result = self.receive()
        self.channel.close()
        return result[0]

# Object server for the actual object
import communication
import types
from socket import *

class ObjectServer(object):
    def __init__(self, ip, port):
        self.channel = socket(AF_INET, SOCK_STREAM, 0)
        self.channel.bind((ip, port))
        self.channel.listen(50)
        self.info = self.channel.getsockname()

    def send(self, client, *args):
        communication.send(client, args)

    def receive(self, client):
        return communication.receive(client)

    def getInfo(self):
        return self.info

    def dispatch(self, invoke, client):
        dict = self.__class__.__dict__
        method = invoke[0]
        if (method in dict.keys() and type(dict[method]) == types.FunctionType):
            method = dict[method]
            params = invoke[1:]
            result = method(self, *params)
            self.send(client, result)

    def start(self):
        while (1):
            client = self.channel.accept()[0]
            invoke = self.receive(client)
            self.dispatch(invoke, client)

# Communication code (the import communcation statements)
from socket import htonl, ntohl
import cPickle
import struct

marshall = cPickle.dumps
unmarshall = cPickle.loads


def send(channel, *args):
    buf = marshall(args)
    value = htonl(len(buf))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buf)

def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    size = ntohl(struct.unpack("L", size)[0])
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
        return unmarshall(buf)[0]

# Echo server sample
class EchoServer(ObjectServer):
    def __init__(self, ip, port):
        ObjectServer.__init__(self, ip, port)
    def echo(self, msg):
        return "Message received: %s" % msg
es = EchoServer("127.0.0.1", 10000)
es.start()

# Echo client sample
class EchoClient(ObjectAdaptor):
    def __init__(self, ip, port):
        ObjectAdaptor.__init__(self, ip, port)
    def echo(self, msg):
        return self.remoteInvoke(self.echo, msg)
ec = EchoClient("127.0.0.1", 10000)
print ec.echo("Hello World!")
