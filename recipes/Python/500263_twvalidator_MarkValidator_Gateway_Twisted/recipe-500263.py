from urlparse import urlparse, urlsplit
from cgi import parse_qs
import cStringIO as StringIO

from twisted.internet import defer
from twisted.web import server, resource, client



def encodeFormData(arg, value):
    """Encode data as a multipart/form-data
    """
 
    BOUNDARY = '----------BOUNDARY'
   
    l = []
    l.append('--' + BOUNDARY)
    l.append('Content-Disposition: form-data; name="%s"' % arg)
    l.append('')
    l.append(value)
    l.append('--' + BOUNDARY + '--')
    l.append('')

    body = '\r\n'.join(l)
    contentType = 'multipart/form-data; boundary=%s' % BOUNDARY

    return body, contentType


class FakeTransport(object):
    def __init__(self):
        self.io = StringIO.StringIO()

    
    def writeSequence(self, sequence):
        self.io.writelines(sequence)

    def write(self, data):
        self.io.write(data)

    def getData(self):
        return self.io.getvalue()


class MarkupValidator(resource.Resource):
    """A simple gateway to a validator service for Twisted Web.
    """

    # Please, install a validator on your server!
    uri = 'http://validator.w3.org/check'
    arg = 'fragment'

    def __init__(self, site):
        """site is the site object of your twisted.web server
        """

        self.site = site


    def render_GET(self, request):
        def finish(data):
            # Write the data back to our client
            request.clientproto = clientproto
            transport.write(data)
            transport.loseConnection()


        # Get the referer and parse it
        referer = request.getHeader('referer')
        scheme, netloc, path, parameters, query, fragment = urlparse(referer)
        args = parse_qs(query)
        
        transport = request.transport
        clientproto = request.clientproto

        # Modify the original request
        request.uri = referer
        request.path = path
        request.args = args
        request.clientproto = 'HTTP/1.0'  # we don't want chunk encoding
        request.transport = FakeTransport()

        # Reload the modified request on the server, without using HTTP
        deferred = request.notifyFinish()
        request.process()

        # XXX TODO handle errors
        deferred.addCallback(lambda _: request.transport.getData()
                             ).addCallback(self.validate, request
                                           ).addCallback(finish)
        
        return server.NOT_DONE_YET

    def validate(self, data, request):
        # We need only the body
        data = data[data.find('\r\n\r\n') + 4:]

        # Build the request for the validator service, using the
        # original request as the base
        headers = request.received_headers
        data, contentType = encodeFormData(self.arg, data)
        
        headers['content-type'] = contentType
        headers.pop('cookie', None)
        headers.pop('referer', None)
        headers.pop('host', None)
        
        return client.getPage(
            self.uri, method='POST', headers=headers, postdata=data 
            )


if __name__ == '__main__':
    """A simple usage example.
    """

    from twisted.web import server
    from twisted.internet import reactor


    class Simple(resource.Resource):
        def render_GET(self, request):
            return """<!DOCTYPE html
  PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" 
      lang="en" xml:lang="en">
  <head>
    <title>twvalidator example</title>
  </head>
  <body>
    <h1>twvalidator example</h1>

    <p><a href="validate">validate</a></p>
  </body>
</html>"""

        def getChild(self, name, request):
            if name == '':
                return self
            return resource.Resource.getChild(
                self, name, request)


    root = Simple()
    site = server.Site(root)

    root.putChild('validate', MarkupValidator(site))

    reactor.listenTCP(8080, site)
    reactor.run()
