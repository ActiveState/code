import sys
from thread import get_ident

from qt import *

if len( sys.argv ) > 1 :
    from twisted.internet.threadedselectreactor import install
    install()
    
from twisted.internet import reactor
from twisted.spread import pb

PORT = 9991

DELAY         = 1
DOG_DELAY     = 2
RESTART_DELAY = 5

class Pinger:

    def __init__( self, host ):
        self.ping = None
        self.host = host
        self.ball = 0
        self._start()
        
    def _start( self ):
        print 'Waiting for Server...'
        client = pb.PBClientFactory()
        connector = reactor.connectTCP(host='127.0.0.1', port=PORT, factory=client, timeout=30)
        dfr = client.getRootObject()
        dfr.addCallbacks( self._gotRemote, self._remoteFail )
    
    def _gotRemote( self, remote ):
        print 'Got remote...'
        remote.notifyOnDisconnect( self._remoteFail )
        self.remote = remote
        self._ping()

    def _remoteFail( self, _ ):
        if self.ping:
            self.ping.cancel()
            self.ping = None
        self.restart = reactor.callLater( RESTART_DELAY, self._start )

    def _ping( self ):
        self.dog = reactor.callLater( DOG_DELAY, self._start )
        self.ball += 1
        print 'THROW', self.ball,
        dfr = self.remote.callRemote( 'Pong', self.ball )
        dfr.addCallbacks( self._pong, self._remoteFail )
            
    def _pong( self, ball ):
        self.dog.cancel()
        print 'CATCH',  ball
        self.ball = ball
        self.ping = reactor.callLater( DELAY, self._ping )

class Ponger( pb.Root ):

    def remote_Pong( self, ball ):
        print 'CATCH', ball,
        ball += 1
        print 'THROW', ball
        return ball

class BaseQObject(QObject):

    MAIN_THREAD_ID = 0
    
    def __init__(self):
        QObject.__init__(self)
        self.installEventFilter(self)
        self.event = None

    def eventFilter(self,obj,event):
        # FIXME:  This is a workaround for an unexplained bug
        # The events were getting posted through postEVentWithCallback()
        # But the event() method wasn't getting called.  But the eventFilter()
        # method is getting called.  
        if event.type()==QEvent.User:
            cb = event.__dict__.get('callback')
            if cb: self._doEvent(event)
            return False
        return QObject.eventFilter(self,obj,event)

    def _doEvent(self,event):
        cb = event.__dict__.get('callback')
        if not cb: return
        data = event.__dict__.get('data')
        if data or type(data)==type(False): cb(data)
        else: cb()
        del event

    def event(self, event):
        if event.type()==QEvent.User:
            self._doEvent(event)
            return True
        return QObject.event(self, event)

    def postEventWithCallback(self, callback, data=None):
        # if we're in main thread, just fire off callback
        if get_ident()==BaseQObject.MAIN_THREAD_ID:
            if data or type(data)==type(False): callback(data)
            else: callback()
        # send callback to main thread 
        else:
            event = QEvent(QEvent.User)
            event.callback = callback
            if data or type(data)==type(False): event.data = data
            qApp.postEvent(self, event)
            
class Interleaver(BaseQObject):
    def __init__(self):
        BaseQObject.__init__(self)

    def toInterleave(self, func, *args, **kwargs):
        #print('toInterleave(): %s'%(str(func)))
        self.postEventWithCallback(func)

if len( sys.argv ) > 1 :
    Pinger( sys.argv[1] )
    ii = Interleaver()
    reactor.interleave(ii.toInterleave)
    app = QApplication([])
    app.exec_loop()
else:
    reactor.listenTCP( PORT, pb.PBServerFactory( Ponger()))
    reactor.run()
