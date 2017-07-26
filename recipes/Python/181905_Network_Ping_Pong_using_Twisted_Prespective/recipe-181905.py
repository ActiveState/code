from twisted.spread import pb
from twisted.internet import reactor
        
import sys

PORT = 8992

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
        dfr = pb.getObjectAt( self.host, PORT, 30 )
        dfr.addCallbacks( self._gotRemote, self._remoteFail )
    
    def _gotRemote( self, remote ):
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

if len( sys.argv ) > 1 :
    Pinger( sys.argv[1] )
else:
    reactor.listenTCP( PORT, pb.BrokerFactory( Ponger()))

reactor.run()
