#-*- coding: utf-8 -*-

import socket
import ssl
import httplib

class HTTPSClientAuthConnection(httplib.HTTPSConnection):
    """ Class to make a HTTPS connection, with support for full client-based SSL Authentication"""

    def __init__(self, host, port, key_file, cert_file, ca_file, timeout=None):
        httplib.HTTPSConnection.__init__(self, host, key_file=key_file, cert_file=cert_file)
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_file = ca_file
        self.timeout = timeout

    def connect(self):
        """ Connect to a host on a given (SSL) port.
            If ca_file is pointing somewhere, use it to check Server Certificate.

            Redefined/copied and extended from httplib.py:1105 (Python 2.6.x).
            This is needed to pass cert_reqs=ssl.CERT_REQUIRED as parameter to ssl.wrap_socket(),
            which forces SSL to check server certificate against our client certificate.
        """
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        # If there's no CA File, don't force Server Certificate Check
        if self.ca_file:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ca_certs=self.ca_file, cert_reqs=ssl.CERT_REQUIRED)
        else:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, cert_reqs=ssl.CERT_NONE)

if __name__ == '__main__':
    # Little test-case of our class
    import sys
    if len(sys.argv) != 6:
        print 'usage: python https_auth_handler.py host port key_file cert_file ca_file'
        sys.exit(1)
    else:
        host, port, key_file, cert_file, ca_file = sys.argv[1:]
    conn = HTTPSClientAuthConnection(host, port, key_file=key_file, cert_file=cert_file, ca_file=ca_file)
    conn.request('GET', '/')
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
