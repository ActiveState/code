from BaseHTTPServer import *
from cherrypy._cphttpserver import CherryHTTPServer
from contrib.quixote.server.simple_server import HTTPRequestHandler
from threading import Thread,Event

class HTTPServerPlus(CherryHTTPServer, Thread):
    
    def __init__(self, **kwargs):
        CherryHTTPServer.__init__(self,**kwargs)
        Thread.__init__(self)

    def run(self):
        self.serve_forever()

    def join(self,timeout=None):
        self.shutdown()
        Thread.join(self, timeout)


from contrib.quixote.publish import Publisher

def create_publisher():
    from quixote.demo.root import RootDirectory
    return Publisher(RootDirectory(), display_exceptions='plain')

class TemplateServer(HTTPServerPlus):

    def __init__(self, port):
        HTTPServerPlus.__init__(self,server_address=('', port), RequestHandlerClass=HTTPRequestHandler)
        self.server_port = port
        self.server_name = 'My Local Server'
        create_publisher()
        self.start()


if __name__=='__main__':
    server = TemplateServer(8800)
    try:
        while 1: pass
    except KeyboardInterrupt:
        print 'Got Ctrl-C...'
        server.join(1.0)
