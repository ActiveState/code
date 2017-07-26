"""A little Transport layer to maintain the JSESSIONID cookie that
Javaserver pages use to maintain a session.  I'd like to use this
to make xmlrpclib session aware.

Sample usage:

    server = Server("http://foobar.com/baz/servlet/xmlrpc.class")
    print server.get_jsession_id();
    print server.test.sayHello()
    print server.get_jsession_id();
    print server.test.sayGoodbye()
    print server.get_jsession_id();

"""

import xmlrpclib
import Cookie

class JspAuthTransport(xmlrpclib.Transport):
    def __init__(self):
        self.__cookies = Cookie.SmartCookie()

    def request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)

        self.send_request(h, handler, request_body)
        self.__sendJsessionCookie(h)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)

        errcode, errmsg, headers = h.getreply()

        if errcode != 200:
            raise xmlrpclib.ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )
        self.verbose = verbose
        self.__processCookies(headers)
        return self.parse_response(h.getfile())


    def get_jsession_id(self):
        if self.__cookies.has_key('JSESSIONID'):
            return self.__cookies['JSESSIONID'].value
        return None


    def __sendJsessionCookie(self, connection):
        if self.__cookies.has_key('JSESSIONID'):
            connection.putheader('Cookie', '$Version="1"; JSESSIONID=%s'
                                 % self.get_jsession_id())


    def __processCookies(self, headers):
        if headers.getheader('Set-Cookie'):
            self.__cookies.load(headers.getheader('Set-Cookie'))


    def send_content(self, connection, request_body):
        connection.putheader("Content-Type", "text/xml")
        connection.putheader("Content-Length", str(len(request_body)))

        connection.endheaders()
        if request_body:
            connection.send(request_body)


class Server:
    """A little wrapper to keep the transport and serverproxy together."""
    def __init__(self, uri):
        self.transport = JspAuthTransport()
	self.serverproxy = xmlrpclib.ServerProxy(uri, self.transport)

    def __getattr__(self, attr):
        return getattr(self.serverproxy, attr)

    def get_jsession_id(self):
        return self.transport.get_jsession_id()



def _test2():
    server = Server("http://www.oreillynet.com/meerkat/xml-rpc/server.php")
    print server.system.listMethods()


if __name__ == '__main__':
    _test2()
