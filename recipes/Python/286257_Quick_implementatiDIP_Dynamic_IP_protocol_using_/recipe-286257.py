# 2004 (c) Nicola Paolucci <nick ath durdn doth net>
# OpenSource, Python License

"""
Command line prototype to update a Dynamic DNS Service that
accepts the GnuDIP protocol (like yi.org):

pydyp.py -u <uname> -w <password> -s <dipserver> -p <dipserverport> -d <domain>

"""

import md5
import sys

from twisted.internet import protocol,reactor
from twisted.protocols import basic
from twisted.python import usage

__version__ = '0.4'
__author__=('Nicola Paolucci <nick ath durdn doth net>',)
__thanks_to__=[]
__copyright__=''
__history__="""
  0.1 First prototype version
  0.2 Use of .hexdigest()
  0.3 Refactored to separate mechanism and policy
  0.4 No need to pass the factory to the protocol
""" # -> "


def hashPassword(password, salt):
    p1 = md5.md5(password).hexdigest() + '.' + salt.strip()
    hashedpass = md5.md5(p1).hexdigest()
    return hashedpass

class DIPProtocol(basic.LineReceiver):
    """ Quick implementation of GnuDIP protocol (TCP) as described here:
    http://gnudip2.sourceforge.net/gnudip-www/latest/gnudip/html/protocol.html
    """

    delimiter = '\n'

    def connectionMade(self):
        basic.LineReceiver.connectionMade(self)
        self.expectingSalt = True

    def lineReceived(self, line):
        if self.expectingSalt:
            self.saltReceived(line)
            self.expectingSalt = False
        else:
            self.responseReceived(line)

    def saltReceived(self, salt):
        """Override this."""

    def responseReceived(self, response):
        """Override this."""


class DIPUpdater(DIPProtocol):
    """A quick class to update an IP, then disconnect."""
    def saltReceived(self, salt):
        password = self.factory.getPassword()
        username = self.factory.getUsername()
        domain = self.factory.getDomain()

        msg = '%s:%s:%s:2' % (username, hashPassword(password, salt), domain)
        self.sendLine(msg)

    def responseReceived(self, response):
        code = response.split(':', 1)[0]
        if code == '0':
            pass  # OK
        elif code == '1':
            print 'Authentication failed'
        else:
            print 'Unexpected response from server:', repr(response)

        self.transport.loseConnection()

class DIPClientFactory(protocol.ClientFactory):
     """ Factory used to instantiate DIP protocol instances with
         correct username,password and domain.
     """ # -> "
     protocol = DIPUpdater

     def __init__(self,username,password,domain):
         self.u = username
         self.p = password
         self.d = domain

     def getUsername(self):
         return self.u

     def getPassword(self):
         return self.p

     def getDomain(self):
         return self.d

     def clientConnectionLost(self, connector, reason):
         reactor.stop()

     def clientConnectionFailed(self, connector, reason):
         print 'Connection failed. Reason:', reason


class Options(usage.Options):
     optParameters = [['server', 's','gnudip2.yi.org', 'DIP Server'],
                      ['port', 'p',3495,'DIP Server  port'],
                      ['username', 'u','durdn', 'Username'],
                      ['password', 'w',None,'Password'],
                      ['domain', 'd','durdn.yi.org', 'Domain']]

if __name__ == '__main__':
     config = Options()
     try:
         config.parseOptions()
     except usage.UsageError, errortext:
         print '%s: %s' % (sys.argv[0], errortext)
         print '%s: Try --help for usage details.' % (sys.argv[0])
         sys.exit(1)

     server = config['server']
     port = int(config['port'])
     password = config['password']
     if not password:
         print 'Password not entered. Try --help for usage details.'
         sys.exit(1)

     reactor.connectTCP(server, port,
                        DIPClientFactory(config['username'],password,
                                         config['domain']))
     reactor.run()
