import base64
import xmlrpclib

from twisted.web import xmlrpc
from twisted.internet import reactor, defer

from where.you.installed.uri import Uri

class AuthQueryProtocol(xmlrpc.QueryProtocol):
    '''
    We're just over-riding the connectionMade() method so that we
    can add the Authorization header.
    '''
    def connectionMade(self):
        self.sendCommand('POST', self.factory.url)
        self.sendHeader('User-Agent', 'Twisted/XMLRPClib')
        self.sendHeader('Host', self.factory.host)
        self.sendHeader('Content-type', 'text/xml')
        self.sendHeader('Content-length', 
            str(len(self.factory.payload)))
        if self.factory.user:
            auth = base64.encodestring('%s:%s' % (
                self.factory.user, self.factory.password))
            self.sendHeader('Authorization', 'Basic %s' % auth)
        self.endHeaders()
        self.transport.write(self.factory.payload)

class AuthQueryFactory(xmlrpc.QueryFactory):
    '''
    We're using a Uri object here for the url, diverging pretty
    strongly from how it's done in t.w.xmlrpc. This is done for 
    convenience and simplicity of presentation in this recipe.
    '''
    deferred = None
    protocol = AuthQueryProtocol

    def __init__(self, url, method, *args):
        self.url, self.host = url.path, url.host
        self.user, self.password = url.user, url.password
        self.payload = xmlrpc.payloadTemplate % (
            method, xmlrpclib.dumps(args))
        self.deferred = defer.Deferred()

class AuthProxy:
    '''
    A Proxy for making remote XML-RPC calls that supports Basic
    Authentication. There's no sense subclassing this, since it needs
    to override all of xmlrpc.Proxy.

    Pass the URL of the remote XML-RPC server to the constructor.

    Use proxy.callRemote('foobar', *args) to call remote method
    'foobar' with *args.
    '''
    def __init__(self, url):
        self.url = Uri(url)
        self.host = self.url.host
        self.port = self.url.port
        self.secure = self.url.scheme == 'https'

    def callRemote(self, method, *args):
        factory = AuthQueryFactory(self.url, method, *args)
        if self.secure:
            from twisted.internet import ssl
            reactor.connectSSL(self.host, self.port or 443,
                               factory, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(self.host, self.port or 80, factory)
        return factory.deferred

def _test():
    '''
    In this test, we'll hit a custom Zope/Plone script on a local Zope server.

    The output will give us this:
    [('authenticated', True), ('name', 'admin'), ('roles', ['Manager', 'Authenticated']), ('id', 'admin')]
    '''
    def callback(data):
        print data.items()
        reactor.stop()
    def errback(failure):
        #print failure.getErrorMessage()
        reactor.stop()
    server = AuthProxy('http://admin:admin@192.168.4.10:9673/site01/')
    d = server.callRemote('getXMLRPCUserInfo')
    d.addCallback(callback)
    d.addErrback(callback)
    reactor.run()

if __name__ == '__main__':
    _test()
