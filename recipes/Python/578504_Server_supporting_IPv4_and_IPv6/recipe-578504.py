"""
Utility functions to create server sockets able to listen on both
IPv4 and IPv6.  Inspired by: http://bugs.python.org/issue17561

Expected usage:

>>> sock = create_server_sock(("", 8000))
>>> if not has_dual_stack(sock):
...     sock.close()
...     sock = MultipleSocketsListener([("0.0.0.0", 8000), ("::", 8000)])
>>>

From here on you have a socket which listens on port 8000,
all interfaces, serving both IPv4 and IPv6.
You can start accepting new connections as usual:

>>> while True:
...     conn, addr = sock.accept()
...     # handle new connection

Supports UNIX, Windows, non-blocking sockets and socket timeouts.
Works with Python >= 2.6 and 3.X.
"""


import os
import sys
import socket
import select
import contextlib


__author__ = "Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>"
__license__ = "MIT"


def has_dual_stack(sock=None):
    """Return True if kernel allows creating a socket which is able to
    listen for both IPv4 and IPv6 connections.
    If *sock* is provided the check is made against it.
    """
    try:
        socket.AF_INET6
        socket.IPPROTO_IPV6
        socket.IPV6_V6ONLY
    except AttributeError:
        return False
    try:
        if sock is not None:
            return not sock.getsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY)
        else:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            with contextlib.closing(sock):
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
                return True
    except socket.error:
        return False


def create_server_sock(address, family=None, reuse_addr=None, queue_size=5,
                       dual_stack=has_dual_stack()):
    """Convenience function which creates a TCP server bound to
    *address* and return the socket object.

    Internally it takes care of choosing the right address family
    (IPv4 or IPv6) depending on the host specified in *address*
    (a (host, port) tuple.
    If host is an empty string or None all interfaces are assumed
    and if dual stack is supported by kernel the socket will be
    able to listen for both IPv4 and IPv6 connections.

    *family* can be set to either AF_INET or AF_INET6 to force the
    socket to use IPv4 or IPv6. If not set it will be determined
    from host.

    *reuse_addr* tells the kernel to reuse a local socket in TIME_WAIT
    state, without waiting for its natural timeout to expire.
    If not set will default to True on POSIX.

    *queue_size* is the maximum number of queued connections passed to
    listen() (defaults to 5).

    If *dual_stack* if True it will force the socket to listen on both
    IPv4 and IPv6 connections (defaults to True on all platforms
    natively supporting this functionality).

    The returned socket can be used to accept() new connections as in:

    >>> server = create_server_sock((None, 8000))
    >>> while True:
    ...     sock, addr = server.accept()
    ...     # handle new sock connection
    """
    AF_INET6 = getattr(socket, 'AF_INET6', 0)
    host, port = address
    if host == "":
        # http://mail.python.org/pipermail/python-ideas/2013-March/019937.html
        host = None
    if host is None and dual_stack:
        host = "::"
    if family is None:
        family = socket.AF_UNSPEC
    if reuse_addr is None:
        reuse_addr = os.name == 'posix' and sys.platform != 'cygwin'
    err = None
    info = socket.getaddrinfo(host, port, family, socket.SOCK_STREAM,
                              0, socket.AI_PASSIVE)
    if not dual_stack:
        # in case dual stack is not supported we want IPv4 to be
        # preferred over IPv6
        info.sort(key=lambda x: x[0] == socket.AF_INET, reverse=True)
    for res in info:
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket.socket(af, socktype, proto)
            if reuse_addr:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if af == AF_INET6:
                if dual_stack:
                    # enable
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
                elif has_dual_stack(sock):
                    # disable
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            sock.bind(sa)
            sock.listen(queue_size)
            return sock
        except socket.error as _:
            err = _
            if sock is not None:
                sock.close()
    if err is not None:
        raise err
    else:
        raise socket.error("getaddrinfo returns an empty list")


