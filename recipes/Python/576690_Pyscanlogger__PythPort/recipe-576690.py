#!/usr/bin/env python
"""
pyscanlogger: Simple port scan detector/logger tool, inspired
by scanlogd {http://www.openwall.com/scanlogd}


"""

import sys, os
import dpkt, pcap
import struct
import socket
import time
import threading
import optparse


# UDP - in progress...

SCAN_TIMEOUT = 5
WEIGHT_THRESHOLD = 25
PIDFILE="/var/run/pyscanlogger.pid"

# TCP flag constants
TH_URG=dpkt.tcp.TH_URG
TH_ACK=dpkt.tcp.TH_ACK
TH_PSH=dpkt.tcp.TH_PUSH
TH_RST=dpkt.tcp.TH_RST
TH_SYN=dpkt.tcp.TH_SYN
TH_FIN=dpkt.tcp.TH_FIN

# Protocols
TCP=dpkt.tcp.TCP
UDP=dpkt.udp.UDP

get_timestamp = lambda : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

class ScanEntry(object):
    """ Port scan entry """
    
    def __init__(self, hash):
        self.src = 0
        self.dst = 0
        self.timestamp = 0
        self.logged = False
        self.type = ''
        self.tcpflags_or = 0
        self.weight = 0
        self.ports = []
        self.next = None
        self.hash = hash

class EntryLog(dict):
    """ Modified dictionary class with fixed size, which
    automatically removes oldest items """

    # This will work only if the value is an object storing
    # its key in the 'hash' attribute and links to other
    # objects usin the 'next' attribute.
    def __init__(self, maxsz):
        self.oldest = None
        self.last = None
        self.maxsz = maxsz
        super(EntryLog, self).__init__()

    def __setitem__(self, key, value):
        if not self.__contains__(key) and len(self)==self.maxsz:
            # Remove oldest
            if self.oldest:
                self.__delitem__(self.oldest.hash)
                self.oldest = self.oldest.next
        
        super(EntryLog, self).__setitem__(key,value)

        if self.last:
            self.last.next = value
            self.last = value
        else:
            self.last = value
            self.oldest = self.last

    
class TimerList(list):
    """ List class of fixed size with entries that time out automatically """

    def __getattribute__(self, name):
        if name in ('insert','pop','extend'):
            raise NotImplementedError
        else:
            return super(TimerList, self).__getattribute__(name)
        
    def __init__(self, maxsz, ttl):
        # Maximum size
        self.maxsz = maxsz
        # Time to live for every entry
        self.ttl = ttl

    def append(self, item):
        """ Append an item to end """

        if len(self)<self.maxsz:
            # We append the time-stamp with the item
            super(TimerList, self).append((time.time(), item))
        else:
            n=self.collect()
            if n:
                # Some items removed, so append
                super(TimerList, self).append((time.time(), item))
            else:
                raise ValueError,'could not append item'
            
    def collect(self):
        """ Collect and remove aged items """
        
        t=time.time()
        old = []
        for item in self:
            if (t-item[0])>self.ttl:
                old.append(item)

        
        for item in old:
            self.remove(item)

        return len(old)

    # Access functions
    def __getitem__(self, index):
        item = super(TimerList, self).__getitem__(index)
        return item[1]

    def __setitem__(self,  index, item):
        # Allow only tuples with time-stamps >= current time-stamp as 1st member
        if type(item) == tuple and len(item) == 2  and type(item[0]) == float and item[0]>=time.time():
            super(TimerList, self).__setitem__(index, item)
        else:
            raise TypeError, 'invalid entry'

    def __contains__(self, item):

        items = [rest for (tstamp,rest) in self]
        return item in items
    
