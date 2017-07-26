# Simple module for handling IPv4 addresses.

# Many thanks to Steve Holden (http://www.holdenweb.com/) for method
# min_container() and other helpful advice.

import struct
from socket import inet_aton, inet_ntoa, error as socket_error

MAX_IPV4_ADDR = 0xFFFFFFFFL

def len_to_bitmask(mask):
    """Return mask length as bitmask"""
    assert 0 <= mask <= 32
    
    return ((2L << mask - 1) - 1) << (32 - mask)
       	
def bit_to_lenmask(bitmask):
    """Convert bitmask to mask length."""

    mask = 32
    while bitmask % 2 == 0:
        bitmask = bitmask >> 1
        mask -= 1
    return mask

def quad_to_dec(addr):
    """Return dotted ip address string as long integer

    Raise IPv4AddrTypeError if address is illegal.
    """

    try:
        return struct.unpack('>L', inet_aton(addr))[0]
    except socket_error:
        raise IPv4AddrTypeError(addr)

def dec_to_quad(num):
    """Return integer ip address in dotted format

    Raise OverflowError if num is too large.
    
    >>> dec_to_quad(2**24+2**16+2**8)
    '1.1.1.0'
    >>> dec_to_quad(3243242652)
    '193.79.244.156'
    """

    return inet_ntoa(struct.pack('>L', num))

class IPv4AddrTypeError(TypeError):
    def __init__(self, addr):
        self.addr = addr
    def __str__(self):
        return "Illegal IPv4 address '%s'" % self.addr
        
class IPv4Addr:
    """Class for representing IPv4 addresses"""

    def __init__(self, addr):
        """Instantiate object.

        @param addr: dotted-quad ip address string
        """
        
        self.mask = 32                  # to help uniform handling of subnets
        self._binmask = MAX_IPV4_ADDR

        self.numeric = quad_to_dec(addr)
        self.string = addr
                     
    def mask_with(self, mask):
        """Return dotted-quad address masked with mask"""
        return dec_to_quad(self.numeric & len_to_bitmask(mask))
