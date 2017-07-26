#!/usr/bin/env python

"""
This is a backport of socket.sendfile() for Python 2.6 and 2.7.
socket.sendfile() will be included in Python 3.5:
http://bugs.python.org/issue17552

This recipe allows to send a file over a socket by using
high-performance sendfile() syscall, which on Linux is about twice as
fast as using the usual file.read() / socket.send() calls (see:
https://github.com/giampaolo/pysendfile#a-simple-benchmark)

On UNIX, in order for this to work you need to install pysendfile first
(https://github.com/giampaolo/pysendfile) with "pip install pysendfile".
On Windows plain send() will automatically be used as fallback.

Usage:

>>> import socket
>>> file = open("somefile.bin", "rb")
>>> sock = socket.create_connection(("localhost", 8021))
>>> sendfile(sock, file)
423192837
>>>

Original code including tests (which are not included in this recipe)
is available here:
https://code.google.com/p/billiejoex/source/browse/works/socket_sendfile.py

Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT
"""

import errno
import io
import os
import select
import socket
try:
    memoryview  # py 2.7 only
except NameError:
    memoryview = lambda x: x

if os.name == 'posix':
    import sendfile as pysendfile  # requires "pip install pysendfile"
else:
    pysendfile = None


_RETRY = frozenset((errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK,
                    errno.EINPROGRESS))


class _GiveupOnSendfile(Exception):
    pass


if pysendfile is not None:

    def _sendfile_use_sendfile(sock, file, offset=0, count=None):
        _check_sendfile_params(sock, file, offset, count)
        sockno = sock.fileno()
        try:
            fileno = file.fileno()
        except (AttributeError, io.UnsupportedOperation) as err:
            raise _GiveupOnSendfile(err)  # not a regular file
        try:
            fsize = os.fstat(fileno).st_size
        except OSError:
            raise _GiveupOnSendfile(err)  # not a regular file
        if not fsize:
            return 0  # empty file
        blocksize = fsize if not count else count

        timeout = sock.gettimeout()
        if timeout == 0:
            raise ValueError("non-blocking sockets are not supported")
        # poll/select have the advantage of not requiring any
        # extra file descriptor, contrarily to epoll/kqueue
        # (also, they require a single syscall).
        if hasattr(select, 'poll'):
            if timeout is not None:
                timeout *= 1000
            pollster = select.poll()
            pollster.register(sockno, select.POLLOUT)

            def wait_for_fd():
                if pollster.poll(timeout) == []:
                    raise socket._socket.timeout('timed out')
        else:
            # call select() once in order to solicit ValueError in
            # case we run out of fds
            try:
                select.select([], [sockno], [], 0)
            except ValueError:
                raise _GiveupOnSendfile(err)

            def wait_for_fd():
                fds = select.select([], [sockno], [], timeout)
                if fds == ([], [], []):
                    raise socket._socket.timeout('timed out')

        total_sent = 0
        # localize variable access to minimize overhead
        os_sendfile = pysendfile.sendfile
        try:
            while True:
                if timeout:
                    wait_for_fd()
                if count:
                    blocksize = count - total_sent
                    if blocksize <= 0:
                        break
                try:
                    sent = os_sendfile(sockno, fileno, offset, blocksize)
                except OSError as err:
                    if err.errno in _RETRY:
                        # Block until the socket is ready to send some
                        # data; avoids hogging CPU resources.
                        wait_for_fd()
                    else:
                        if total_sent == 0:
                            # We can get here for different reasons, the main
                            # one being 'file' is not a regular mmap(2)-like
                            # file, in which case we'll fall back on using
                            # plain send().
                            raise _GiveupOnSendfile(err)
                        raise err
                else:
                    if sent == 0:
                        break  # EOF
                    offset += sent
                    total_sent += sent
            return total_sent
        finally:
            if total_sent > 0 and hasattr(file, 'seek'):
                file.seek(offset)
else:
    def _sendfile_use_sendfile(sock, file, offset=0, count=None):
        raise _GiveupOnSendfile(
            "sendfile() not available on this platform")


def _sendfile_use_send(sock, file, offset=0, count=None):
    _check_sendfile_params(sock, file, offset, count)
    if sock.gettimeout() == 0:
        raise ValueError("non-blocking sockets are not supported")
    if offset:
        file.seek(offset)
    blocksize = min(count, 8192) if count else 8192
    total_sent = 0
    # localize variable access to minimize overhead
    file_read = file.read
    sock_send = sock.send
    try:
        while True:
            if count:
                blocksize = min(count - total_sent, blocksize)
                if blocksize <= 0:
                    break
            data = memoryview(file_read(blocksize))
            if not data:
                break  # EOF
            while True:
                try:
                    sent = sock_send(data)
                except OSError as err:
                    if err.errno in _RETRY:
                        continue
                    raise
                else:
                    total_sent += sent
                    if sent < len(data):
                        data = data[sent:]
                    else:
                        break
        return total_sent
    finally:
        if total_sent > 0 and hasattr(file, 'seek'):
            file.seek(offset + total_sent)


