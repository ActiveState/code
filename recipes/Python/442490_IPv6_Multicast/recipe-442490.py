#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import time
import socket
import select
import struct

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ LibC definitions of if_nametoindex
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if_nametoindex = None

if if_nametoindex is None:
    try: import ctypes
    except ImportError: pass
    else:
        _libc = ctypes.cdll.libc
        def if_nametoindex(interfaceName):
            # if you have a better way to get the interface index, I'd love to hear
            # it...  You are supposed to be able to leave the interface number as 0,
            # but I get an exception when I try this.  (MacOS 10.4)  It may be because
            # it is a multihomed device...
            return _libc.if_nametoindex(interfaceName)

if if_nametoindex is None:
    try: import dl
    except ImportError: pass
    else:
        _libc = dl.open('libc.so')
        def if_nametoindex(interfaceName):
            # if you have a better way to get the interface index, I'd love to hear
            # it...  You are supposed to be able to leave the interface number as 0,
            # but I get an exception when I try this.  (MacOS 10.4)  It may be because
            # it is a multihomed device...
            return _libc.call('if_nametoindex', interfaceName)

if if_nametoindex is None:
    raise RuntimeError("No implementation allowing access to if_nametoindex available")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

maddr = ('ff12::4242', 4242)

def ipv6Multicast(host='::1', maddr=maddr):
    haddr = socket.getaddrinfo(host, maddr[1], socket.AF_INET6, socket.SOCK_DGRAM)[0][-1]
    maddr = socket.getaddrinfo(maddr[0], maddr[1], socket.AF_INET6, socket.SOCK_DGRAM)[0][-1]

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 5)

    ifn = haddr[3] or if_nametoindex('lo0')
    ifn = struct.pack("I", ifn)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, ifn)

    group = socket.inet_pton(socket.AF_INET6, maddr[0]) + ifn
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, group)

    sock.bind(haddr)
    sock.setblocking(False)

    return sock, maddr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    # change host to use your IPv6 address...
    sock, maddr = ipv6Multicast(host='::1')

    # send initial message
    msg = ' '.join(sys.argv[1:])
    msg = msg or 'IPv6 multicast recipie'
    sock.sendto(msg, maddr)

    try:
        t0 = 0
        while 1:
            tn = time.time()
            if tn-t0 > 1:
                sock.sendto('blink: '+msg, maddr)
                t0 = tn

            if select.select([sock],[],[],1)[0]:
                # we have a message... print what was sent!
                print sock.recvfrom(1024)
    except KeyboardInterrupt:
        pass
