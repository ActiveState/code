import xmlrpclib
from twisted.web import xmlrpc, server, http
from twisted.internet import defer, protocol, reactor

Fault = xmlrpclib.Fault

class TwistedRPCServer(xmlrpc.XMLRPC):
    """ A class which works as an XML-RPC server with
    HTTP basic authentication """

    def __init__(self, user='', password=''):
        self._user = user
        self._password = password
        self._auth = (self._user !='')
        xmlrpc.XMLRPC.__init__(self)
        
    def xmlrpc_echo(self, x):
        return x

    def xmlrpc_ping(self):
        return 'OK'

    def render(self, request):
        """ Overridden 'render' method which takes care of
        HTTP basic authorization """
        
        if self._auth:
            cleartext_token = self._user + ':' + self._password
            user = request.getUser()
            passwd = request.getPassword()
        
            if user=='' and passwd=='':
                request.setResponseCode(http.UNAUTHORIZED)
                return 'Authorization required!'
            else:
                token = user + ':' + passwd
                if token != cleartext_token:
                    request.setResponseCode(http.UNAUTHORIZED)
                    return 'Authorization Failed!'

        request.content.seek(0, 0)
        args, functionPath = xmlrpclib.loads(request.content.read())
        try:
            function = self._getFunction(functionPath)
        except Fault, f:
            self._cbRender(f, request)
        else:
            request.setHeader("content-type", "text/xml")
            defer.maybeDeferred(function, *args).addErrback(
                self._ebRender
                ).addCallback(
                self._cbRender, request
                )

        return server.NOT_DONE_YET


# The server
# How to use the server... (Sample code)

# $ python
# >>> from twistedserver import TwistedRPCServer
# >>> s = TwistedRPCServer('user','pass')
# >>> from twisted.web import server
# >>> from twisted.internet import reactor
# >>> reactor.listenTCP(8080, server.Site(s))
# >>> reactor.run()

# Sample client
# Without auth
# 
# $ python
# >>> from xmlrpclib import ServerProxy
# >>> p = ServerProxy('http://localhost:8080')
# >>> p
# <ServerProxy for localhost:8080/RPC2>
# >>> p.echo('hi')
# Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "/usr/lib/python2.5/xmlrpclib.py", line 1147, in __call__
#    return self.__send(self.__name, args)
#  File "/usr/lib/python2.5/xmlrpclib.py", line 1437, in __request
#    verbose=self.__verbose
#  File "/usr/lib/python2.5/xmlrpclib.py", line 1191, in request
#    headers
# xmlrpclib.ProtocolError: <ProtocolError for localhost:8080/RPC2: 401  
# Unauthorized>

# With auth
# >>> p = ServerProxy('http://user:pass@localhost:8080')
# >>> p.echo('hi')
# 'hi'