class MultipleSocketsListener:
    """Listen on multiple addresses specified as a list of
    (host, port) tuples.
    Useful to listen on both IPv4 and IPv6 on those systems where
    a dual stack is not supported natively (Windows and many UNIXes).

    The returned instance is a socket-like object which can be used to
    accept() new connections, as with a common socket.
    Calls like settimeout() and setsockopt() will be applied to all
    sockets.
    Calls like gettimeout() or getsockopt() will refer to the first
    socket in the list.
    """

    def __init__(self, addresses, family=None, reuse_addr=None, queue_size=5):
        self._socks = []
        self._sockmap = {}
        if hasattr(select, 'poll'):
            self._pollster = select.poll()
        else:
            self._pollster = None
        completed = False
        try:
            for addr in addresses:
                sock = create_server_sock(
                    addr, family=family, reuse_addr=reuse_addr,
                    queue_size=queue_size, dual_stack=False)
                self._socks.append(sock)
                fd = sock.fileno()
                if self._pollster is not None:
                    self._pollster.register(fd, select.POLLIN)
                self._sockmap[fd] = sock
            completed = True
        finally:
            if not completed:
                self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        addrs = []
        for sock in self._socks:
            try:
                addrs.append(sock.getsockname())
            except socket.error:
                addrs.append(())
        return '<%s (%r) at %#x>' % (self.__class__.__name__, addrs, id(self))

    def _poll(self):
        """Return the first readable fd."""
        timeout = self.gettimeout()
        if self._pollster is None:
            fds = select.select(self._sockmap.keys(), [], [], timeout)
            if timeout and fds == ([], [], []):
                raise socket.timeout('timed out')
        else:
            if timeout is not None:
                timeout *= 1000
            fds = self._pollster.poll(timeout)
            if timeout and fds == []:
                raise socket.timeout('timed out')
        try:
            return fds[0][0]
        except IndexError:
            pass  # non-blocking socket

    def _multicall(self, name, *args, **kwargs):
        for sock in self._socks:
            meth = getattr(sock, name)
            meth(*args, **kwargs)

    def accept(self):
        """Accept a connection from the first socket which is ready
        to do so.
        """
        fd = self._poll()
        sock = self._sockmap[fd] if fd else self._socks[0]
        return sock.accept()

    def filenos(self):
        """Return sockets' file descriptors as a list of integers.
        This is useful with select().
        """
        return list(self._sockmap.keys())

    def getsockname(self):
        """Return first registered socket's own address."""
        return self._socks[0].getsockname()

    def getsockopt(self, level, optname, buflen=0):
        """Return first registered socket's options."""
        return self._socks[0].getsockopt(level, optname, buflen)

    def gettimeout(self):
        """Return first registered socket's timeout."""
        return self._socks[0].gettimeout()

    def settimeout(self, timeout):
        """Set timeout for all registered sockets."""
        self._multicall('settimeout', timeout)

    def setblocking(self, flag):
        """Set non/blocking mode for all registered sockets."""
        self._multicall('setblocking', flag)

    def setsockopt(self, level, optname, value):
        """Set option for all registered sockets."""
        self._multicall('setsockopt', level, optname, value)

    def shutdown(self, how):
        """Shut down all registered sockets."""
        self._multicall('shutdown', how)

    def close(self):
        """Close all registered sockets."""
        self._multicall('close')
        self._socks = []
        self._sockmap.clear()


# ===================================================================
# --- tests
# ===================================================================


