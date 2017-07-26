# coding: utf-8

'''This module provides 2 classes and 4 functions to,
   obtain, check and convert IP and MAC addresses.

   Class IP and MAC represent an IP respectively a
   MAC address.  Instances of IP and MAC classes
   are immutable.

   The IP class provides properties to check whether
   the address is link-local, loopback, multicast,
   a network address or network mask, private (non-
   routable), TEST-NET, THIS-HOST or THIS-NET.

   Functions getIPs and getMACs collect the available
   IP respectively MAC addresses from the underlying
   system.  Both functions provide an optional argument
   to exclude specific IP or MAC instances.

   Functions isIP and isMAC can be used to check an
   address.  The return value is an IP respectively
   MAC instance if the given address is valid.  None
   is returned otherwise.

   The IPv6 format is not supported, only IPv4.  For
   both, see module ipaddress (Python 3 only) at
   <https://docs.python.org/3/library/ipaddress.html>

   Run  python ipmac.py  to see examples and the test
   results.  Use  python ipmac.py -debug  to include
   debug output.

   The core code is copied from standard Python 2.6
   and 3.1 module Lib/uuid.py and then modified to:

     - use immutable classes IP and MAC like UUID,
     - handle any number of IP and MAC addresses,
     - collect IP and MAC addresses from several
       additional sources,
     - locate external programs only once,
     - use env and grep with ifconfig on *nixes,
     - support Python versions 2.4 thru 3.5, both
       32- and 64-bit.

   Tested on CentOS 4 (Intel), MacOS X 10.4.11 Tiger
   (Intel), MacOS X 10.3.9 Panther (PowerPC), RedHat 3
   (Opteron), Solaris 10 (Opteron), Windows XP SP2 and
   SP3 and Windows Server 2003 R2 with 32-bit Python
   2.4, 2.5, 2.6, 3.0 and/or 3.1, on CentOS 4 and 5
   (Intel) with 64-bit Python 2.4 and 2.6, on MacOS X
   10.11.5 with 64-bit Python 2.7.10 and 3.5.1 and on
   iOS 9.3.2 with 64-bit Pythonista 2.1 (on iPad).

   This module does not support Python 2.3 and older
   and has not been tested on platforms other than
   the ones listed above.
'''

import os
import socket
import struct
import sys
try:
    import ctypes
except ImportError:
    ctypes = None

__version__ =  '16.07.07'  # '10.4.22'
__all__     = ('getIPs',  'IP',  'isIP',
               'getMACs', 'MAC', 'isMAC')

if sys.hexversion < 0x3000000:
    _byte =  ord  # 2.x chr to integer
    _Ints = (int, long)
    _Strs =  basestring
else:
    _byte = int  # 3.x byte to integer
    _Ints = int
    _Strs = str  # (str, unicode)?

_b08    = 1 << 8
_b32    = 1 << 32
_b48    = 1 << 48
_debugf = None  # or printf
_exes   = {}  # executables cache
_IPsep  = '.'
_MACsep = ':'


def _bytes2int(bytes, byte=_byte):
    # convert bytes to int.
    i = 0
    for b in bytes:
        i = (i << 8) + byte(b)
    return i


def _hostname_ips():
    # get IP addresses from hostname.
    h = socket.gethostname()
    try:
        for a in socket.gethostbyname_ex(h)[2]:
            yield isIP(a)
    except AttributeError:  # no gethostbyname_ex()
        yield isIP(socket.gethostbyname(h))


def _which(exe, dirs):
    # return full path of an executable.
    p = _exes.get(exe, None)
    if p is None:
        for d in dirs:
            p = os.path.join(d, exe)
            if os.access(p, os.X_OK):
                break
        else:
            p = ''  # no such exe
        _exes[exe] = p
        if _debugf:
            _debugf('_which(%r): %r', exe, p)
    return p


