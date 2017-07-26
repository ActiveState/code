#!/usr/bin/env python

import asio
import logging
import os
import sys

MAX_READ_BYTES = 2 ** 16

def createLogger():
  logger = logging.getLogger('proxy')
  logger.setLevel(logging.INFO)

  consoleHandler = logging.StreamHandler()
  consoleHandler.setLevel(logging.DEBUG)

  formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  consoleHandler.setFormatter(formatter)

  logger.addHandler(consoleHandler)

  return logger

logger = createLogger()

class Connection(object):

  def __init__(self, ioService, clientToProxySocket,
               remoteAddress, remotePort):
    self.__dataFromClient = ''
    self.__dataFromRemote = ''
    self.__writingToClient = False
    self.__writingToRemote = False
    self.__clientToProxySocket = clientToProxySocket
    self.__clientToProxyString = ('%s -> %s' %
      (clientToProxySocket.getpeername(),
       clientToProxySocket.getsockname()))
    self.__proxyToRemoteSocket = ioService.createAsyncSocket()
    self.__proxyToRemoteString = ''
    self.__proxyToRemoteSocket.asyncConnect(
      (remoteAddress, remotePort), 
      self.__connectCallback)

  def close(self):
    if not self.__writingToClient:
      if ((not self.__clientToProxySocket.closed()) and
          (len(self.__clientToProxyString) > 0)):
        logger.info('disconnect %s' % self.__clientToProxyString)
      self.__clientToProxySocket.close()
    if not self.__writingToRemote:
      if ((not self.__proxyToRemoteSocket.closed()) and
          (len(self.__proxyToRemoteString) > 0)):
        logger.info('disconnect %s' % self.__proxyToRemoteString)
      self.__proxyToRemoteSocket.close()

  def __connectCallback(self, err):
    if (err != 0):
      logger.info('connect error \'%s\'' % (os.strerror(err)))
      self.close()
    else:
      self.__proxyToRemoteString = ('%s -> %s' %
        (self.__proxyToRemoteSocket.getpeername(),
         self.__proxyToRemoteSocket.getsockname()))
      logger.info('connect %s' % self.__proxyToRemoteString)
      self.__clientToProxySocket.asyncRead(
        MAX_READ_BYTES,
        self.__readFromClientCallback)
      self.__proxyToRemoteSocket.asyncRead(
        MAX_READ_BYTES,
        self.__readFromRemoteCallback)

  def __readFromClientCallback(self, data, err):
    if self.__proxyToRemoteSocket.closed():
      self.close()
    elif (err != 0):
      self.close()
    elif not data:
      self.close()
    else:
      self.__writingToRemote = True
      self.__proxyToRemoteSocket.asyncWriteAll(data, self.__writeToRemoteCallback)

  def __readFromRemoteCallback(self, data, err):
    if self.__clientToProxySocket.closed():
      self.close()
    elif (err != 0):
      self.close()
    elif not data:
      self.close()
    else:
      self.__writingToClient = True
      self.__clientToProxySocket.asyncWriteAll(data, self.__writeToClientCallback)

  def __writeToRemoteCallback(self, err):
    self.__writingToRemote = False
    if self.__clientToProxySocket.closed():
      self.close()
    elif (err != 0):
      self.close()
    else:
      self.__clientToProxySocket.asyncRead(MAX_READ_BYTES, self.__readFromClientCallback)

  def __writeToClientCallback(self, err):
    self.__writingToClient = False
    if self.__proxyToRemoteSocket.closed():
      self.close()
    elif (err != 0):
      self.close()
    else:
      self.__proxyToRemoteSocket.asyncRead(MAX_READ_BYTES, self.__readFromRemoteCallback)

class Acceptor(object):

  def __init__(self, ioService,
               localAddress, localPort,
               remoteAddress, remotePort):
    self.__ioService = ioService
    self.__remoteAddress = remoteAddress
    self.__remotePort = remotePort
    self.__asyncSocket = ioService.createAsyncSocket();
    self.__asyncSocket.setReuseAddress()
    self.__asyncSocket.bind((localAddress, localPort))
    self.__asyncSocket.listen()
    self.__asyncSocket.asyncAccept(self.__acceptCallback)
    logger.info('listening on %s' % str(self.__asyncSocket.getsockname()))

  def __acceptCallback(self, sock, err):
    if ((err == 0) and (sock != None)):
      logger.info('accept %s -> %s' % (sock.getpeername(), sock.getsockname()))
      Connection(self.__ioService, sock, self.__remoteAddress, self.__remotePort)
    self.__asyncSocket.asyncAccept(self.__acceptCallback)

def parseAddrPortString(addrPortString):
  addrPortList = addrPortString.split(':', 1)
  return (addrPortList[0], int(addrPortList[1]))

def printUsage():
  logger.error(
    'Usage: %s <listen addr> [<listen addr> ...] <remote addr>' %
    sys.argv[0])

def main():
  if (len(sys.argv) < 3):
    printUsage()
    sys.exit(1)

  localAddressPortList = map(parseAddrPortString, sys.argv[1:-1])
  (remoteAddress, remotePort) = parseAddrPortString(sys.argv[-1])

  ioService = asio.createAsyncIOService()
  logger.info('ioService = ' + str(ioService))
  for (localAddress, localPort) in localAddressPortList:
    Acceptor(ioService,
             localAddress = localAddress,
             localPort = localPort,
             remoteAddress = remoteAddress,
             remotePort = remotePort)
  logger.info('remote address %s' % str((remoteAddress, remotePort)))
  ioService.run()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
