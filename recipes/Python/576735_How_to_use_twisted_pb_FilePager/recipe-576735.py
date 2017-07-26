from twisted.spread.util import FilePager
from twisted.spread.flavors import Referenceable
from twisted.internet.defer import Deferred
import os

PATH = r"C:\temp\very_large_file.exe"

### Server Side

class ResultsPager(FilePager):
    def __init__(self, collector, path):
        self._deferred = Deferred()
        print "%s, %d bytes" % (path, os.path.getsize(path))
        fd = file(path, 'rb')
        FilePager.__init__(self, collector, fd, callback=self.done)

    def done(self):
        print "The entire file has been transferred."
        self._deferred.callback(self.collector)

    def wait(self):
        return self._deferred

class FilePagerizer(Referenceable):
    def remote_getFile(self, collector, path):
        pager = ResultsPager(collector, path)
        return pager.wait()

### Client Side

class SimplePageCollector(Referenceable):
    def __init__(self):
        self.pages = []
    def remote_gotPage(self, page):
        self.pages.append(page)
        print "gotPage (%d bytes)" % len(page)
        
    def remote_endedPaging(self):
        print 'endedPaging'

class FilerGetter:
    def __init__(self, p):
        self._file_pagerizer = p

    def getRemoteFile(self, path):        
        root, ext = os.path.splitext(os.path.basename(path))
        local_path = root + '-new' + ext
        return self._file_pagerizer.callRemote(
            "getFile",
            SimplePageCollector(), path).addCallback(self._finished, local_path)

    def _finished(self, collector, path):        
        data = ''.join(collector.pages)
        with file(path, 'wb') as f:
            f.write(data)        
            print "write to %s, %d bytes" % (path, len(data))

if __name__ == '__main__':
    import sys
    from twisted.internet import reactor
    from twisted.python import log
    log.startLogging(sys.stdout)
    PORTNO = 8123
    if sys.argv[1] == 'server':
        from twisted.spread.flavors import Root
        from twisted.spread.pb import PBServerFactory 
        class SimpleRoot(Root):
            def rootObject(self, broker):
                return FilePagerizer()
        reactor.listenTCP(PORTNO, PBServerFactory(SimpleRoot()))
        
    elif sys.argv[1] == 'client':
        
        from twisted.spread import pb        
        def getFile1(x, path):
            r = FilerGetter(x)
            return r.getRemoteFile(path)
            
        from twisted.spread import util            
        def getFile2(x, path):            
            def finished(pages):
                data = ''.join(pages)           
                root, ext = os.path.splitext(os.path.basename(path))
                local_path = root + '-new' + ext     
                f = file(local_path, 'wb')        
                f.write(data)                
                print "%d bytes written to %s" % (len(data), local_path)
                
            util.getAllPages(x, "getFile", path).addCallback(finished)
        
        cf = pb.PBClientFactory()
        reactor.connectTCP("localhost", PORTNO, cf)
        cf.getRootObject().addCallback(getFile2, PATH)        
    else:
        raise sys.exit("usage: %s (server|client)" % sys.argv[0])
    reactor.run()
