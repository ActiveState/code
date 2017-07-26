#! /usr/bin/env python
"""Provide simple support for Java-style servlets.

The code in this module provides an incomplete port of Java's API for
servlets. Only essential classes and methods are implemented here."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

import urllib.parse
import socketserver
import http.server
import webbrowser
import socket
import cgitb
import cgi
import sys
import io

################################################################################

class HttpServlet(http.server.BaseHTTPRequestHandler):

    """Provide a base class for implementing a servlet.

    The HttpServlet class should be inherited by any class that is to be
    run as a servlet. A few basic HTTP methods are automatically handled
    by this class and passed on to the service method to be written by
    the servlet designer. Request and response systems are handled here."""

    # These variables properly identify and setup the handler.
    server_version = 'HttpServlet/' + http.server.__version__
    protocol_version = 'HTTP/1.1'

    __debug = False # Determines how exceptions are reported.
    
    @classmethod
    def debug(cls, value):
        """Set the debugging status of servlet applications.

        This determines what happens when code raises an exception.
        if True: traceback is sent back to the browser for analysis.
        if False: the browser receives an ambiguous 500 error code."""
        cls.__debug = value

    def do_GET(self):
        """Handle the GET method sent via HTTP."""
        if self.path == '/favicon.ico':
            self.send_error(404)
            return
        self.__call_service(self.path)

    def do_POST(self):
        """Handle the POST method sent via HTTP."""
        try:
            length = int(self.headers.get('content-length'))
        except:
            self.send_error(411)
        else:
            self.__call_service('?' + self.rfile.read(length).decode())

    def __call_service(self, query):
        """Execute service method implemented by child class.

        When either a GET or POST request is received, this method is
        called with a string representing the query. Request and response
        objects are created for the child's service method, and an answer
        is sent back to the client with errors automatically being caught."""
        request = _HttpServletRequest(query)
        response = _HttpServletResponse()
        try:
            self.service(request, response)
        except Exception:
            if self.__debug:
                self.send_response(500)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Connection', 'close')
                self.end_headers()
                klass, value, trace = sys.exc_info()
                # The next function call may raise an exception.
                html = cgitb.html((klass, value, trace.tb_next))
                self.wfile.write(html.encode())
            else:
                self.send_error(500)
        else:
            response_value = response._value
            self.send_response(200)
            self.send_header('Content-Type', response._type)
            self.send_header('Content-Length', str(len(response_value)))
            self.end_headers()
            self.wfile.write(response_value)
            
    def service(self, request, response):
        """Process the client's request and send back a response."""
        raise NotImplementedError()

################################################################################

class _HttpServletRequest:

    """Store the query from the client's request.

    Instances of this class are automatically created
    to store query variables obtained by parsing the
    path or post data sent from the client to the servlet."""

    def __init__(self, path):
        """Initialize the request object from the path."""
        query = urllib.parse.urlparse(path).query
        self.__dict = urllib.parse.parse_qs(query, True)

    def getParameter(self, name):
        """Compute the value of the named parameter.

        The parameter that has the specified name is found,
        and the first value associated with that name is
        returned. If the name cannot be found, then None
        is returned to the caller instead of an exception."""
        return self.__dict.get(name, [None])[0]

################################################################################

class _HttpServletResponse:

    """Allow servlet to send response to client.

    Servlet child classes have their service methods called with an
    instance of this class. It allows the responses to be configured
    for both the type of data and the content of the data being sent."""

    def __init__(self):
        """Initialize a blank, generic response object."""
        self.__content_type = 'text/plain'
        self.__print_writer = _PrintWriter()

    def setContentType(self, content_type):
        """Set the type of data being sent to client.

        This is the argument to the "Content-Type" header sent to
        the client. By default, it is set to "text/plain" but may
        be set to whatever is appropriate for the data type being
        sent. Note the data alterations in the _value property."""
        self.__content_type = content_type

    def getWriter(self):
        """Produce a writer object for printing.

        This method returns a PrintWriter object that caches the
        servlet's response to the client. Once the service method
        returns, the PrintWriter's value is sent back to the client."""
        return self.__print_writer

    @property
    def _type(self):
        """Read-only content-type property for __call_service."""
        return self.__content_type

    @property
    def _value(self):
        """Read-only response-value property for __call_service."""
        value = self.__print_writer.getvalue()
        lines = value.replace('\r\n', '\n').replace('\r', '\n')
        return lines.replace('\n', '\r\n').encode()

################################################################################

class _PrintWriter(io.StringIO):

    """Cache the response generated for the client.

    An instance of the class is automatically built by HTTP Servlet
    Response objects to cache the data being sent back to the client."""

    print = io.StringIO.write

    def println(self, string):
        """Print a line of data to the internal representation."""
        self.write(string + '\r\n')

################################################################################

class HttpServer(socketserver.ThreadingMixIn, http.server.HTTPServer):

    """Create a server with specified address and handler.

    A generic web server can be instantiated with this class. It will listen
    on the address given to its constructor and will use the handler class
    to process all incoming traffic. Running a server is greatly simplified."""

    # We should not be binding to an
    # address that is already in use.
    allow_reuse_address = False

    @classmethod
    def main(cls, RequestHandlerClass, port=80):
        """Start server with handler on given port.

        This static method provides an easy way to start, run, and exit
        a HttpServer instance. The server will be executed if possible,
        and the computer's web browser will be directed to the address."""
        try:
            server = cls(('', port), RequestHandlerClass)
            active = True
        except socket.error:
            active = False
        else:
            addr, port = server.socket.getsockname()
            print('Serving HTTP on', addr, 'port', port, '...')
        finally:
            port = '' if port == 80 else ':' + str(port)
            addr = 'http://localhost' + port + '/'
            webbrowser.open(addr)
        if active:
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print('Keyboard interrupt received: EXITING')
            finally:
                server.server_close()

    def handle_error(self, request, client_address):
        """Process exceptions raised by the RequestHandlerClass.

        Overriding this method is necessary for two different reasons:
        (1) SystemExit exceptions are incorrectly caught otherwise and
        (2) Socket errors should be silently passed in the server code"""
        klass, value = sys.exc_info()[:2]
        if klass is SystemExit:
            self.__exit = value
            self._BaseServer__serving = None
        elif issubclass(klass, socket.error):
            pass
        else:
            super().handle_error(request, client_address)

    def serve_forever(self, poll_interval=0.5):
        """Handle all incoming client requests forever.

        This method has been overridden so that SystemExit exceptions
        raised in the RequestHandlerClass can be re-raised after being
        caught in the handle_error method above. This allows servlet
        code to terminate server execution if so desired or required."""
        super().serve_forever(poll_interval)
        if self._BaseServer__serving is None:
            raise self.__exit
