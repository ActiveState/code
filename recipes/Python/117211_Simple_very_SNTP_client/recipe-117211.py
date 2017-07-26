from socket import *
import struct
import sys
import time

TIME1970 = 2208988800L      # Thanks to F.Lundh

client = socket( AF_INET, SOCK_DGRAM )
data = '\x1b' + 47 * '\0'
client.sendto( data, ( sys.argv[1], 123 ))
data, address = client.recvfrom( 1024 )
if data:
    print 'Response received from:', address
    t = struct.unpack( '!12I', data )[10]
    t -= TIME1970
    print '\tTime=%s' % time.ctime(t)