if sys.platform.startswith('win'):

    # On Windows prior to 2000, UuidCreate gives a UUID containing
    # the MAC address.  On Windows 2000 and later, UuidCreate makes
    # a random UUID and UuidCreateSequential gives a UUID containing
    # the MAC address.  These routines are provided by the RPC runtime.

    # NOTE: at least on Tim's WinXP Pro SP2 desktop box, while the last
    # 6 bytes returned by UuidCreateSequential are fixed, they don't
    # appear to bear any relationship to the MAC address of any network
    # device on the box.

    def _windll_macs():
        # get the MAC address from UuidCreate*.
        try:
            b = ctypes.windll.rpcrt4
            f = getattr(b, 'UuidCreateSequential',
                getattr(b, 'UuidCreate', None))
            if f:
                b = ctypes.create_string_buffer(16)
                if f(b) == 0:
                    yield MAC(_bytes2int(b.raw[-6:]))
        except (AttributeError, TypeError, ValueError):
            pass

    def _netbios_macs():
        # get MAC addresses from NetBIOS.  See
        # <http://support.microsoft.com/kb/118623>.
        try:
            import netbios
            from win32wnet import Netbios

            ncb = netbios.NCB()
            ncb.Command = netbios.NCBENUM
            ncb.Buffer = a = netbios.LANA_ENUM()
            a._pack()
            if Netbios(ncb) == 0:
                a._unpack()
                for i in range(a.length):
                    ncb.Reset()
                    ncb.Command  = netbios.NCBRESET
                    ncb.Lana_num = _byte(a.lana[i])
                    if Netbios(ncb) == 0:
                        ncb.Reset()
                        ncb.Command  = netbios.NCBASTAT
                        ncb.Lana_num = _byte(a.lana[i])
                        ncb.Callname = '*'.ljust(16)
                        ncb.Buffer = s = netbios.ADAPTER_STATUS()
                        if Netbios(ncb) == 0:
                            s._unpack()
                            yield isMAC(_bytes2int(s.adapter_address[:6]))
        except (ImportError, AttributeError):
            pass

    _dirs = None  # ('c:\...', ...)

    def _ipconfig(tag, Class):
        # get IP or MAC addresses from ipconfig /all.
        global _dirs
        if _dirs is None:
            try:  # check system directory first
                f = ctypes.windll.kernel32.GetSystemDirectoryA
                b = ctypes.create_string_buffer(300)
                f(b, 300)
                t = (b.value.decode('mbcs'),)
            except (ImportError, AttributeError):
                t = ()
            _dirs = t + (r'c:\windows\system32',
                         r'c:\winnt\system32', '')

        m, c = [], _which('ipconfig.exe', _dirs)
        if c:
            for t in os.popen(c + ' /all'):
                if tag in t:
                    try:
                        t = t.split(':', 1)[1].strip()
                        m.append(Class(t))
                    except (IndexError, TypeError, ValueError):
                        pass
        return m

    def _ipconfig_ips():
        # get IP addresses from ipconfig.
        return _ipconfig('IP', IP)

    _MACsep = '-'

    def _ipconfig_macs():
        # get MAC addresses from ipconfig.
        return _ipconfig(_MACsep, MAC)

    _all_ips  = (_hostname_ips, _ipconfig_ips)
    _all_macs = (_windll_macs, _netbios_macs, _ipconfig_macs)

