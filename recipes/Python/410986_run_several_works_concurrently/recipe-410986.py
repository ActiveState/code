from __future__ import nested_scopes

from zope.interface import Interface, Attribute
from twisted.internet import defer


class IWorker(Interface):
    """A worker is an object that can do some 'work' and return
    its result in a deferred.
    """

    deferred = Attribute("""A Deferred that is fired at work completion""")

    def startWork():
        """Start the work.
        """


def spawnDeferredWorkers(workerList, n):
    """Run several works concurrently.

    workerList is a list of objects that satisfies the IWorker interface.
    n specifies how many works to run concurrently.
    
    Return a list of Deferred objects, which will fire with the result of each work.
    """

    def callback(result):
        # start the next work
        try:
            worker = workerIterator.next()
            worker.startWork()
        except StopIteration:
            pass
        
        return result
        
    def errback(reason):
        # ignore the error and start the next work
        try:
            worker = workerIterator.next()
            worker.startWork()
        except StopIteration:
            pass
        
        return reason

    
    deferredList = []
    for worker in workerList:
        deferred = worker.deferred
        deferred.addCallback(callback).addErrback(errback)
           
        deferredList.append(deferred)
    
    workerIterator = iter(workerList)
    
    # begin the first n works
    for i in range(n):
        try:
            worker = workerIterator.next()
            worker.startWork()
        except StopIteration:
            pass

    return deferredList


def getRFC(n = 10, m = 3):
    """An example of spawnDeferredWorkers for getting a list a RFC.
    
    n specifies how many RFC (starting from 1) to download.
    m specifies how many downloads to run concurrently.
    """
    
    from zope.interface import implements
    from twisted.web import client
    from twisted.internet import reactor
    
    import time

    
    class HTTPClientWorker(client.HTTPDownloader):
        """
        Adaptation of client.HTTPDownloader to IWorker interface
        """
        implements(IWorker)

        def __init__(self, *args, **kwargs):
            client.HTTPDownloader.__init__(self, *args, **kwargs)

        def startWork(self):
            print "starting downloading %s..." % self.url
            reactor.connectTCP(self.host, self.port, self)


    # callback functions
    def gotPageList(result):
        pages = len(result)
        errors = len(filter(lambda item: not item[0], result))
        print "\n\ngot %d pages with %d errors" % (pages, errors)
        
        end = time.clock()
        print "%d secs elapsed" % (end - start)
        
        reactor.stop()

    def savePage(page, worker):
        print "got %s" % worker.url

    def error(reason, worker):
        print "failed to download %s" % worker.url
        print reason.value.__class__, reason.value
        
        return reason


    workerList = [HTTPClientWorker("http://www.ietf.org/rfc/rfc%d.txt" % rfc,
                                   "rfc%d.txt" % rfc)
                  for rfc in range(1, n + 1)]

    deferredList = spawnDeferredWorkers(workerList, m)
    for deferred, worker in zip(deferredList, workerList):
        deferred.addCallback(savePage, worker).addErrback(error, worker)

    deferred = defer.DeferredList(deferredList, consumeErrors = True)
    deferred.addCallback(gotPageList)

    start = time.clock()

    reactor.run()


if __name__ == "__main__":
    import sys
    
    getRFC(int(sys.argv[1]), int(sys.argv[2]))