def _check_sendfile_params(sock, file, offset, count):
    if 'b' not in getattr(file, 'mode', 'b'):
        raise ValueError("file should be opened in binary mode")
    if not sock.type & socket.SOCK_STREAM:
        raise ValueError("only SOCK_STREAM type sockets are supported")
    if count is not None:
        if not isinstance(count, int):
            raise TypeError(
                "count must be a positive integer (got %s)" % repr(count))
        if count <= 0:
            raise ValueError(
                "count must be a positive integer (got %s)" % repr(count))


def sendfile(sock, file, offset=0, count=None):
    """sendfile(sock, file[, offset[, count]]) -> sent

    Send a *file* over a connected socket *sock* until EOF is
    reached by using high-performance sendfile(2) and return the
    total number of bytes which were sent.
    *file* must be a regular file object opened in binary mode.
    If sendfile() is not available (e.g. Windows) or file is
    not a regular file socket.send() will be used instead.
    *offset* tells from where to start reading the file.
    If specified, *count* is the total number of bytes to transmit
    as opposed to sending the file until EOF is reached.
    File position is updated on return or also in case of error in
    which case file.tell() can be used to figure out the number of
    bytes which were sent.
    The socket must be of SOCK_STREAM type.
    Non-blocking sockets are not supported.
    """
    try:
        return _sendfile_use_sendfile(sock, file, offset, count)
    except _GiveupOnSendfile:
        return _sendfile_use_send(sock, file, offset, count)


###########################################################################
# --- tests
###########################################################################