else:  # *nix

    _uuid_generate_time = None
    # If ctypes is available, use it to find routines for
    # UUID generation (making this module thread-UNsafe!)
    # Thanks to Thomas Heller for ctypes and for his help
    # with its use here.  See Lib/uuid.py for more.
    try:
        import ctypes.util
        # The uuid_generate_* routines are provided by
        # libuuid on at least Linux and FreeBSD and by
        # libc on MacOS X.
        for lib in ('uuid', 'c'):
            try:
                lib = ctypes.CDLL(ctypes.util.find_library(lib))
                _uuid_generate_time = getattr(lib, 'uuid_generate_time',
                                                   _uuid_generate_time)
            except (TypeError, AttributeError):
                lib = None
        del lib
    except (AttributeError, ImportError):
        pass

    _bins  = ('/bin',  '/usr/bin',  '')
    _sbins = ('/sbin', '/usr/sbin', '')

    def _run(cmd, opts, tag, offset, Class, cut_addr_=False):
        # get IP or MAC addresses from cmd output.
        c = '%s %s 2>/dev/null' % (cmd, opts)

        e = _which('env', _bins)
        if e:  # LC_ALL=C gets English output
            c = '%s LC_ALL=C %s' % (e, c)

        e = _which('grep', _bins)
        if e:  # pipe to case-insensitve grep
            c = '%s | %s -i %s' % (c, e, tag)  # tag.strip('()')

        if _debugf:
            _debugf('_run: %s', c)

        m = []
        for t in os.popen(c):
            t = t.lower().split()
            try:
                t = t[offset(t.index(tag))]
                # cut prefix from Linux inet addr:<IP>
                if cut_addr_ and t.startswith('addr:'):
                    t = t[5:]
                m.append(Class(t))
            except (IndexError, TypeError, ValueError):
                pass
        return m

    def _ifconfig_ips():
        # get IP addresses from ifconfig on MacOS ('-a'), Linux ('-a'
        # or ''), Tru64 ('-av'), Solaris ('-a') but not all *nixes.
        m, c = [], _which('ifconfig', _sbins)
        if c:
            for a in ('-a', '-av'):
                m = _run(c, a, 'inet', lambda i: i+1, IP, _cut_addr)
                if m:
                    break
        return m

    def _macs(cmd, opts, tag, offset):
        if cmd:  # get MAC addresses from cmd ...
            return _run(cmd, opts, tag, offset, MAC, False)
        return []

    def _ifconfig_macs():
        # get MAC addresses from ifconfig on MacOS ('-a'), Linux ('-a'
        # or ''), Tru64 ('-av'), but not all *nixes nor Solaris.
        m, c = [], _which('ifconfig', _sbins)
        for a, t in (('-a',  'ether'),   # MacOS
                     ('-a',  'hwaddr'),  # Linux
                     ('-av', 'ether'),
                     ('-av', 'hwaddr')):
            m = _macs(c, a, t, lambda i: i + 1)
            if m:
                break
        return m

    def _arp_macs():
        # get MAC addresses from arp on Solaris (and MacOS).
        m, c = [], _which('arp', _sbins)
        for a in getIPs():
            # using (c, '-an', '(%s)' % a, lambda i: i+2)
            # works on MacOS X, but then replace tag with
            # tag.strip('()') in the _grep format above
            m.extend(_macs(c, '-an', a, lambda i: -1))  # PYCHOK false
        return m

    def _lanscan_macs():
        # this might get MAC addresses on HP-UX.
        c = _which('lanscan', _sbins)
        return _macs(c, '-ai', 'lan0', lambda i: 0)  # PYCHOK false

    def _uuid_macs():
        # If the system provides UUID generator(s),
        # use those to extract the MAC address.

        # NOTE: the uuid's returned by iOS 9.3.2 on
        # iPad/iPhone are not persistent and may or
        # may not reflect the device MAC address.
        try:
            import uuid
            u = uuid.uuid1(clock_seq=0)
            yield isMAC(_bytes2int(u.bytes_le[-6:]))
        except (AttributeError, ImportError):
            pass

        if _uuid_generate_time:
            b = ctypes.create_string_buffer(16)
            if _uuid_generate_time(b) == 0:
                yield isMAC(_bytes2int(b.raw[-6:]))

    try:
        # Linux (and perhaps AIX, see <http://www.ibm.com/
        # developerworks/aix/library/au-ioctl-socket.html>)

        from fcntl import ioctl
        # see e.g. CentOS 4 /usr/include/linux/sockios.h or
        # <http://www.kernel-api.org/docs/online/1.2.13/df/
        # da2/sockios_8h-source.html>
        _SIOCGIFADDR  = 0x8915  # PA address
        _SIOCGIHWADDR = 0x8927  # hardware address

        def _ioctl_(SIOCG, Class):
            # see <http://code.activestate.com/recipes/439094
            # -get-the-ip-address-associated-with-a-network-inter/>
            m, c = [], 24 - Class.size
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for d in range(32):
                try:  # Linux ('eth'), MacOS ('en')
                    d = struct.pack('256s', 'eth' + str(d))
                    b = ioctl(s.fileno(), SIOCG, d)
                    # 32-bit IP addr is in bytes b[20:24]
                    # in network byte order, get IP addr
                    # str from socket.inet_ntoa(b[20:24]),
                    # 48-bit MAC addr is in bytes b[18:24]
                    m.append(Class(_bytes2int(b[c:24])))
                except (IOError, ValueError, TypeError):
                    if m:
                        break
            return m

        def _ioctl_ips():
            return _ioctl_(_SIOCGIFADDR, IP)

        def _ioctl_macs():
            return _ioctl_(_SIOCGIHWADDR, MAC)

    except ImportError:
        _ioctl_ips = _ioctl_macs = lambda: ()

    _cut_addr = False
    if sys.platform.startswith('darwin'):
        _all_ips  = (_hostname_ips, _ifconfig_ips)
        _all_macs = (_uuid_macs, _ifconfig_macs)
    elif sys.platform.startswith('iphone'):
        _all_ips  = (_hostname_ips,)
        _all_macs = (_uuid_macs,)
    elif sys.platform.startswith('linux'):
        _cut_addr = True
        _all_ips  = (_hostname_ips, _ioctl_ips, _ifconfig_ips)
        _all_macs = (_uuid_macs, _ioctl_macs, _ifconfig_macs)
    elif sys.platform.startswith('sunos'):
        _all_ips  = (_hostname_ips, _ifconfig_ips)
        _all_macs = (_uuid_macs, _arp_macs)
    else:  # not tested!
        _all_ips  = (_hostname_ips, _ifconfig_ips)
        _all_macs = (_uuid_macs, _ifconfig_macs, _lanscan_macs)

