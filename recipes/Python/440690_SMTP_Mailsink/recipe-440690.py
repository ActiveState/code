# SmtpMailsink Copyright 2005 Aviarc Corporation
# Written by Adam Feuer, Matt Branthwaite, and Troy Frever

import sys, asyncore, threading, socket, smtpd, time, StringIO

class SmtpMailsinkServer(smtpd.SMTPServer):
    __version__ = 'Python SMTP Mail Sink version 0.1'

    def __init__( self, *args, **kwargs):
        smtpd.SMTPServer.__init__( self, *args, **kwargs )
        self.mailboxFile = None

    def setMailsinkFile( self, mailboxFile ):
        self.mailboxFile = mailboxFile
        
    def process_message(self, peer, mailfrom, rcpttos, data):
        if self.mailboxFile is not None:
            self.mailboxFile.write( "From %s\n" % mailfrom )
            self.mailboxFile.write( data )
            self.mailboxFile.write( "\n\n" )
            self.mailboxFile.flush()

class SmtpMailsink( threading.Thread ):
    TIME_TO_WAIT_BETWEEN_CHECKS_TO_STOP_SERVING = 0.001

    def __init__( self, host = "localhost", port = 8025, mailboxFile = None, threadName = None ):   
        self.throwExceptionIfAddressIsInUse( host, port )
        self.initializeThread( threadName )
        self.initializeSmtpMailsinkServer( host, port, mailboxFile )

    def throwExceptionIfAddressIsInUse( self, host, port ):
        testSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        testSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,
                               testSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
        testSocket.bind( ( host, port ) )
        testSocket.close()

    def initializeThread( self, threadName ):
        self._stopevent = threading.Event()
        self.threadName = threadName
        if self.threadName is None:
            self.threadName = SmtpMailsink.__class__
        threading.Thread.__init__( self, name = self.threadName )
        
    def initializeSmtpMailsinkServer( self, host, port, mailboxFile ):
        self.smtpMailsinkServer = SmtpMailsinkServer( ( host, port ), None )
        self.resetMailbox( mailboxFile )
        smtpd.__version__ = SmtpMailsinkServer.__version__ 
                
    def resetMailbox( self, mailboxFile = None ):
        self.mailboxFile = mailboxFile
        if self.mailboxFile is None:
            self.mailboxFile = StringIO.StringIO()
        self.smtpMailsinkServer.setMailsinkFile( self.mailboxFile )

    def getMailboxContents( self ):
        return self.mailboxFile.getvalue()
    
    def getMailboxFile( self ):
        return self.mailboxFile
    
    def run( self ):
        while not self._stopevent.isSet():
            asyncore.loop( timeout = SmtpMailsink.TIME_TO_WAIT_BETWEEN_CHECKS_TO_STOP_SERVING, count = 1 )

    def stop( self, timeout=None ):
        self._stopevent.set()
        threading.Thread.join( self, timeout )
        self.smtpMailsinkServer.close()
        
if __name__ == "__main__":
    if len( sys.argv ) < 2 or len( sys.argv ) > 3:
        print "Usage: python SmtpMailsink.py mailsinkfile [hostname]"
        sys.exit( 1 )
    mailfile = sys.argv[1]
    hostname = "localhost"
    if len( sys.argv ) > 2:
        hostname = sys.argv[ 2 ]
    fileobject = open( mailfile, "w" )
    smtpMailsink = SmtpMailsink( host = hostname, mailboxFile = fileobject )
    smtpMailsink.start()
    while True:

        time.sleep( 1 )