if __name__ == '__main__':
    import contextlib
    import threading
    import Queue
    import thread
    import random
    import string
    import sys

    if sys.version_info < (2, 7):
        import unittest2 as unittest  # requires "pip install unittest2"
    else:
        import unittest

    TESTFN = "$testfile"

    def unlink(fname):
        try:
            os.remove(fname)
        except OSError:
            pass

    def bind_port(sock, host="localhost"):
        if sock.family == socket.AF_INET and sock.type == socket.SOCK_STREAM:
            if hasattr(socket, 'SO_REUSEADDR'):
                if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) == 1:
                    raise ValueError("tests should never set the SO_REUSEADDR "
                                     "socket option on TCP/IP sockets!")
            if hasattr(socket, 'SO_REUSEPORT'):
                try:
                    if sock.getsockopt(socket.SOL_SOCKET,
                                       socket.SO_REUSEPORT) == 1:
                        raise ValueError(
                            "tests should never set the SO_REUSEPORT "
                            "socket option on TCP/IP sockets!")
                except OSError:
                    # Python's socket module was compiled using modern headers
                    # thus defining SO_REUSEPORT but this process is running
                    # under an older kernel that does not support SO_REUSEPORT.
                    pass
            if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)

        sock.bind((host, 0))
        port = sock.getsockname()[1]
        return port

    @contextlib.contextmanager
    def create_connection(address, timeout=None):
        sock = socket.socket()
        sock.connect(address)
        if timeout is not None:
            sock.settimeout(timeout)
        try:
            yield sock
        finally:
            sock.close()

    class ThreadableTest:
        """Threadable Test class

        The ThreadableTest class makes it easy to create a threaded
        client/server pair from an existing unit test. To create a
        new threaded class from an existing unit test, use multiple
        inheritance:

           class NewClass (OldClass, ThreadableTest):
                pass

        This class defines two new fixture functions with obvious
        purposes for overriding:

            clientSetUp ()
            clientTearDown ()

        Any new test functions within the class must then define
        tests in pairs, where the test name is preceeded with a
        '_' to indicate the client portion of the test. Ex:

            def testFoo(self):
                # Server portion

            def _testFoo(self):
                # Client portion

        Any exceptions raised by the clients during their tests
        are caught and transferred to the main thread to alert
        the testing framework.

        Note, the server setup function cannot call any blocking
        functions that rely on the client thread during setup,
        unless serverExplicitReady() is called just before
        the blocking call (such as in setting up a client/server
        connection and performing the accept() in setUp().
        """

        def __init__(self):
            # Swap the true setup function
            self.__setUp = self.setUp
            self.__tearDown = self.tearDown
            self.setUp = self._setUp
            self.tearDown = self._tearDown

        def serverExplicitReady(self):
            """This method allows the server to explicitly indicate that
            it wants the client thread to proceed. This is useful if the
            server is about to execute a blocking routine that is
            dependent upon the client thread during its setup routine."""
            self.server_ready.set()

        def _setUp(self):
            self.server_ready = threading.Event()
            self.client_ready = threading.Event()
            self.done = threading.Event()
            self.queue = Queue.Queue(1)
            self.server_crashed = False

            # Do some munging to start the client test.
            methodname = self.id()
            i = methodname.rfind('.')
            methodname = methodname[i+1:]
            test_method = getattr(self, '_' + methodname)
            self.client_thread = thread.start_new_thread(
                self.clientRun, (test_method,))

            try:
                try:
                    self.__setUp()
                except:
                    self.server_crashed = True
                    raise
            finally:
                self.server_ready.set()
            self.client_ready.wait()

        def _tearDown(self):
            self.__tearDown()
            self.done.wait()

            if self.queue.qsize():
                exc = self.queue.get()
                raise exc

        def clientRun(self, test_func):
            self.server_ready.wait()
            self.clientSetUp()
            self.client_ready.set()
            if self.server_crashed:
                self.clientTearDown()
                return
            if not hasattr(test_func, '__call__'):
                raise TypeError("test_func must be a callable function")
            try:
                try:
                    test_func()
                except BaseException as e:
                    self.queue.put(e)
            finally:
                self.clientTearDown()

        def clientSetUp(self):
            raise NotImplementedError("clientSetUp must be implemented.")

        def clientTearDown(self):
            self.done.set()
            thread.exit()

    class SocketTCPTest(unittest.TestCase):

        def setUp(self):
            self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.port = bind_port(self.serv)
            self.serv.listen(1)

        def tearDown(self):
            self.serv.close()
            self.serv = None

    class ThreadedTCPSocketTest(SocketTCPTest, ThreadableTest):

        def __init__(self, methodName='runTest'):
            SocketTCPTest.__init__(self, methodName=methodName)
            ThreadableTest.__init__(self)

        def clientSetUp(self):
            self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def clientTearDown(self):
            self.cli.close()
            self.cli = None
            ThreadableTest.clientTearDown(self)

    class SendfileUsingSendTest(ThreadedTCPSocketTest):
        """
        Test the send() implementation of socket.sendfile().
        """

        FILESIZE = (10 * 1024 * 1024)  # 10MB
        BUFSIZE = 8192
        FILEDATA = ""
        TIMEOUT = 2

        @classmethod
        def setUpClass(cls):
            def chunks(total, step):
                assert total >= step
                while total > step:
                    yield step
                    total -= step
                if total:
                    yield total

            chunk = "".join([random.choice(string.ascii_letters).encode()
                             for i in range(cls.BUFSIZE)])
            with open(TESTFN, 'wb') as f:
                for csize in chunks(cls.FILESIZE, cls.BUFSIZE):
                    f.write(chunk)
            with open(TESTFN, 'rb') as f:
                cls.FILEDATA = f.read()
                assert len(cls.FILEDATA) == cls.FILESIZE

        @classmethod
        def tearDownClass(cls):
            unlink(TESTFN)

        def accept_conn(self):
            self.serv.settimeout(self.TIMEOUT)
            conn, addr = self.serv.accept()
            conn.settimeout(self.TIMEOUT)
            self.addCleanup(conn.close)
            return conn

        def recv_data(self, conn):
            received = []
            while True:
                chunk = conn.recv(self.BUFSIZE)
                if not chunk:
                    break
                received.append(chunk)
            return b''.join(received)

        def meth_from_sock(self, sock):
            # Depending on the mixin class being run return either send()
            # or sendfile() method implementation.
            #return getattr(sock, "_sendfile_use_send")
            return _sendfile_use_send

        # regular file

        def _testRegularFile(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address) as sock:
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file)
                    self.assertEqual(sent, self.FILESIZE)
                    self.assertEqual(file.tell(), self.FILESIZE)

        def testRegularFile(self):
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), self.FILESIZE)
            self.assertEqual(data, self.FILEDATA)

        # non regular file

        def _testNonRegularFile(self):
            address = self.serv.getsockname()
            file = io.BytesIO(self.FILEDATA)
            with create_connection(address) as sock:
                sent = sendfile(sock, file)
                self.assertEqual(sent, self.FILESIZE)
                self.assertEqual(file.tell(), self.FILESIZE)
                self.assertRaises(_GiveupOnSendfile,
                                  _sendfile_use_sendfile, sock, file)

        def testNonRegularFile(self):
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), self.FILESIZE)
            self.assertEqual(data, self.FILEDATA)

        # empty file

        def _testEmptyFileSend(self):
            address = self.serv.getsockname()
            filename = TESTFN + "2"
            with open(filename, 'wb'):
                self.addCleanup(unlink, filename)
            with open(filename, 'rb') as file:
                with create_connection(address) as sock:
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file)
                    self.assertEqual(sent, 0)
                    self.assertEqual(file.tell(), 0)

        def testEmptyFileSend(self):
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(data, b"")

        # offset

        def _testOffset(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address) as sock:
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file, offset=5000)
                    self.assertEqual(sent, self.FILESIZE - 5000)
                    self.assertEqual(file.tell(), self.FILESIZE)

        def testOffset(self):
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), self.FILESIZE - 5000)
            self.assertEqual(data, self.FILEDATA[5000:])

        # count

        def _testCount(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address, timeout=2) as sock:
                    count = 5000007
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file, count=count)
                    self.assertEqual(sent, count)
                    self.assertEqual(file.tell(), count)

        def testCount(self):
            count = 5000007
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), count)
            self.assertEqual(data, self.FILEDATA[:count])

        # count small

        def _testCountSmall(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address, timeout=2) as sock:
                    count = 1
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file, count=count)
                    self.assertEqual(sent, count)
                    self.assertEqual(file.tell(), count)

        def testCountSmall(self):
            count = 1
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), count)
            self.assertEqual(data, self.FILEDATA[:count])

        # count + offset

        def _testCountWithOffset(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address, timeout=2) as sock:
                    count = 100007
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file, offset=2007, count=count)
                    self.assertEqual(sent, count)
                    self.assertEqual(file.tell(), count + 2007)

        def testCountWithOffset(self):
            count = 100007
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), count)
            self.assertEqual(data, self.FILEDATA[2007:count+2007])

        # non blocking sockets are not supposed to work

        def _testNonBlocking(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address) as sock:
                    sock.setblocking(False)
                    meth = self.meth_from_sock(sock)
                    self.assertRaises(ValueError, meth, sock, file)
                    self.assertRaises(ValueError, sendfile, sock, file)

        def testNonBlocking(self):
            conn = self.accept_conn()
            if conn.recv(8192):
                self.fail('was not supposed to receive any data')

        # timeout (non-triggered)

        def _testWithTimeout(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address, timeout=2) as sock:
                    meth = self.meth_from_sock(sock)
                    sent = meth(sock, file)
                    self.assertEqual(sent, self.FILESIZE)

        def testWithTimeout(self):
            conn = self.accept_conn()
            data = self.recv_data(conn)
            self.assertEqual(len(data), self.FILESIZE)
            self.assertEqual(data, self.FILEDATA)

        # timeout (triggered)

        def _testWithTimeoutTriggeredSend(self):
            address = self.serv.getsockname()
            with open(TESTFN, 'rb') as file:
                with create_connection(address, timeout=0.01) as sock:
                    meth = self.meth_from_sock(sock)
                    self.assertRaises(socket.timeout, meth, sock, file)

        def testWithTimeoutTriggeredSend(self):
            conn = self.accept_conn()
            conn.recv(88192)

        # errors

        def _test_errors(self):
            pass

        def test_errors(self):
            with open(TESTFN, 'rb') as file:
                s = socket.socket(type=socket.SOCK_DGRAM)
                with contextlib.closing(s):
                    meth = self.meth_from_sock(s)
                    self.assertRaises(ValueError, meth, s, file)
            with open(TESTFN, 'rt') as file:
                s = socket.socket()
                with contextlib.closing(s):
                    meth = self.meth_from_sock(s)
                    self.assertRaises(ValueError, meth, s, file)
            with open(TESTFN, 'rb') as file:
                s = socket.socket()
                with contextlib.closing(s):
                    meth = self.meth_from_sock(s)
                    self.assertRaises(TypeError,
                                      meth, s, file, count='2')
                    self.assertRaises(TypeError,
                                      meth, s, file, count=0.1)
                    self.assertRaises(ValueError,
                                      meth, s, file, count=0)
                    self.assertRaises(ValueError,
                                      meth, s, file, count=-1)

    @unittest.skipUnless(thread, 'Threading required for this test.')
    @unittest.skipUnless(pysendfile is not None,
                         'sendfile() required for this test.')
    class SendfileUsingSendfileTest(SendfileUsingSendTest):
        """
        Test the sendfile() implementation of socket.sendfile().
        """
        def meth_from_sock(self, sock):
            return _sendfile_use_sendfile

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(SendfileUsingSendTest))
    test_suite.addTest(unittest.makeSuite(SendfileUsingSendfileTest))
    unittest.TextTestRunner(verbosity=2).run(test_suite)