# see Python recipe <http://code.activestate.com/recipes/66517
# -ip-address-conversion-functions-with-the-builtin-s/?in=user-97991>
_NET = '!L'  # network byte order (big-endian)


def _ip42int(addr, *unused):
    # convert a dot-quad IP addr to an _NET int
    # (raises socket.error for invalid addr)
    return struct.unpack(_NET, socket.inet_aton(addr))[0]


def _ip42str(ip):
    # convert an int to dot-quad IP string
    return socket.inet_ntoa(struct.pack(_NET, ip))


def _ip4int(ip):
    # check an int IP (avoid the DeprecationWarning:
    # struct integer overflow masking is deprecated)
    if 0 <= ip < _b32:  # IP
        return _ip42int(_ip42str(ip))
    raise ValueError('IP out of range: %r' % ip)


def _ip4masks(bits):
    # return an IP net and host mask
    if 0 < bits <= 32:
        b = 1 << (32 - bits)
        return (_b32 - b), (b - 1)
    raise ValueError('invalid IP mask width: %r' % (bits,))


def _ip4isnet(ip, net):
    # check whether an int IP is in the given net
    a, m, _ = _ip4netuple(net)
    return (ip & m) == a  # and ip != a?


_ip4nets = {}  # IP net (addr, mask) cache

# see RFCs and <http://code.google.com/p/ipaddr-py/>
_IP4NET_LINKLOCAL = '169.254.0.0/16'  # RFC 3927
_IP4NET_LOOPBACK  = '127.0.0.0/8'     # RFC 5735
_IP4NET_MULTICAST = '224.0.0.0/4'     # RFC 3171
_IP4NET_PRIVATE_A = '10.0.0.0/8'      # RFC 1918
_IP4NET_PRIVATE_B = '172.16.0.0/12'   # RFC 1918
_IP4NET_PRIVATE_C = '192.168.0.0/16'  # RFC 1918
_IP4NET_TEST_NET  = '192.0.2.0/24'    # RFC 5735
_IP4NET_THIS_HOST = '0.0.0.0/32'      # RFC 5735
_IP4NET_THIS_NET  = '0.0.0.0/8'       # RFC 5735


def _ip4isnet_(addr_mask_cast, ip):
    # check network addr, mask or cast match
    return ip in [_ip4netuple(n)[addr_mask_cast] for
            n in (_IP4NET_LINKLOCAL,
                  _IP4NET_LOOPBACK,
                  _IP4NET_MULTICAST,
                  _IP4NET_PRIVATE_A,
                  _IP4NET_PRIVATE_B,
                  _IP4NET_PRIVATE_C,
                  _IP4NET_TEST_NET,
                  _IP4NET_THIS_HOST,
                  _IP4NET_THIS_NET)]


