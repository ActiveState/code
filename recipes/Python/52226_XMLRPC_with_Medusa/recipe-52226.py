# xmlrpc_server.py
from socket import gethostname
from medusa.xmlrpc_handler import xmlrpc_handler
from medusa.http_server import http_server
from medusa import asyncore

class xmlrpc_server(xmlrpc_handler):
    """The xmlrpc_server class demonstrates a simple implementation 
    of Userland's XML-RPC protocol.  You must download and install
    xmlrpclib and Medusa to run this code.

    Obtain Sam Rushing's Medusa library from http://www.nightmare.com
    Download Fredrik Lundh's xmlrpclib at http://www.pythonware.com"""

    def __init__(self, host=None, port=8182):
        if host is None:
            host = gethostname()
        hs = http_server(host, port)
        hs.install_handler(self)
        asyncore.loop()

    def add(self, op1, op2):
        return op1 + op2

    def call(self, method, params):
        print "call method: %s, params: %s" % (method, str(params))
        if method == 'add':
            return apply(self.add, params)
        return "method not found: %s" % method

if __name__ == '__main__':
    server = xmlrpc_server()

---

# xmlrpc_client.py
from socket import gethostname
from xmlrpclib import Transport, dumps

class xmlrpc_connection:
    """The xmlrpc_connection class tests the xmlrpc_server.  You must 
    download and install the medusa and xmlrpclib libraries to run 
    this code:  http://www.nightmare.com  http://www.pythonware.com"""

    def __init__(self, host=None, port=8182):
        if host is None:
            host = gethostname()
        self.host = "%s:%s" % (host, port)
        self.transport = Transport()

    def remote(self, method, params=()):
        """remote invokes the server with the method name and an 
        optional set of parameters.  The return value is always a
        tuple."""

        response = self.transport.request(self.host, 
                                          '/RPC2',
                                          dumps(params, method))
        return response

if __name__ == '__main__':
    connection = xmlrpc_connection()
    (answer,) = connection.remote("add", (40, 2))
    print "The answer is:", answer
