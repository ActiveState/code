#! /usr/bin/env python
import fcntl, struct, sys
from socket import *

# set some symbolic constants
SIOCGIFFLAGS = 0x8913
null256 = '\0'*256

# get the interface name from the command line 
ifname = sys.argv[1]

# create a socket so we have a handle to query
s = socket(AF_INET, SOCK_DGRAM)

# call ioctl() to get the flags for the given interface
result = fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, ifname + null256)

# extract the interface's flags from the return value
flags, = struct.unpack('H', result[16:18])

# check "UP" bit and print a message
up = flags & 1
print ('DOWN', 'UP')[up]

# return a value suitable for shell's "if"
sys.exit(not up)