def _ip4net(ip):
    # return containing IP net or an empty string
    for n in (_IP4NET_PRIVATE_A,
              _IP4NET_PRIVATE_B,
              _IP4NET_PRIVATE_C,
              _IP4NET_TEST_NET,
              _IP4NET_LOOPBACK,
              _IP4NET_LINKLOCAL,
              _IP4NET_MULTICAST,
              _IP4NET_THIS_HOST,
              _IP4NET_THIS_NET):
        if _ip4isnet(ip, n):
            return n
    return ''  # no network


def _ip4netuple(net):
    # return an IP net addr, mask and cast
    t = _ip4nets.get(net, None)
    if t is None:
        a, b = net.split('/')
        m, b = _ip4masks(int(b))
        a = _ip42int(a) & m
        t =  a, m, (a | b)
        _ip4nets[net] = t
        if _debugf:
            _debugf('_ip4nets[%r]: (addr 0x%08x, mask 0x%08x, cast 0x%08x)', net, *t)
    return t


def _mac2int(addr, sep=_MACsep):
    # convert a MAC str to an int
    h = addr.split(sep)
    if len(h) > 4:
        i = 0
        for b in h:
            b = int(b, 16)
            if 0 <= b < _b08:
                i = (i << 8) + b
            else:
                break  # raise
        else:
            if 0 < i < _b48:
                return i
    raise ValueError('invalid MAC address: %r' % (addr,))


def _macint(mac):
    # check an int MAC
    if 0 < mac < _b48:
        return mac
    raise ValueError('MAC out of range: %r' % (mac,))


class _Base(object):
    '''Base class for IP and MAC classes.
    '''
    _int = 0  # value as int

    def __init__(self, addr, addr2int, addrint):
        try:
            if isinstance(addr, self.__class__):
                i = addr._int
            elif isinstance(addr, _Strs):
                if self.sep in addr:  # PYCHOK false
                    i = addr2int(addr, self.sep)  # PYCHOK false
                elif addr[:2].lower() == '0x':
                    i = addrint(int(addr, 16))
                else:
                    i = addrint(int(addr, 10))
            elif isinstance(addr, _Ints):
                i = addrint(addr)
            else:
                raise TypeError('%s invalid: %s' %
                                (self.__class__.__name__, type(addr)))
            self.__dict__['_int'] = i  # immutable
        except (socket.error, ValueError):
            raise ValueError('%s invalid: %r' %
                             (self.__class__.__name__, addr))
        if _debugf:
            _debugf('_Base(%r): %r', addr, self)

    # see Python 2.6 and 3.1 Lib/uuid.py

    def __cmp__(self, other):  # 2.x
        if isinstance(other, self.__class__):
            return cmp(self._int, other._int)
        return NotImplemented

    def __eq__(self, other):  # 3.x
        if isinstance(other, self.__class__):
            return self._int == other._int
        return NotImplemented

    def __ne__(self, other):  # 3.x
        if isinstance(other, self.__class__):
            return self._int != other._int
        return NotImplemented

    # Q. What's the value of being able to sort UUIDs?
    # A. Use them as keys in a B-Tree or similar mapping.

    def __lt__(self, other):  # 3.x
        if isinstance(other, self.__class__):
            return self._int < other._int
        return NotImplemented

    def __gt__(self, other):  # 3.x
        if isinstance(other, self.__class__):
            return self._int > other._int
        return NotImplemented

    def __le__(self, other):  # 3.x
        if isinstance(other, self.__class__):
            return self._int <= other._int
        return NotImplemented

    def __ge__(self, other):  # 3.x
        if isinstance(other, self.__class__):
            return self._int >= other._int
        return NotImplemented

    def __hash__(self):
        return hash(self._int)

    def __hex__(self):  # 2.6+
        return self.HEX % (self._int,)  # PYCHOK false
    hex = property(__hex__, doc='This address as hexadecimal string, see the .HEX attribute.')

    def __int__(self):  # 2.6+
        return self._int
    int = property(__int__, doc='This address as an int.')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, attr, value):  # PYCHOK expected
        raise TypeError('%s objects are immutable' % (self.__class__.__name__,))


