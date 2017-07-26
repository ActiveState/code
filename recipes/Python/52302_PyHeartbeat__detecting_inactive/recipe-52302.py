# Filename: HeartbeatClient.py

"""Heartbeat client, sends out an UDP packet periodically"""

import socket, time

SERVER_IP = '127.0.0.1'; SERVER_PORT = 43278; BEAT_PERIOD = 5

print ('Sending heartbeat to IP %s , port %d\n'
    'press Ctrl-C to stop\n') % (SERVER_IP, SERVER_PORT)
while True:
    hbSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hbSocket.sendto('PyHB', (SERVER_IP, SERVER_PORT))
    if __debug__: print 'Time: %s' % time.ctime()
    time.sleep(BEAT_PERIOD)

--- 8< --- snip --- 8< --- snip --- 8< --- snip --- 8< ---

# Filename: ThreadedBeatServer.py

"""Threaded heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 20; CHECK_TIMEOUT = 15

import socket, threading, time

class Heartbeats(dict):
    """Manage shared heartbeats dictionary with thread locking"""

    def __init__(self):
        super(Heartbeats, self).__init__()
        self._lock = threading.Lock()

    def __setitem__(self, key, value):
        """Create or update the dictionary entry for a client"""
        self._lock.acquire()
        super(Heartbeats, self).__setitem__(key, value)
        self._lock.release()

    def getSilent(self):
        """Return a list of clients with heartbeat older than CHECK_TIMEOUT"""
        limit = time.time() - CHECK_TIMEOUT
        self._lock.acquire()
        silent = [ip for (ip, ipTime) in self.items() if ipTime < limit]
        self._lock.release()
        return silent

class Receiver(threading.Thread):
    """Receive UDP packets and log them in the heartbeats dictionary"""

    def __init__(self, goOnEvent, heartbeats):
        super(Receiver, self).__init__()
        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats
        self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recSocket.settimeout(CHECK_TIMEOUT)
        self.recSocket.bind((socket.gethostbyname('localhost'), UDP_PORT))

    def run(self):
        while self.goOnEvent.isSet():
            try:
                data, addr = self.recSocket.recvfrom(5)
                if data == 'PyHB':
                    self.heartbeats[addr[0]] = time.time()
            except socket.timeout:
                pass

def main():
    receiverEvent = threading.Event()
    receiverEvent.set()
    heartbeats = Heartbeats()
    receiver = Receiver(goOnEvent = receiverEvent, heartbeats = heartbeats)
    receiver.start()
    print ('Threaded heartbeat server listening on port %d\n'
        'press Ctrl-C to stop\n') % UDP_PORT
    try:
        while True:
            silent = heartbeats.getSilent()
            print 'Silent clients: %s' % silent
            time.sleep(CHECK_PERIOD)
    except KeyboardInterrupt:
        print 'Exiting, please wait...'
        receiverEvent.clear()
        receiver.join()
        print 'Finished.'

if __name__ == '__main__':
    main()

--- 8< --- snip --- 8< --- snip --- 8< --- snip --- 8< ---

# Filename: TwistedBeatServer.py

"""Asynchronous events-based heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 20; CHECK_TIMEOUT = 15

import time
from twisted.application import internet, service
from twisted.internet import protocol
from twisted.python import log

class Receiver(protocol.DatagramProtocol):
    """Receive UDP packets and log them in the clients dictionary"""

    def datagramReceived(self, data, (ip, port)):
        if data == 'PyHB':
            self.callback(ip)

class DetectorService(internet.TimerService):
    """Detect clients not sending heartbeats for too long"""

    def __init__(self):
        internet.TimerService.__init__(self, CHECK_PERIOD, self.detect)
        self.beats = {}

    def update(self, ip):
        self.beats[ip] = time.time()

    def detect(self):
        """Log a list of clients with heartbeat older than CHECK_TIMEOUT"""
        limit = time.time() - CHECK_TIMEOUT
        silent = [ip for (ip, ipTime) in self.beats.items() if ipTime < limit]
        log.msg('Silent clients: %s' % silent)

application = service.Application('Heartbeat')
# define and link the silent clients' detector service
detectorSvc = DetectorService()
detectorSvc.setServiceParent(application)
# create an instance of the Receiver protocol, and give it the callback
receiver = Receiver()
receiver.callback = detectorSvc.update
# define and link the UDP server service, passing the receiver in
udpServer = internet.UDPServer(UDP_PORT, receiver)
udpServer.setServiceParent(application)
# each service is started automatically by Twisted at launch time
log.msg('Asynchronous heartbeat server listening on port %d\n'
    'press Ctrl-C to stop\n' % UDP_PORT)