if __name__ == '__main__':
    import unittest
    import threading
    import errno
    import time
    try:
        from test.support import find_unused_port  # PY3
    except ImportError:
        from test.test_support import find_unused_port  # PY2

    class TestCase(unittest.TestCase):

        def echo_server(self, sock):
            def run():
                with contextlib.closing(sock):
                    conn, _ = sock.accept()
                    with contextlib.closing(conn) as conn:
                        msg = conn.recv(1024)
                        if not msg:
                            return
                        conn.sendall(msg)

            t = threading.Thread(target=run)
            t.start()
            time.sleep(.1)

        def test_create_server_sock(self):
            port = find_unused_port()
            sock = create_server_sock((None, port))
            with contextlib.closing(sock):
                self.assertEqual(sock.getsockname()[1], port)
                self.assertEqual(sock.type, socket.SOCK_STREAM)
                if has_dual_stack():
                    self.assertEqual(sock.family, socket.AF_INET6)
                else:
                    self.assertEqual(sock.family, socket.AF_INET)
                self.echo_server(sock)
                cl = socket.create_connection(('localhost', port), timeout=2)
                with contextlib.closing(cl):
                    cl.sendall(b'foo')
                    self.assertEqual(cl.recv(1024), b'foo')

        def test_has_dual_stack(self):
            # IPv4 sockets are not supposed to support dual stack
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with contextlib.closing(sock):
                sock.bind(("", 0))
                self.assertFalse(has_dual_stack(sock=sock))

        def test_dual_stack(self):
            sock = create_server_sock((None, 0))
            with contextlib.closing(sock):
                self.echo_server(sock)
                port = sock.getsockname()[1]
                cl = socket.create_connection(("127.0.0.1", port), timeout=2)
                with contextlib.closing(cl):
                    cl.sendall(b'foo')
                    self.assertEqual(cl.recv(1024), b'foo')

            sock = create_server_sock((None, 0))
            with contextlib.closing(sock):
                self.echo_server(sock)
                port = sock.getsockname()[1]
                if has_dual_stack():
                    self.assertTrue(has_dual_stack(sock=sock))
                    cl = socket.create_connection(("::1", port), timeout=2)
                    with contextlib.closing(cl):
                        cl.sendall(b'foo')
                        self.assertEqual(cl.recv(1024), b'foo')
                else:
                    self.assertFalse(has_dual_stack(sock=sock))
                    try:
                        socket.create_connection(("::1", port))
                    except socket.error as err:
                        if os.name == 'nt':
                            code = errno.WSAECONNREFUSED
                        else:
                            code = errno.ECONNREFUSED
                        self.assertEqual(err.errno, code)
                    else:
                        self.fail('exception not raised')

                    # just stop server
                    cl = socket.create_connection(("127.0.0.1", port), timeout=2)
                    with contextlib.closing(sock):
                        cl.sendall(b'foo')
                        cl.recv(1024)
                    if hasattr(unittest, 'skip'):  # PY >= 2.7
                        unittest.skip('dual stack cannot be tested as not '
                                      'supported')

        # --- multiple listener tests

        def test_mlistener(self):
            port = find_unused_port()
            # v4
            sock = MultipleSocketsListener(
                [('127.0.0.1', port), ('::1', port)])
            with contextlib.closing(sock):
                self.echo_server(sock)
                port = sock.getsockname()[1]
                cl = socket.create_connection(("127.0.0.1", port), timeout=2)
                with contextlib.closing(cl):
                    cl.sendall(b'foo')
                    self.assertEqual(cl.recv(1024), b'foo')
            # v6
            sock = MultipleSocketsListener(
                [('127.0.0.1', port), ('::1', port)])
            with contextlib.closing(sock):
                self.echo_server(sock)
                port = sock.getsockname()[1]
                cl = socket.create_connection(("::1", port), timeout=2)
                with contextlib.closing(cl):
                    cl.sendall(b'foo')
                    self.assertEqual(cl.recv(1024), b'foo')

        def test_mlistener_timeout(self):
            sock = MultipleSocketsListener([('127.0.0.1', 0), ('::1', 0)])
            sock.settimeout(.01)
            self.assertRaises(socket.timeout, sock.accept)

        def test_mlistener_nonblocking(self):
            sock = MultipleSocketsListener([('127.0.0.1', 0), ('::1', 0)])
            sock.setblocking(False)
            try:
                sock.accept()
            except socket.error as err:
                if os.name == 'nt':
                    code = errno.WSAEWOULDBLOCK
                else:
                    code = errno.EAGAIN
                self.assertEqual(err.errno, code)
            else:
                self.fail('exception not raised')

        def test_mlistener_ctx_manager(self):
            with MultipleSocketsListener([("0.0.0.0", 0), ("::", 0)]) as msl:
                pass
            self.assertEqual(msl._socks, [])
            self.assertEqual(msl._sockmap, {})

        def test_mlistener_overridden_meths(self):
            with MultipleSocketsListener([("0.0.0.0", 0), ("::", 0)]) as msl:
                self.assertEqual(
                    bool(msl.getsockopt(
                        socket.SOL_SOCKET, socket.SO_REUSEADDR)),
                    os.name == 'posix')
                self.assertEqual(msl.getsockname()[0], "0.0.0.0")
                self.assertTrue(msl.filenos())
                msl.setblocking(True)
                msl.settimeout(2)
                self.assertEqual(msl.gettimeout(), 2)
                try:
                    msl.setsockopt(
                        socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
                except socket.error:
                    pass

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestCase))
    unittest.TextTestRunner(verbosity=2).run(test_suite)
