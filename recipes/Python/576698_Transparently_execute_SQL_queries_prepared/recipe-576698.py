'''
Transparent use of prepared statements with Postgresql.

Usage example with psycgopg2: We create a cursor that provides
both with dict-like field access and prepared statements.

from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from this_recipe import PrepCursorMixin

class Cursor(PrepCursorMixin, RealDictCursor):
    pass 


class Connection(_connection):
    def cursor(self):
        return super(Connection, self).cursor(cursor_factory=Cursor)


def connect(*a, **kw):
    return Connection(*a, **kw)
'''

import re

class PrepCursorMixin(object):
    '''
    mix in with dbapi cursor class
    
    formatRe fishes out all format specifiers for a given paramstyle
    this one works with paramstyles 'format' or 'pyformat'
    '''
    formatRe = re.compile('(\%s|\%\([\w\.]+\)s)', re.DOTALL)

    def __init__(self, *a, **kw):
        super(PrepCursorMixin, self).__init__(*a, **kw)

        # preferably store prepd statements on connection
        conn = getattr(self, 'connection', None)
        if conn:
            pc = getattr(conn, 'prepCache', {})
            self.prepCache = self.connection.prepCache = pc
        else:    
            self.prepCache = {}

    def executeps(self, cmd, args=None):
        '''
        execute a command using a prepared statement.
        '''
        prepStmt = self.prepCache.get(cmd)
        if prepStmt is None:
            cmdId = "ps_%d" % (len(self.prepCache) + 1)  
            # unique name for new prepared statement
            prepStmt = self.prepCache[cmd] = \
                       self.prepareStatement(cmd, cmdId)

        self.execute(prepStmt, args)

    def prepareStatement(self, cmd, cmdId):
        '''
        translate a sql command into its corresponding 
        prepared statement, and execute the declaration.
        '''
        specifiers = []

        def replaceSpec(mo):
            specifiers.append(mo.group())
            return '$%d' % len(specifiers)

        replacedCmd = self.formatRe.sub(replaceSpec, cmd)
        prepCmd = 'prepare %s as %s' % (cmdId, replacedCmd)

        if len(specifiers) == 0:    # no variable arguments
            execCmd = 'execute %s' % cmdId

        else:       # set up argument slots in prep statement
            execCmd = 'execute %s(%s)' % (cmdId, ', '.join(specifiers))

        self.execute(prepCmd)
        return execCmd

    def executemanyps(self, cmd, seq_of_parameters):
        '''
        prepared statement version of executemany.
        '''
        for p in seq_of_parameters:
            self.executeps(cmd, p)

        # Don't want to leave the value of the last execute() call
        try:
            self.rowcount = -1 
        except TypeError:   # fooks with psycopg
            pass


if __name__ == '__main__':
    '''
    just demonstrate the string mangling that goes on
    '''

    class DummyBaseCursor(object):
        def __init__(self, conn):
            self.connection = conn

        def execute(self, cmd, args=None):
            print 'execute'
            print 'cmd:', cmd
            print 'args:', args
            print '-' * 20

    class DummyCursor(PrepCursorMixin, DummyBaseCursor):
        def executeps(self, cmd, args):
            print 'executeps'
            print 'cmd:', cmd
            print 'args:', args
            super(DummyCursor, self).executeps(cmd, args)

    class DummyConnection(object): pass

    dc = DummyCursor(DummyConnection)

    sql = \
       ['''
        select * from dummies
        where name=%s
        and surname=%s
        ''',
        '''
        select * from dummies
        where name=%(name)s
        and surname=%(surname)s
        ''',
        'select * from dummies']

    theargs = [('Joe','Blow'), {'name':'Joe', 'surname':'Blow'}, None]

    for x in range(3):
        for y in range(2):
            dc.executeps(sql[x], theargs[x])
