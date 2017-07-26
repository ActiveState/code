from twisted.spread.util import StringPager
from twisted.spread.flavors import Referenceable
from twisted.internet.defer import Deferred

### Server Side

class ResultsPager(StringPager):
    def __init__(self, collector, string, firstPage):
        self._atFirstPage = True
        self._firstPage = firstPage
        self._deferred = Deferred()
        StringPager.__init__(self, collector, string, callback=self.done)

    def nextPage(self):
        if self._atFirstPage:
            self._atFirstPage = False
            return self._firstPage
        else:
            return StringPager.nextPage(self)

    def done(self):
        self._deferred.callback(self.collector)

    def wait(self):
        return self._deferred

class DatabaseThingy(Referenceable):
    def remote_getResult(self, collector, phrase):
        st = phrase * 1024 * 1024
        lp = 1, 2, phrase * 2
        pager = ResultsPager(collector, st, lp)
        return pager.wait()

### Client Side

class SimplePageCollector(Referenceable):
    def __init__(self):
        self.pages = []
    def remote_gotPage(self, page):
        self.pages.append(page)
    def remote_endedPaging(self):
        print 'paging ended'

class ResultGetter:
    def __init__(self, dt):
        self.dataThingy = dt

    def getRemoteResult(self):
        return self.dataThingy.callRemote(
            "getResult",
            SimplePageCollector(),
            "hello world ").addCallback(self._massage
                                        ).addCallbacks(self.ok, self.nok)
    
    def _massage(self, collector):
        pages = collector.pages
        bigstr = ''.join(pages[1:])
        return tuple(pages[0])+ (bigstr,)

        return collector.args()

    def ok(self, (int1, int2, shortString, hugeString)):
        print 'data ok'
        print int1, int2, repr(shortString), len(hugeString)

    def nok(self, f):
        print 'data not ok'
        return f

if __name__ == '__main__':
    import sys
    from twisted.internet import reactor
    from twisted.python import log
    log.startLogging(sys.stdout)
    PORTNO = 8123
    if sys.argv[1] == 'server':
        from twisted.spread.flavors import Root
        from twisted.spread.pb import BrokerFactory
        class SimpleRoot(Root):
            def rootObject(self, broker):
                return DatabaseThingy()
        reactor.listenTCP(PORTNO, BrokerFactory(SimpleRoot()))
    elif sys.argv[1] == 'client':
        from twisted.spread.pb import getObjectAt
        def getIt(x):
            r = ResultGetter(x)
            return r.getRemoteResult()
        getObjectAt("localhost", PORTNO).addCallback(getIt)
    else:
        raise sys.exit("usage: %s (server|client)" % sys.argv[0])
    reactor.run()