class ScanLogger(object):
    """ Port scan detector/logger """
    
    # TCP flags to scan type mapping
    scan_types = {0: 'TCP null',
                  TH_FIN: 'TCP fin',
                  TH_SYN: 'TCP syn', TH_SYN|TH_RST: 'TCP syn',
                  TH_ACK: 'TCP ack',
                  TH_URG|TH_PSH|TH_FIN: 'TCP x-mas', TH_URG|TH_PSH|TH_FIN|TH_ACK: 'TCP x-mas',
                  TH_SYN|TH_FIN: 'TCP syn/fin',
                  TH_FIN|TH_ACK: 'TCP fin/ack',
                  TH_SYN|TH_ACK|TH_RST: 'TCP full-connect',
                  TH_URG|TH_PSH|TH_ACK|TH_RST|TH_SYN|TH_FIN: 'TCP all-flags' } 
                  
    def __init__(self, timeout, threshold, maxsize, daemon=True, logfile='/var/log/scanlog'):
        self.scans = EntryLog(maxsize)
        # Port scan weight threshold
        self.threshold = threshold
        # Timeout for scan entries
        self.timeout = timeout
        # Daemonize ?
        self.daemon = daemon
        # Log file
        try:
            self.scanlog = open(logfile,'a')
        except (IOError, OSError), (errno, strerror):
            print "Error opening scan log file %s => %s" % (logfile, strerror)
            self.scanlog = None
            
        # Recent scans - this list allows to keep scan information
        # upto last 'n' seconds, so as to not call duplicate scans
        # in the same time-period. 'n' is 60 sec by default.

        # Since entries time out in 60 seconds, max size is equal
        # to maximum such entries possible in 60 sec - assuming
        # a scan occurs at most every 5 seconds, this would be 12.
        self.recent_scans = TimerList(12, 60.0)
        
    def hash_func(self, addr):
        """ Hash a host address """
        
        value = addr
        h = 0
    
        while value:
            # print value
            h ^= value
            value = value >> 9
        
        return h & (8192-1)

    def host_hash(self, src, dst):
        """ Hash mix two host addresses """

        return self.hash_func(src)^self.hash_func(dst)

    def log_scan(self, scan, continuation=False):
        """ Log the scan to file and/or console """

        srcip, dstip = socket.inet_ntoa(struct.pack('I',scan.src)), socket.inet_ntoa(struct.pack('I',scan.dst))
        ports = ','.join([str(port) for port in scan.ports])
        
        if not continuation:
            line = '[%s]: %s scan (flags:%d) from %s to %s (ports:%s)' % (get_timestamp(),
                                                                          scan.type,
                                                                          scan.tcpflags_or,
                                                                          srcip,
                                                                          dstip,
                                                                          ports)
        else:
            line = '[%s]: Continuation of %s scan from %s to %s (ports:%s)' % (get_timestamp(),
                                                                               scan.type,
                                                                               srcip,
                                                                               dstip,
                                                                               ports)
                                                                             
        if self.scanlog:
            self.scanlog.write(line + '\n')
            self.scanlog.flush()

        if not self.daemon:
            print line
                  
    def process(self, pkt):

        if not hasattr(pkt, 'ip'):
            return

        ip = pkt.ip
        # Ignore non-tcp, non-udp packets
        if type(ip.data) not in (TCP, UDP):
            return

        pload = ip.data
        src,dst,dport,flags = int(struct.unpack('I',ip.src)[0]),int(struct.unpack('I', ip.dst)[0]),int(pload.dport),0
        proto = type(pload)
        
        if proto == TCP: flags = pload.flags
        key = self.host_hash(src,dst)

        curr=time.time()

        # Keep dropping old entries
        self.recent_scans.collect()
        
        if key in self.scans:
            scan = self.scans[key]

            if scan.src != src:
                # Skip packets in reverse direction or invalid protocol
                return
                
            # Update only if not too old, else skip and remove entry
            if curr - scan.timestamp > self.timeout:
                del self.scans[key]
                return

            if scan.logged: return
            
            # Update TCP flags if existing port
            if dport in scan.ports:
                # Same port, update flags
                scan.tcpflags_or |= flags
                return
                
            scan.timestamp = curr
            scan.tcpflags_or |= flags
            scan.ports.append(dport)

            # Add weight for port
            if dport < 1024:
                scan.weight += 3
            else:
                scan.weight += 1
            
            if scan.weight>=self.threshold:
                scan.logged = True
                if proto==TCP:
                    scan.type = self.scan_types.get(scan.tcpflags_or,'unknown')
                elif proto==UDP:
                    scan.type = 'UDP'
                    # Reset flags for UDP scan
                    scan.tcpflags_or = 0
                    
                # See if this was logged recently
                scanentry = (key, scan.type, scan.tcpflags_or)
                
                if scanentry not in self.recent_scans:
                    self.log_scan(scan)
                    self.recent_scans.append(scanentry)
                else:
                    self.log_scan(scan, True)
                        
        else:
            # Add new entry
            scan = ScanEntry(key)
            scan.src = src
            scan.dst = dst
            scan.timestamp = curr
            scan.tcpflags_or |= flags
            scan.ports.append(dport)
            self.scans[key] = scan
            
    def log(self):
        
        pc = pcap.pcap()
        decode = { pcap.DLT_LOOP:dpkt.loopback.Loopback,
                   pcap.DLT_NULL:dpkt.loopback.Loopback,
                   pcap.DLT_EN10MB:dpkt.ethernet.Ethernet } [pc.datalink()]

        try:
            print 'listening on %s: %s' % (pc.name, pc.filter)
            for ts, pkt in pc:
                self.process(decode(pkt))
        except KeyboardInterrupt:
            if not self.daemon:
                nrecv, ndrop, nifdrop = pc.stats()
                print '\n%d packets received by filter' % nrecv
                print '%d packets dropped by kernel' % ndrop

    def run_daemon(self):
        # Disconnect from tty
        try:
            pid = os.fork()
            if pid>0:
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, "fork #1 failed", e
            sys.exit(1)

        os.setsid()
        os.umask(0)

        # Second fork
        try:
            pid = os.fork()
            if pid>0:
                open(PIDFILE,'w').write(str(pid))
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, "fork #2 failed", e
            sys.exit(1)
            
        self.log()
        
    def run(self):
        # If dameon, then create a new thread and wait for it
        if self.daemon:
            print 'Daemonizing...'
            self.run_daemon()
        else:
            # Run in foreground
            self.log()

def main():
    
    if os.geteuid() != 0:
        sys.exit("You must be super-user to run this program")
        
    o=optparse.OptionParser()
    o.add_option("-d", "--daemonize", dest="daemon", help="Daemonize",
                 action="store_true", default=False)
    o.add_option("-f", "--logfile", dest="logfile", help="File to save logs to",
                 default="/var/log/scanlog")
    
    options, args = o.parse_args()
    s=ScanLogger(SCAN_TIMEOUT, WEIGHT_THRESHOLD, 8192, options.daemon, options.logfile)
    s.run()
    
if __name__ == '__main__':
    main()
