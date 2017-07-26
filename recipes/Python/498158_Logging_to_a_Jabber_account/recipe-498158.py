import xmpp # Jabber client/server lib from http://pyxmpp.jajcus.net/

class JabberHandler(logging.Handler):
    """
    A handler class which sends a Jabber message for each logging event.
    """
    def __init__(self, from_id, passwd, to_id):
        logging.Handler.__init__(self)
        
        self.from_id, self.passwd = from_id, passwd
        self.to_id = to_id
        jid=xmpp.JID(self.from_id)
        self.user, self.server = jid.getNode(), jid.getDomain()
    
        conn=xmpp.Client(self.server)#,debug=[])
        conres=conn.connect()
        
        if not conres:
            print "Unable to connect to server %s!"%self.server
            sys.exit(1)
        if conres<>'tls':
            print "Warning: unable to estabilish secure connection - TLS failed!"
        authres=conn.auth(self.user, self.passwd)
        if not authres:
            print "Unable to authorize on %s - check login/password."%self.server
            sys.exit(1)
        if authres<>'sasl':
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%self.server
        conn.sendInitPresence()
        self.conn = conn

    def emit(self, record):
        try:
            msg = self.format(record)
            self.conn.send(xmpp.Message(to=self.to_id,body=msg, frm="Logger"))
        except:
            self.handleError(record)

if __name__=="__main__":
    log = logging.getLogger("URGENT")
    log.setLevel(logging.ERROR)
    log.addHandler(JabberHandler("myID@jabber.org", "mypasswd", "myID@jabber.org"))
    log.error("Serious error because of ...")
