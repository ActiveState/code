import socket
import errno
from time import time as now


def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """

    s = socket.socket()
    # time module is needed to calc timeout shared between two exceptions
    end = timeout and now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        except socket.timeout, err:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error, err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if type(err.args) != tuple or err[0] not in (errno.ETIMEDOUT, errno.ECONNREFUSED):
                raise
        else:
            s.close()
            return True
