import xmlrpclib

from zope.interface import implements

from twisted.internet import defer
from twisted.cred import checkers
from twisted.cred import credentials

class ZopeChecker(object):
    '''
    A Zope cred checker for twisted applications.
    '''
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, host, port=8080, scheme="https", path="/"):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path

    def requestAvatarId(self, c):
        '''
        Please, please for the love of all that is holy to you, 
        make sure that your scheme is 'https'
        '''
        url = '%s://%s:%s@%s:%s%s' % (self.scheme, c.username, c.password, 
            self.host, self.port, self.path)
        server = xmlrpclib.ServerProxy(url)
        info = server.getXMLRPCUserInfo()
        if info.get('authenticated'):
            return defer.succeed(c.username)
        else:
            return defer.fail(error.UnauthorizedLogin())