class IP(_Base):
    '''IP address class.
    '''
    HEX  = '0x%08x'  # hex format (or '%#010x')
    sep  = _IPsep
    size = 4  # bytes

    def __init__(self, addr):
        '''Construct an IP instance from a dot-quad string, a hexa/decimal
           string, an integer value or from another IP instance.

           Raises a TypeError or ValueError for an invalid address.
        '''
        _Base.__init__(self, addr, _ip42int, _ip4int)

    def __linklocal(self):
        return _ip4isnet(self._int, _IP4NET_LINKLOCAL)
    islinklocal = property(__linklocal, doc='True if an IP link-local address per RFC 3927.')

    def __loopback(self):
        return _ip4isnet(self._int, _IP4NET_LOOPBACK)
    isloopback = property(__loopback, doc='True if an IP loopback address per RFC 5735.')

    def __multicast(self):
        return _ip4isnet(self._int, _IP4NET_MULTICAST)
    ismulticast = property(__multicast, doc='True if an IP multicast (class D) address per RFC 3171.')

    def __netcast(self):
        return _ip4isnet_(2, self._int)
    isnetcast = property(__netcast, doc='True if an IP network broadcast.')

    def __netmask(self):
        return _ip4isnet_(1, self._int)
    isnetmask = property(__netmask, doc='True if an IP network mask.')

    def __network(self):
        return _ip4isnet_(0, self._int)
    isnetwork = property(__network, doc='True if an IP network address.')

    def __private(self):
        return self.isprivateA or \
               self.isprivateB or \
               self.isprivateC
    isprivate = property(__private, doc='True if a private (non-routable) IP address per RFC 1918.')

    def __privateA(self):
        return _ip4isnet(self._int, _IP4NET_PRIVATE_A)
    isprivateA = property(__privateA, doc='True if a private (class A) IP address per RFC 1918.')

    def __privateB(self):
        return _ip4isnet(self._int, _IP4NET_PRIVATE_B)
    isprivateB = property(__privateB, doc='True if a private (class B) IP address per RFC 1918.')

    def __privateC(self):
        return _ip4isnet(self._int, _IP4NET_PRIVATE_C)
    isprivateC = property(__privateC, doc='True if a private (class C) IP address per RFC 1918.')

    def __reserved(self):
        return self.isloopback  or \
               self.islinklocal or \
               self.ismulticast or \
               self.isnetmask   or \
               self.isnetwork
    isreserved = property(__reserved, doc='True if link-local, loopback, multicast, netmask or network.')

    def __testnet(self):
        return _ip4isnet(self._int, _IP4NET_TEST_NET)
    istestnet = property(__testnet, doc='True if a TEST-NET (class E) IP address per RFC 5735.')

    def __thishost(self):
        return _ip4isnet(self._int, _IP4NET_THIS_HOST)
    isthishost = property(__thishost, doc='True if a THIS-HOST IP address per RFC 5735.')

    def __thisnet(self):
        return _ip4isnet(self._int, _IP4NET_THIS_NET)
    isthisnet = property(__thisnet, doc='True if a THIS-NET IP address per RFC 5735.')

    def __net(self):
        return _ip4net(self._int)
    net = property(__net, doc='The containing IP network or an empty string.')

    def __str__(self):
        return _ip42str(self._int)
    str = property(__str__, doc='This IP address as a dot-quad string.')

    def __ton(self):
        return self._int  # is in network byte order
    ton = property(__ton, doc='This IP address as an int in network byte order.')

    def __toh(self):
        return socket.ntohl(self._int)
    toh = property(__toh, doc='This IP address as an int in host byte order.')


class MAC(_Base):
    '''MAC address class.
    '''
    HEX  = '0x%012x'  # hex format (or '%#014x')
    sep  = _MACsep
    size =  6  # bytes

    def __init__(self, addr):
        '''Construct a MAC instance from an address string, a hexa/decimal
           string, an integer value or from another MAC instance.

           Raises a TypeError or ValueError for an invalid address.
        '''
        _Base.__init__(self, addr, _mac2int, _macint)

    def __str__(self):
        h = '%012x' % self._int
        return self.sep.join([h[d:d+2] for d in range(0, len(h), 2)])
    str = property(__str__, doc='''This MAC address as a 12-digit hexadecimal
                                   string, separated by the MAC.sep attribute.''')


