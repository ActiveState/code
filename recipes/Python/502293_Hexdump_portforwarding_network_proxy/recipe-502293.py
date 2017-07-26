#!/usr/bin/env python
# hex-dump network proxy: run with "-h" to see usage information
"""usage: PROGRAM [options] <fromport:hostname:toport> <...>

A port forwarding proxy server that hex-dumps traffic in both directions.

Example:
  Listen for and forward connections on port 8080 to port 80 on
  www.google.com, hex-dumping the network traffic in both directions:
 
  $ PROGRAM 8080:www.google.com:80

Copyright (C) 2005-2007 Andrew Ellerton, mail: activestate-at->ellerton.net
"""
import sys, getopt, logging, re
try: import twisted
except ImportError:
  print "Please install the 'twisted' package from http://twistedmatrix.com/"
  sys.exit(1)

from twisted.python import failure
from twisted.internet import reactor, error, address, tcp
from twisted.internet.protocol import Protocol, Factory, ClientFactory

# --------------------------------------------------------------------------
# This GREAT hexdump function from Sebastian Keim's Python recipe at:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812
# --------------------------------------------------------------------------
HEX_FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
def hexdump(prefix, src, length=16):
  N=0; result=''
  while src:
    s,src = src[:length],src[length:]
    hexa = ' '.join(["%02X"%ord(x) for x in s])
    s = s.translate(HEX_FILTER)
    result += "%s %04X   %-*s   %s\n" % (prefix, N, length*3, hexa, s)
    N+=length
  return result
# --------------------------------------------------------------------------
def transport_info(t):
  if isinstance(t, tcp.Client): return transport_info(t.getHost())
  elif isinstance(t, address.IPv4Address): return "%s:%d" % (t.host, t.port)
  else: return repr(t)

class HexdumpClientProtocol(Protocol):
  def __init__(self, factory):
    self.factory=factory

  def connectionMade(self):
    logger.debug("bridge connection open %s" % transport_info(self.transport))
    self.factory.owner.clientName=transport_info(self.transport)
    self.writeCache()

  def write(self, buf):
    self.transport.write(buf)

  def dataReceived(self, recvd):
    self.factory.owner.write(recvd)

  def writeCache(self):
    while self.factory.writeCache:
      item = self.factory.writeCache.pop(0)
      self.write(item)

class HexdumpClientFactory(ClientFactory):
  def __init__(self, owner):
    self.owner = owner
    self.writeCache = []

  def startedConnecting(self, connector):
    logger.debug('connection opening...')

  def buildProtocol(self, addr):
    logger.debug('connecting to remote server %s' % transport_info(addr))
    p = HexdumpClientProtocol(self)
    self.owner.dest = p
    return p

  def clientConnectionLost(self, connector, reason):
    if isinstance(reason, failure.Failure):
      if reason.type == twisted.internet.error.ConnectionDone:
        logger.info("remote server closed connection")
      else:
        logger.info("remote server connection lost, reason: %r" % reason)
    self.owner.close()

  def clientConnectionFailed(self, connector, reason):
    logger.debug("dest: connection failed: %r" % reason)
    self.owner.close()

class HexdumpServerProtocol(Protocol):
  def __init__(self, serverFactory):
    self.factory=serverFactory
    self.clientFactory = HexdumpClientFactory(self)
    self.clientName=id(self) # this is repopulated later
    self.serverName=None

  def serverName(self):
    return "%s:%d" %(self.factory.remote_host,self.factory.remote_port)

  def connectionMade(self):
    self.serverName="%s:%d" %(self.factory.remote_host,self.factory.remote_port)
    logger.info("client %s opened connection -> server %s" % (
      self.clientName, self.serverName))

    # cxn to this server has opened. Open a port to the destination...
    reactor.connectTCP(self.factory.remote_host,
      self.factory.remote_port, self.clientFactory)

  def connectionLost(self, reason):
    logger.info("client %s closed connection" % self.clientName) # str(reason)
    if self.dest and self.dest.transport: self.dest.transport.loseConnection()

  def connectionFailed(self, reason):
    logger.debug("proxy connection failed: %s" % str(reason))

  def dataReceived(self, recvd):
    logger.info("client %s -> server %s (%d bytes)\n%s" % (
      self.clientName, self.serverName, len(recvd), hexdump('->', recvd)))
    if hasattr(self, "dest"):
      self.dest.write(recvd)
    else:
      logger.debug("caching data until remote connection is open")
      self.clientFactory.writeCache.append(recvd)

  def write(self, buf):
    logger.info("client %s <= server %s (%d bytes)\n%s" % (
      self.clientName, self.serverName, len(buf), hexdump('<=', buf)))
    self.transport.write(buf)

  def close(self):
    self.dest = None
    self.transport.loseConnection()

class HexdumpServerFactory(Factory):
  def __init__(self, listen_port, remote_host, remote_port, max_connections = None):
    self.listen_port = listen_port
    self.remote_host = remote_host
    self.remote_port = remote_port
    self.max_connections = max_connections
    self.numConnections = 0

  def startFactory(self):
    logger.info("listening on %d -> %s:%d" % (self.listen_port, self.remote_host, self.remote_port))

  def buildProtocol(self, addr): # could process max/num connections here
    return HexdumpServerProtocol(self)

if __name__ == "__main__":
  import os.path
  __usage__ = __doc__.replace("PROGRAM", os.path.basename(sys.argv[0]))
  port_map_pattern=re.compile("(\d+):([\w\.\-]+):(\d+)")
  logger = logging.getLogger()
  num_factories=0

  def die_usage(msg=""):
    sys.stderr.write("%s%s\n" % (__usage__, msg))
    sys.exit(1)

  def add_factory(port_map_desc):
    match = port_map_pattern.match(port_map_desc)
    if not match: die_usage("malformed port map description: %s" % port_map_desc)
    listen_port = int(match.group(1))
    remote_host = match.group(2)
    remote_port = int(match.group(3))
    factory = HexdumpServerFactory(listen_port, remote_host, remote_port)
    reactor.listenTCP(factory.listen_port, factory)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:v", ["help", "log=", "verbose"])
  except getopt.GetoptError, e:
    die_usage(str(e))

  logname=None
  logger.setLevel(logging.INFO)
  for o, a in opts:
    if o in ("-h", "--help"): die_usage()
    if o in ("-v", "--verbose"): logger.setLevel(logging.DEBUG)
    if o in ("-l", "--log"): logname=a; print "log: [%s]" % logname

  if logname: handler=logging.FileHandler(logname)
  else: handler = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  for a in args: add_factory(a); num_factories+=1
  if num_factories==0: die_usage("No proxy/port forwarding connections specified")

  logger.info("ready (Ctrl+C to stop)")
  reactor.run()
  logger.info("stopped")
