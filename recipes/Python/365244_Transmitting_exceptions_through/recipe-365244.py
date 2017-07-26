"""xmlrpc

Specialized XML-RPC support that can raise exceptions across the
client/server boundary.

To use this, just create an instance of Server and call methods on it.
Special exceptions raised on the server will cause the same
exceptions to be triggered on the client side.
"""

import xmlrpclib
import re

__all__ = ['Server']

# List of exceptions that are allowed.  Only exceptions listed here will be reconstructed
# from an xmlrpclib.Fault instance.
allowed_errors = [ValueError, TypeError]

error_pat = re.compile('(?P<exception>[^:]*):(?P<rest>.*$)')

class ExceptionUnmarshaller (xmlrpclib.Unmarshaller):
    def close(self):
        # return response tuple and target method
        if self._type is None or self._marks:
            raise xmlrpclib.ResponseError()
        if self._type == "fault":
            d = self._stack[0]
            m = error_pat.match(d['faultString'])
            if m:
                exception_name = m.group('exception')
                rest = m.group('rest')
                for exc in allowed_errors:
                    if exc.__name__ == exception_name:
                        raise exc(rest)

            # Fall through and just raise the fault
            raise xmlrpclib.Fault(**d)
        return tuple(self._stack)

class ExceptionTransport (xmlrpclib.Transport):
    # Override user-agent if desired
    ##user_agent = "xmlrpc-exceptions/0.0.1"

    def getparser (self):
        # We want to use our own custom unmarshaller
        unmarshaller = ExceptionUnmarshaller()
        parser = xmlrpclib.ExpatParser(unmarshaller)
        return parser, unmarshaller

# Alternatively you can just use the regular ServerProxy and pass it
# an instance of ExceptionTransport.

class Server (xmlrpclib.ServerProxy):
    def __init__ (self, *args, **kwargs):
        # Supply our own transport
        kwargs['transport'] = ExceptionTransport()
        xmlrpclib.ServerProxy.__init__(self, *args, **kwargs)

if __name__ == '__main__':
    s = Server('http://localhost:8000')
    print s.exception()

# Sample code for a server that returns exceptions in the right format
import sys, xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def exception ():
    try:
        # Put code here, call other functions
        int('a')
    except Exception, exc:
        raise xmlrpclib.Fault(1, '%s:%s' % (exc.__class__.__name__, exc) )

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(exception)
server.serve_forever()
