#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################
##
## sql+
## dB Oracle client
## configuration file .sql+
## author: Jose Soares Da Silva
## date:     11 March 2013
## version:  1.0
#######################################################################
import sys, os, cmd, cx_Oracle, pydoc
from tempfile import mkstemp
_CONN = None
_HIST = []
_FD=None
_OUTPUT=None
LINES=os.getenv('LINES') or 41
COLUMNS=os.getenv('COLUMNS') or 125

try: #cx_Oracle monkeypatch...
    makedsn = cx_Oracle.makedsn
    cx_Oracle.makedsn = lambda *args, **kw: makedsn(*args, **kw).replace('SID','SERVICE_NAME')
except:
    pass

#read configuration file...
config={}
for kk in open('.sql+').readlines():
    if not kk.startswith('#'):
        fv=kk.find('=')
        if fv != -1:
            config[ kk[:fv].strip()] = kk[fv:].strip().strip('=').strip().strip('"')

class Edit(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "%s=> " % config.get('DBURI').split('/')[-1]
    def do_help(self, args):
        """
           help or ? with no arguments prints a list of available commands
           help or ? <command> gives help on <command>
        """
        cmd.Cmd.do_help(self, args)

    def do_db(self, args):
        """change db (user/password)"""
        global _CONN
        _CONN=None
        dburi=config.get('DBURI').split('@')
        config['DBURI']='%s@%s'%(args,dburi[1])
        init_db_conn()

    def do_history(self, args):
        """Print history"""
        print _HIST

    def do_quit(self, args):
        """Exits"""
        sys.exit()
    def do_exit(self, args):
        """Exits"""
        sys.exit()
    def do_shell(self, args):
        """system command; use '!' or the keyword 'shell'"""
        os.system(args)
    def do_edit(self, args):
        """use vim to edit commands"""
        fd, tmpfile = mkstemp()
        os.write(fd, '\n'.join(_HIST[-2:-1]))
        os.close(fd)
        os.system('%s %s' % (config.get('EDITOR'), tmpfile))
        ln = open(tmpfile).read()
        os.unlink(tmpfile)
        tmpfile = ''
        self.lastcmd=ln
        _HIST.append(ln)
        return self.default(ln)
    def do_input(self, args):
        """input from <file>"""
        return 'input '+args.strip(';')
    def do_output(self, args):
        """
           output to <file name>
           enter 'output' without <file name> to close file
        """
        global _FD, _OUTPUT
        if args:
            _OUTPUT = args
            _FD = open(_OUTPUT,'a')
        else:
            _FD.close()
            _FD=_OUTPUT = None
    def do_desc(self, args):
        """desc table name"""
        show_qry(config.get('SQL_DESC')%args.strip(';').upper())
        show_qry(config.get('SQL_LIST_INDEX')%args.strip(';').upper())
    def do_index(self, args):
        """show index info <index name>"""
        show_qry(config.get('SQL_INDEX')%args.strip(';').upper())
    def do_constraints(self, args):
        """show constraints <table name>"""
        show_qry(config.get('SQL_CONSTRAINTS')%args.strip(';').upper())
    def do_foreigns(self, args):
        """show foreign keys <table name>"""
        show_qry(config.get('SQL_FOREIGNS')%args.strip(';').upper())
    def do_set(self, args):
        """settings"""
        show_qry("ALTER SESSION SET %s"%args)
    def do_settings(self, args):
        """show settings"""
        show_qry('select * from nls_session_parameters')
    def do_tables(self, args):
        """list tables"""
        show_qry(config.get('SQL_TABLES'))
    def do_sequences(self, args):
        """list sequences"""
        show_qry(config.get('SQL_SEQUENCES'))
    def do_triggers(self, args):
        """show triggers definition"""
        show_qry(config.get('SQL_TRIGGERS'))
    def precmd(self, line):
        _HIST.append( line.strip() )
        return line
    def default(self, line):
        return line


def input_file(filename):
    o=open(filename)
    sql=''
    for k in o.readlines():
        if not k.strip().startswith('--'):
            for j in k:
                if j == ';':
                    show_qry(sql)
                    sql=''
                else:
                    sql=sql+j

def table(righe):
    d={}
    if righe:
        for j in range(len(righe)):
            w=righe[j]
            for r in range(len(righe[j])):
                d[r] = max((d.get(r) or 0), len(str(w[r])))
    return d

def settings():
    for k,v in config.items():
        if k.startswith('NLS_'):
            show_qry("alter session set %s ='%s'"%(k,v))

def init_db_conn():
    global _CONN
    dburi = config.get('DBURI')
    if not _CONN:
        try:
            _CONN = cx_Oracle.connect(dburi)
        except cx_Oracle.DatabaseError, message:
            print message
    return _CONN

def db_conn():
    return _CONN

def select_qry(sql):
    desc=results=None
    cur = db_conn().cursor()
    try:
        cc = cur.execute(sql)
    except cx_Oracle.DatabaseError, message:
        print message
        cc=None

    if cc:
        results = cc.fetchall()
        desc    = cc.description
    else:
        if cur.rowcount > 1:
            print '%s rows affected'%cur.rowcount
        if cur.rowcount == 1:
            print '%s row affected'%cur.rowcount
        if cur.rowcount == 0:
            print 'no rows affected'

    cur.close()
    _CONN.commit()
    return results,desc

def show_qry(sql):
    if sql.strip().startswith('--'):
        return
    filename=fd=''
    nr=reclen=0
    fd, filename = mkstemp()
    sql = sql.strip().strip(';')
    #emulate pg/mysql limit
    limit = sql.split('limit')
    if len(limit) > 1:
        if sql.lower().find('where') != -1:
            sql=limit[0] + ' and rownum <= ' + limit[1]
        else:
            sql=limit[0] + ' where rownum <= ' + limit[1]
    rs,desc = select_qry(sql)
    if not rs:
        return
    title=[]
    for row in desc:
        title.append(row[0].lower())
    righe = [ title ] + rs
    leng = table(righe)
    for j in leng.values():
        reclen+=j
    for row in righe:#print rows
        for rc in range(len(row)):
            if rc:
                fmt = "| %%-%ss" % (leng[rc])
            else:
                fmt = "%%-%ss" % (leng[rc])
            if row[rc] is None:
                val='NULL'
            else:
                val=row[rc]
            os.write(fd,(fmt%val))
        os.write(fd,'\n')
        if not nr: #print titles
            for rc in range(len(row)):
                if rc:
                    os.write(fd,'+ '+('-'*(leng[rc])))
                else:
                    os.write(fd, ('-'*(leng[rc])))
            os.write(fd,'\n')
        nr+=1
    if nr: nr-=1
    os.write(fd, '(%s rows)\n' % nr )
    os.close(fd)
    pager(filename,reclen,len(rs))

def pager(filename,reclen,totrec):
    if totrec > int(LINES) or reclen > int(COLUMNS):
        pydoc.pager(open(filename).read())
    else:
        print open(filename).read()
    if _FD:
        _FD.write(open(filename).read())
    os.unlink(filename)

def oracle_main(par):
    if not par.get('cmd'):
        while True:
            edit = Edit()
            edit . cmdloop()
            cc = edit.lastcmd.split()
            if cc[0]=='input' and len(cc) == 2:
                par['cmd']=['-f',"%s"%cc[1]]
            else:
                if isinstance(edit.lastcmd, list):
                    edit.lastcmd=' '.join(edit.lastcmd) #join in one line
                par['cmd']=['-c',"%s"%edit.lastcmd]
            oracle_main(par)

    com=par['cmd'][0]
    if com.strip() == '-h':
        print usage
        sys.exit()
    qry=par['cmd'][1]
    if not init_db_conn():
        print 'connection error'
    else:
        if com == '-f':
            input_file(qry)
        elif com=='-c':
            show_qry(qry)

###################################################################################
if __name__ == "__main__":
    usage = 'usage: sql+ [-c <query> | -f <filename> ]'
    parms=dict(cmd=sys.argv[1:])
    init_db_conn()
    settings()
    oracle_main( parms )

-----------------------------------------------------------------------------------------
**configuration file: .sql+**

[globals]
DBURI                   = "user/password@host/dbname"
EDITOR                  = "vim"

[settings]
NLS_DATE_FORMAT         = "YYYY-MM-DD"
NLS_TIMESTAMP_FORMAT    = "YYYY-MM-DD HH24:MI:SS.FF"
NLS_TIMESTAMP_TZ_FORMAT = "YYYY-MM-DD HH24:MI:SS.FFTZD"

[SQL info]
SQL_TABLES              = "SELECT distinct lower(table_name) as table_name FROM user_tab_columns ORDER BY 1"
SQL_SEQUENCES           = "select lower(SEQUENCE_NAME) as sequence_name, MIN_VALUE, MAX_VALUE, INCREMENT_BY, CYCLE_FLAG, ORDER_FLAG, CACHE_SIZE from USER_SEQUENCES ORDER BY 1"
SQL_FOREIGNS            = "SELECT ucc.constraint_name, ucc.column_name ,fc.table_name  FROM   user_cons_columns ucc ,user_constraints fc ,user_constraints uc WHERE  uc.constraint_type = 'R' AND    uc.constraint_name = ucc.constraint_name AND    fc.constraint_name = uc.r_constraint_name AND    uc.table_name='%s' ORDER BY 1, 2"
SQL_DESC                = "SELECT column_name as NAME, data_type AS TYPE, char_length AS LENGTH, nullable, data_default AS "DEFAULT" FROM user_tab_columns WHERE  table_name='%s' ORDER BY column_name"
SQL_CONSTRAINTS         = "SELECT ucc.constraint_name,ucc.column_name, uc.constraint_type, uc.search_condition FROM   user_constraints uc, user_cons_columns ucc WHERE  uc.constraint_name = ucc.constraint_name AND    uc.table_name='%s' AND    uc.constraint_type = 'C' ORDER BY ucc.constraint_name,ucc.position"
SQL_TRIGGERS            = "SELECT trigger_name, trigger_type, triggering_event, table_name, description, trigger_body FROM user_triggers ORDER BY 1"
SQL_LIST_INDEX          = "SELECT case when constraint_type = 'P' then 'PRIMARY KEY' else ' ' end as index_type, ui.index_name, ui.uniqueness, uic.column_name, uic.column_position, uic.descend FROM user_indexes ui JOIN user_ind_columns uic ON uic.index_name = ui.index_name left JOIN user_constraints ON user_constraints.constraint_name = ui.index_name AND user_constraints.constraint_type = 'P' WHERE ui.table_name = '%s' ORDER BY constraint_type, uic.column_position;"
SQL_INDEX               = "SELECT case when constraint_type = 'P' then 'PRIMARY KEY' else ' ' end as index_type, ui.table_name,ui.index_name, ui.uniqueness, uic.column_name, uic.column_position, uic.descend FROM user_indexes ui JOIN user_ind_columns uic ON uic.index_name = ui.index_name left JOIN user_constraints ON user_constraints.constraint_name = ui.index_name AND user_constraints.constraint_type = 'P' WHERE ui.index_name = '%s' ORDER BY constraint_type, uic.column_position;"