def _gets(gens, exclude):
    '''Return all IP or MAC addresses subject to exclude.
    '''
    x = exclude
    if x is None:
        x = lambda _: False  # PYCHOK expected
    elif not hasattr(x, '__call__'):
        raise TypeError('exclude not callable: %r' % (x,))

    t = []
    for g in gens:
        for a in g():
            if _debugf:
                _debugf('%s yields: %r', g.__name__, a)
            if a and a not in t and not x(a):
                t.append(a)
    t = tuple(t)

    if _debugf:
        _debugf('_gets(exclude=%r): %r', exclude, t)
    return t


def getIPs(exclude=lambda ip: ip.isreserved):
    '''Get all unique IP addresses as a tuple of IP instances.

       By default, all reserved IP addresses are excluded.  Set
       optional argument exclude=None to include all IP addresses
       or provide a callable returning True or False to exclude
       respectively include a given IP instance.
    '''
    return _gets(_all_ips, exclude)


def getMACs(exclude=None):
    '''Get all unique MAC addresses as a tuple of MAC instances.

       By default, optional argument exclude=None to include all
       MAC addresses.  Provide a callable returning True or False
       to exclude respectively include a given MAC instance.
    '''
    return _gets(_all_macs, exclude)


def isIP(addr):
    '''Return an IP instance for a valid IP address, None otherwise.
    '''
    try:
        return IP(addr)
    except (TypeError, ValueError):
        return None


def isMAC(addr):
    '''Return a MAC instance for a valid MAC address, None otherwise.
    '''
    try:
        return MAC(addr)
    except (TypeError, ValueError):
        return None


if __name__ == '__main__':

    _argv0 = sys.argv[0] + ' '

    def printf(fmt, *args):
        # Formatted print.
        print(_argv0 + fmt % args)

    if sys.argv[-1] in ('-debug', '-d'):
        _debugf = printf

    printf('%s using Python %s on %s\n', __version__,
            sys.version.split()[0], sys.platform)

    def test(Class, gets):

        n = Class.__name__

        global e, t
        e = t = 0

        def check(value, *expected):
            global e, t
            t += 1
            if value not in expected:
                x = ', '.join([repr(x) for x in expected])
                printf('%s error: %r, expected %s',
                        n, value, x)
                e += 1

        s = gets()
        printf('get%ss(): %r', n, s)
        check(gets(), s)

        for a in s:
            # check immutable
            check(a.HEX, Class.HEX)
            check(a.sep, Class.sep)
            check(a.size, Class.size)
            try:
                a.size = 0
                check(a.size, TypeError.__name__)
            except TypeError:
                check(a.size, Class.size)

            # check constructor
            check(Class(a), a)
            check(Class(a.hex), a)
            check(Class(a.int), a)
            check(Class(str(a)), a)
            check(Class(str(a.int)), a)

            r = repr(a)
            printf('%s.str: %r', r, a.str)
            printf('%s.hex: %r', r, a.hex)
            printf('%s.int:  %x (%%x)', r, a.int)
            printf('%s.int:  %d (%%d)', r, a.int)

            if Class is IP:
                printf('%s.ton:  %x (%%x)', r, a.ton)
                printf('%s.toh:  %x (%%x)', r, a.toh)
                printf('%s.net: %r',   r, a.net)
                for m in dir(a):
                    if m.startswith('is'):
                        # check is... properties
                        p = getattr(a, m)
                        printf('%s.%-12s %r', r, m + ':', p)
                        if m.startswith('isprivate'):
                            check(p, False, True)
                        else:
                            check(p, False)
                        # check immutability
                        try:
                            x = None
                            setattr(a, p, True)
                        except:
                            x = sys.exc_info()[0]
                        check(x, TypeError)

        # check Errors
        for v, X in (('text', ValueError),
                     (None,   TypeError),
                     ([],     TypeError),
                     (Class,  TypeError)):
            try:
                x = None
                Class(v)
            except:
                x = sys.exc_info()[0]
            check(x, X)

        # check exclude None case
        check(gets(None), gets(None))

        printf('%s errors in %d tests\n', e or 'no', t)
        return e

    e = test(IP,  getIPs) + \
        test(MAC, getMACs)
    printf('%s errors in total', e or 'no')
