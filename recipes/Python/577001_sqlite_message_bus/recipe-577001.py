#!/usr/bin/python

"""Simple message bus implemented on top of a shared sqlite3 database.

We use a single, shared table for messages. Each message has a unique,
incrementing id. When a program connects to the message bus, it reads the
highest id that's in the table - after that it'll "receive" messages that's been
sent after it started.

Each user has a name and messages can be addressed using standard glob notation
to "broadcast" messages. I.e there can be a client1, client2, client3 and then a
message can be addressed to "client*".

Note that each send/recv will hit the database, so it's prudent to only to so at
intervals, e.g if waiting for a response to a message there should be a
microsleep in between calls to recv().
"""

# standard
import cPickle
import fnmatch
import time



# mostly here for documentation purposes, not used in code.
CREATE_TABLE  = ('create table if not exists mbus (id integer primary key '
                 'autoincrement, source, dest, data blob)')

# read all messages higher than the specified id
RECV_MESSAGES = 'select * from mbus where id > ? order by id asc'

SEND_MESSAGE  = 'insert into mbus values (NULL, ?, ?, ?)'

# used at startup to find 
FIND_LAST_ID  = 'select max(id) from mbus'



    
class MBus:

    def __init__ (self, db, name):
        self.db    = db
        self.name  = name
        self.seen  = self._find_last_id()
        self.mbox  = []

    # PRIVATE
    def _find_last_id (self):
        return self.db.execute(FIND_LAST_ID, ()).fetchone()[0] or 1

    def _poll (self):
        """Fetch new messages from database and append to mailbox.
        """
        for row in list(self.db.execute(RECV_MESSAGES, (self.seen,))):
            self.seen, source, dest, blob = row
            if source != self.name and fnmatch.fnmatch(self.name, dest):
                tag, data = cPickle.loads(str(blob))
                self.mbox.append((self.seen, source, tag, data))

    def _filter (self, tag, func):
        """Remove and return matching messages from mailbox and retain the rest.
        """
        mbox = []
        for t in self.mbox:
            if fnmatch.fnmatch(t[2], tag) and func(t):
                yield t
            else:
                mbox.append(t)
        self.mbox = mbox

    # PUBLIC
    def recv (self, tag='*', func=lambda _: True, wait=5, sleep=0.5):
        end = time.time() + wait
        while True:
            self._poll()
            for t in self._filter(tag, func):
                yield t
            if time.time() > end:
                break
            time.sleep(sleep)

    def send (self, dest, tag, **kwargs):
        data  = (tag, kwargs)
        rowid = self.db.execute(SEND_MESSAGE, (self.name, dest,
                                               cPickle.dumps(data))).lastrowid
        return rowid
    


# PBULIC API    

def connect (db, name):
    """Create a MBus and populate module environment with it's global methods.

    The common case is that we connect to only one message bus. To avoid passing
    around a message bus object we can instead simply do:

    import mbus

    mbus.connect(db, 'client')
    mbus.send('*', 'ping')
    for rowid, source, tag, data in mbus.recv(tag='pong'):
        pass
    """
    g = globals()
    m = MBus(db, name)
    g['send'] = m.send
    g['recv'] = m.recv



# TESTING
    
if __name__ == '__main__':
    import os
    import sys
    import sqlite3

    p  = 'test.db'
    c  = not os.path.exists(p)
    db = sqlite3.connect(p, isolation_level=None)
    if c:
        db.execute(CREATE_TABLE)

    if sys.argv[1] == 'server':
        mb = MBus(db, 'server')
        while True:
            for _, source, _, data in mb.recv(tag='ping'):
                mb.send(source, 'pong', pid=os.getpid())
                sys.exit(0)
    else:
        mb = MBus(db, 'client')
        mb.send('server', 'ping')
        for _, source, _, data in mb.recv(tag='pong'):
            print 'received pong from pid', data['pid']
