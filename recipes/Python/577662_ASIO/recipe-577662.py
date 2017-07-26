import collections
import errno
import functools
import select
import socket

'''Asynchronous socket service inspired by the basic design of Boost ASIO.

This service currently supports TCP sockets only, and supports asynchronous
versions of common client operations (connect, read, write) and server operations 
(accept).

This implementation supports the use of select, poll, epoll, or kqueue as the
underlying poll system call.

Aaron Riekenberg
aaron.riekenberg@gmail.com
'''

class AsyncException(Exception):

  def __init__(self, value):
    super(AsyncException, self).__init__()
    self.__value = value

  def __str__(self):
    return repr(self.__value)

class AsyncSocket(object):

  '''Socket class supporting asynchronous operations.'''

  def __init__(self, asyncIOService, sock = None):
    super(AsyncSocket, self).__init__()
    self.__asyncIOService = asyncIOService
    self.__acceptCallback = None
    self.__connectCallback = None
    self.__readCallback = None
    self.__writeAllCallback = None
    self.__writeBuffer = b''
    self.__maxReadBytes = 0
    self.__closed = False
    if sock:
      self.__socket = sock
    else:
      self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket.setblocking(0)
    asyncIOService.addAsyncSocket(self)

  def __str__(self):
    return ('AsyncSocket [ fileno = %d ]' % self.fileno())

  def getsockname(self):
    return self.__socket.getsockname()

  def getpeername(self):
    return self.__socket.getpeername()
 
  def closed(self):
    return self.__closed

  def getSocket(self):
    return self.__socket

  def fileno(self):
    return self.__socket.fileno()

  def setReuseAddress(self):
    self.__socket.setsockopt(
      socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  def listen(self, backlog = socket.SOMAXCONN):
    self.__socket.listen(backlog)

  def bind(self, addr):
    self.__socket.bind(addr)

  def asyncConnect(self, address, callback):
    if (self.__acceptCallback):
      raise AsyncException('Accept already in progress')
    if (self.__connectCallback):
      raise AsyncException('Connect already in progress')
    if (self.__readCallback):
      raise AsyncException('Read already in progress')
    if (self.__writeAllCallback):
      raise AsyncException('Write all already in progress')
    if (self.__closed):
      raise AsyncException('AsyncSocket closed')

    err = self.__socket.connect_ex(address)
    if err in (errno.EINPROGRESS, errno.EWOULDBLOCK):
      self.__connectCallback = callback
      self.__asyncIOService.registerAsyncSocketForWrite(self)
    else:
      self.__asyncIOService.invokeLater(
        functools.partial(callback, err = err))

  def asyncAccept(self, callback):
    if (self.__acceptCallback):
      raise AsyncException('Accept already in progress')
    if (self.__connectCallback):
      raise AsyncException('Connect already in progress')
    if (self.__readCallback):
      raise AsyncException('Read already in progress')
    if (self.__writeAllCallback):
      raise AsyncException('Write all already in progress')
    if (self.__closed):
      raise AsyncException('AsyncSocket closed')

    try:
      (newSocket, addr) = self.__socket.accept()
      asyncSocket = AsyncSocket(self.__asyncIOService, newSocket)
      self.__asyncIOService.invokeLater(
        functools.partial(callback, sock = asyncSocket, err = 0))
    except socket.error as e:
      if e.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
        self.__acceptCallback = callback
        self.__asyncIOService.registerAsyncSocketForRead(self)
      else:
        self.__asyncIOService.invokeLater(
          functools.partial(callback, sock = None, err = e.args[0]))

  def asyncRead(self, maxBytes, callback):
    if (self.__acceptCallback):
      raise AsyncException('Accept already in progress')
    if (self.__connectCallback):
      raise AsyncException('Connect already in progress')
    if (self.__readCallback):
      raise AsyncException('Read already in progress')
    if (self.__closed):
      raise AsyncException('AsyncSocket closed')

    self.__maxReadBytes = maxBytes
    try:
      data = self.__socket.recv(self.__maxReadBytes)
      self.__asyncIOService.invokeLater(
        functools.partial(callback, data = data, err = 0))
    except socket.error as e:
      if e.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
        self.__readCallback = callback
        self.__asyncIOService.registerAsyncSocketForRead(self)
      else:
        self.__asyncIOService.invokeLater(
          functools.partial(callback, data = data, err = e.args[0]))

  def asyncWriteAll(self, data, callback):
    if (self.__acceptCallback):
      raise AsyncException('Accept already in progress')
    if (self.__connectCallback):
      raise AsyncException('Connect already in progress')
    if (self.__writeAllCallback):
      raise AsyncException('Write all already in progress')
    if (self.__closed):
      raise AsyncException('AsyncSocket closed')

    self.__writeBuffer += data
    writeWouldBlock = False
    try:
      bytesSent = self.__socket.send(self.__writeBuffer)
      self.__writeBuffer = self.__writeBuffer[bytesSent:]
      if (len(self.__writeBuffer) == 0):
        self.__asyncIOService.invokeLater(
          functools.partial(callback, err = 0))
      else:
        writeWouldBlock = True
    except socket.error as e:
      if e.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
        writeWouldBlock = True
      else:
        self.__asyncIOService.invokeLater(
          functools.partial(callback, err = e.args[0]))

    if (writeWouldBlock):
      self.__writeAllCallback = callback
      self.__asyncIOService.registerAsyncSocketForWrite(self)

  def close(self):
    if self.__closed:
      return

    self.__asyncIOService.removeAsyncSocket(self)
    self.__socket.close()
    self.__closed = True

    if self.__acceptCallback:
      self.__asyncIOService.invokeLater(
        functools.partial(self.__acceptCallback, sock = None, err = errno.EBADF))
      self.__acceptCallback = None

    if self.__connectCallback:
      self.__asyncIOService.invokeLater(
        functools.partial(self.__connectCallback, err = errno.EBADF))
      self.__connectCallback = None

    if self.__readCallback:
      self.__asyncIOService.invokeLater(
        functools.partial(self.__readCallback, data = None, err = errno.EBADF))
      self.__readCallback = None

    if self.__writeAllCallback:
      self.__asyncIOService.invokeLater(
        functools.partial(self.__writeAllCallback, err = errno.EBADF))
      self.__writeAllCallback = None

  def handleError(self):
    err = self.__socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

    if (self.__connectCallback):
      self.__asyncIOService.unregisterAsyncSocketForWrite(self)
      self.__asyncIOService.invokeLater(
        functools.partial(self.__connectCallback, err = err))
      self.__connectCallback = None

    if (self.__acceptCallback):
      self.__asyncIOService.unregisterAsyncSocketForRead(self)
      self.__asyncIOService.invokeLater(
        functools.partial(self.__acceptCallback, sock = None, err = err))
      self.__acceptCallback = None

    if (self.__readCallback):
      self.__asyncIOService.unregisterAsyncSocketForRead(self)
      self.__asyncIOService.invokeLater(
        functools.partial(self.__readCallback, data = None, err = err))
      self.__readCallback = None

    if (self.__writeAllCallback):
      self.__asyncIOService.unregisterAsyncSocketForWrite(self)
      self.__asyncIOService.invokeLater(
        functools.partial(self.__writeAllCallback, err = err))
      self.__writeAllCallback = None

  def handleRead(self):
    if (self.__acceptCallback):
      try:
        (newSocket, addr) = self.__socket.accept()
        asyncSocket = AsyncSocket(self.__asyncIOService, newSocket)
        self.__asyncIOService.unregisterAsyncSocketForRead(self)
        self.__asyncIOService.invokeLater(
          functools.partial(self.__acceptCallback, sock = asyncSocket, err = 0))
        self.__acceptCallback = None
      except socket.error as e:
        if e.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
          pass
        else:
          self.__asyncIOService.unregisterAsyncSocketForRead(self)
          self.__asyncIOService.invokeLater(
            functools.partial(self.__acceptCallback, sock = None, err = e.args[0]))
          self.__acceptCallback = None

    if (self.__readCallback):
      try:
        data = self.__socket.recv(self.__maxReadBytes)
        self.__asyncIOService.unregisterAsyncSocketForRead(self)
        self.__asyncIOService.invokeLater(
          functools.partial(self.__readCallback, data = data, err = 0))
        self.__readCallback = None
      except socket.error as e:
        if e.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
          pass
        else:
          self.__asyncIOService.unregisterAsyncSocketForRead(self)
          self.__asyncIOService.invokeLater(
            functools.partial(self.__readCallback, data = None, err = e.args[0]))
          self.__readCallback = None

  def handleWrite(self):
    if (self.__connectCallback):
      err = self.__socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
      if err not in (errno.EINPROGRESS, errno.EWOULDBLOCK):
        self.__asyncIOService.unregisterAsyncSocketForWrite(self)
        self.__asyncIOService.invokeLater(
          functools.partial(self.__connectCallback, err = err))
        self.__connectCallback = None

    if (self.__writeAllCallback):
      try:
        bytesSent = self.__socket.send(self.__writeBuffer)
        self.__writeBuffer = self.__writeBuffer[bytesSent:]
        if (len(self.__writeBuffer) == 0):
          self.__asyncIOService.unregisterAsyncSocketForWrite(self)
          self.__asyncIOService.invokeLater(
            functools.partial(self.__writeAllCallback, err = 0))
          self.__writeAllCallback = None
      except socket.error as e:
        if e.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
          pass
        else:
          self.__asyncIOService.unregisterAsyncSocketForWrite(self)
          self.__asyncIOService.invokeLater(
            functools.partial(self.__writeAllCallback, err = e.args[0]))
          self.__writeAllCallback = None

class AsyncIOService(object):

  '''Service used to poll asynchronous sockets.'''

  def __init__(self):
    self.__fdToAsyncSocket = {}
    self.__fdsRegisteredForRead = set()
    self.__fdsRegisteredForWrite = set()
    self.__eventQueue = collections.deque()

  def createAsyncSocket(self):
    return AsyncSocket(asyncIOService = self)

  def addAsyncSocket(self, asyncSocket):
    self.__fdToAsyncSocket[asyncSocket.fileno()] = asyncSocket

  def removeAsyncSocket(self, asyncSocket):
    fileno = asyncSocket.fileno()
    if fileno in self.__fdToAsyncSocket:
      del self.__fdToAsyncSocket[fileno]
    if ((fileno in self.__fdsRegisteredForRead) or
        (fileno in self.__fdsRegisteredForWrite)):
      self.unregisterForEvents(asyncSocket)
      self.__fdsRegisteredForRead.discard(fileno)
      self.__fdsRegisteredForWrite.discard(fileno)

  def invokeLater(self, event):
    self.__eventQueue.append(event)

  def registerAsyncSocketForRead(self, asyncSocket):
    fileno = asyncSocket.fileno()
    if fileno not in self.__fdsRegisteredForRead:
      if fileno in self.__fdsRegisteredForWrite:
        self.modifyRegistrationForEvents(asyncSocket, readEvents = True, writeEvents = True)
      else:
        self.registerForEvents(asyncSocket, readEvents = True, writeEvents = False)
      self.__fdsRegisteredForRead.add(fileno)

  def unregisterAsyncSocketForRead(self, asyncSocket):
    fileno = asyncSocket.fileno()
    if fileno in self.__fdsRegisteredForRead:
      if fileno in self.__fdsRegisteredForWrite:
        self.modifyRegistrationForEvents(asyncSocket, readEvents = False, writeEvents = True)
      else:
        self.unregisterForEvents(asyncSocket)
      self.__fdsRegisteredForRead.discard(fileno)

  def registerAsyncSocketForWrite(self, asyncSocket):
    fileno = asyncSocket.fileno()
    if fileno not in self.__fdsRegisteredForWrite:
      if fileno in self.__fdsRegisteredForRead:
        self.modifyRegistrationForEvents(asyncSocket, readEvents = True, writeEvents = True)
      else:
        self.registerForEvents(asyncSocket, readEvents = False, writeEvents = True)
      self.__fdsRegisteredForWrite.add(fileno)

  def unregisterAsyncSocketForWrite(self, asyncSocket):
    fileno = asyncSocket.fileno()
    if fileno in self.__fdsRegisteredForWrite:
      if fileno in self.__fdsRegisteredForRead:
        self.modifyRegistrationForEvents(asyncSocket, readEvents = True, writeEvents = False)
      else:
        self.unregisterForEvents(asyncSocket)
      self.__fdsRegisteredForWrite.discard(fileno)

  def getReadFDSet(self):
    return self.__fdsRegisteredForRead

  def getWriteFDSet(self):
    return self.__fdsRegisteredForWrite

  def getNumFDs(self):
    return len(self.__fdToAsyncSocket)

  def registerForEvents(self, asyncSocket, readEvents, writeEvents):
    raise NotImplementedError

  def modifyRegistrationForEvents(self, asyncSocket, readEvents, writeEvents):
    raise NotImplementedError

  def unregisterForEvents(self, asyncSocket):
    raise NotImplementedError

  def doPoll(self, block):
    raise NotImplementedError

  def run(self):
    while True:
      # As we process events in self.__eventQueue, more events are likely
      # to be added to it by invokeLater.  We don't want to starve events
      # coming in from doPoll, so we limit the number of events processed
      # from self.__eventQueue to the initial size of the queue.  After this if
      # the queue is still not empty, set doPoll to be non blocking so we get
      # back to processing events in the queue in a timely manner.
      initialQueueLength = len(self.__eventQueue)
      eventsProcessed = 0
      while ((len(self.__eventQueue) > 0) and
             (eventsProcessed < initialQueueLength)):
        event = self.__eventQueue.popleft()
        event()
        eventsProcessed += 1

      if ((len(self.__eventQueue) == 0) and
          (len(self.__fdsRegisteredForRead) == 0) and
          (len(self.__fdsRegisteredForWrite) == 0)):
        break

      block = True
      if (len(self.__eventQueue) > 0):
        block = False
      self.doPoll(block = block)

  def handleEventForFD(self, fd, readReady, writeReady, errorReady):
    if fd in self.__fdToAsyncSocket:
      asyncSocket = self.__fdToAsyncSocket[fd]
      if (readReady):
        asyncSocket.handleRead()
      if (writeReady):
        asyncSocket.handleWrite()
      if (errorReady):
        asyncSocket.handleError()

class EPollAsyncIOService(AsyncIOService):

  def __init__(self):
    super(EPollAsyncIOService, self).__init__()
    self.__poller = select.epoll()

  def __str__(self):
    return ('EPollAsyncIOService [ fileno = %d ]' % self.__poller.fileno())

  def registerForEvents(self, asyncSocket, readEvents, writeEvents):
    fileno = asyncSocket.fileno()
    eventMask = 0
    if (readEvents):
      eventMask |= select.EPOLLIN
    if (writeEvents):
      eventMask |= select.EPOLLOUT
    self.__poller.register(fileno, eventMask)

  def modifyRegistrationForEvents(self, asyncSocket, readEvents, writeEvents):
    fileno = asyncSocket.fileno()
    eventMask = 0
    if (readEvents):
      eventMask |= select.EPOLLIN
    if (writeEvents):
      eventMask |= select.EPOLLOUT
    self.__poller.modify(fileno, eventMask)

  def unregisterForEvents(self, asyncSocket):
    fileno = asyncSocket.fileno()
    self.__poller.unregister(fileno)

  def doPoll(self, block):
    readyList = self.__poller.poll(-1 if block else 0)
    for (fd, eventMask) in readyList:
      readReady = ((eventMask & select.EPOLLIN) != 0)
      writeReady = ((eventMask & select.EPOLLOUT) != 0)
      errorReady = ((eventMask & 
                     (select.EPOLLERR | select.EPOLLHUP)) != 0)
      self.handleEventForFD(fd = fd,
                            readReady = readReady,
                            writeReady = writeReady,
                            errorReady = errorReady)

class KQueueAsyncIOService(AsyncIOService):

  def __init__(self):
    super(KQueueAsyncIOService, self).__init__()
    self.__kqueue = select.kqueue()

  def __str__(self):
    return ('KQueueAsyncIOService [ fileno = %d ]' % self.__kqueue.fileno())

  def registerForEvents(self, asyncSocket, readEvents, writeEvents):
    fileno = asyncSocket.fileno()
    if readEvents:
      readKE = select.kevent(ident = fileno,
                             filter = select.KQ_FILTER_READ,
                             flags = select.KQ_EV_ADD)
    else:
      readKE = select.kevent(ident = fileno,
                             filter = select.KQ_FILTER_READ,
                             flags = (select.KQ_EV_ADD | select.KQ_EV_DISABLE))
    if writeEvents:
      writeKE = select.kevent(ident = fileno,
                              filter = select.KQ_FILTER_WRITE,
                              flags = select.KQ_EV_ADD)
    else:
      writeKE = select.kevent(ident = fileno,
                              filter = select.KQ_FILTER_WRITE,
                              flags = (select.KQ_EV_ADD | select.KQ_EV_DISABLE))
    # Should be able to put readKE and writeKE in a list in
    # one call to kqueue.control, but this is broken due to Python issue 5910
    self.__kqueue.control([readKE], 0, 0)
    self.__kqueue.control([writeKE], 0, 0)

  def modifyRegistrationForEvents(self, asyncSocket, readEvents, writeEvents):
    fileno = asyncSocket.fileno()
    if readEvents:
      readKE = select.kevent(ident = fileno,
                             filter = select.KQ_FILTER_READ,
                             flags = select.KQ_EV_ENABLE)
    else:
      readKE = select.kevent(ident = fileno,
                             filter = select.KQ_FILTER_READ,
                             flags = select.KQ_EV_DISABLE)
    if writeEvents:
      writeKE = select.kevent(ident = fileno,
                              filter = select.KQ_FILTER_WRITE,
                              flags = select.KQ_EV_ENABLE)
    else:
      writeKE = select.kevent(ident = fileno,
                              filter = select.KQ_FILTER_WRITE,
                              flags = select.KQ_EV_DISABLE)
    # Should be able to put readKE and writeKE in a list in
    # one call to kqueue.control, but this is broken due to Python issue 5910
    self.__kqueue.control([readKE], 0, 0)
    self.__kqueue.control([writeKE], 0, 0)

  def unregisterForEvents(self, asyncSocket):
    fileno = asyncSocket.fileno()
    readKE = select.kevent(ident = fileno,
                           filter = select.KQ_FILTER_READ,
                           flags = select.KQ_EV_DELETE)
    writeKE = select.kevent(ident = fileno,
                            filter = select.KQ_FILTER_WRITE,
                            flags = select.KQ_EV_DELETE)
    # Should be able to put readKE and writeKE in a list in
    # one call to kqueue.control, but this is broken due to Python issue 5910
    self.__kqueue.control([readKE], 0, 0)
    self.__kqueue.control([writeKE], 0, 0)

  def doPoll(self, block):
    eventList = self.__kqueue.control(
                  None,
                  self.getNumFDs() * 2,
                  None if block else 0)
    for ke in eventList:
      fd = ke.ident
      readReady = (ke.filter == select.KQ_FILTER_READ)
      writeReady = (ke.filter == select.KQ_FILTER_WRITE)
      errorReady = ((ke.flags & select.KQ_EV_EOF) != 0)
      self.handleEventForFD(fd = fd,
                            readReady = readReady,
                            writeReady = writeReady,
                            errorReady = errorReady)

class PollAsyncIOService(AsyncIOService):

  def __init__(self):
    super(PollAsyncIOService, self).__init__()
    self.__poller = select.poll()

  def __str__(self):
    return 'PollAsyncIOService'

  def registerForEvents(self, asyncSocket, readEvents, writeEvents):
    fileno = asyncSocket.fileno()
    eventMask = 0
    if (readEvents):
      eventMask |= select.POLLIN
    if (writeEvents):
      eventMask |= select.POLLOUT
    self.__poller.register(fileno, eventMask)

  def modifyRegistrationForEvents(self, asyncSocket, readEvents, writeEvents):
    fileno = asyncSocket.fileno()
    eventMask = 0
    if (readEvents):
      eventMask |= select.POLLIN
    if (writeEvents):
      eventMask |= select.POLLOUT
    self.__poller.modify(fileno, eventMask)

  def unregisterForEvents(self, asyncSocket):
    fileno = asyncSocket.fileno()
    self.__poller.unregister(fileno)

  def doPoll(self, block):
    readyList = self.__poller.poll(None if block else 0)
    for (fd, eventMask) in readyList:
      readReady = ((eventMask & select.POLLIN) != 0)
      writeReady = ((eventMask & select.POLLOUT) != 0)
      errorReady = ((eventMask & 
                     (select.POLLERR | select.POLLHUP | select.POLLNVAL)) != 0)
      self.handleEventForFD(fd = fd,
                            readReady = readReady,
                            writeReady = writeReady,
                            errorReady = errorReady)

class SelectAsyncIOService(AsyncIOService):

  def __init__(self):
    super(SelectAsyncIOService, self).__init__()

  def __str__(self):
    return 'SelectAsyncIOService'

  def registerForEvents(self, asyncSocket, readEvents, writeEvents):
    pass

  def modifyRegistrationForEvents(self, asyncSocket, readEvents, writeEvents):
    pass

  def unregisterForEvents(self, asyncSocket):
    pass

  def doPoll(self, block):
    allFDSet = self.getReadFDSet() | self.getWriteFDSet()
    (readList, writeList, exceptList) = \
      select.select(self.getReadFDSet(), self.getWriteFDSet(), allFDSet,
                    None if block else 0)
    for fd in allFDSet:
      readReady = fd in readList
      writeReady = fd in writeList
      errorReady = fd in exceptList
      if (readReady or writeReady or errorReady):
        self.handleEventForFD(fd = fd,
                              readReady = readReady,
                              writeReady = writeReady,
                              errorReady = errorReady)

def createAsyncIOService(allow_epoll = True,
                         allow_kqueue = True,
                         allow_poll = True):
  '''Create an AsyncIOService supported by the platform and parameters.'''

  if (allow_epoll and hasattr(select, 'epoll')):
    return EPollAsyncIOService()
  elif (allow_kqueue and hasattr(select, 'kqueue')):
    return KQueueAsyncIOService()
  elif (allow_poll and hasattr(select, 'poll')):
    return PollAsyncIOService()
  else:
    return SelectAsyncIOService()
