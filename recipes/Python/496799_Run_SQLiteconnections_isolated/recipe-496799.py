import pysqlite2.dbapi2 as sqlite
import Queue, time, thread, os
from threading import Thread

_threadex = thread.allocate_lock()
qthreads = 0
sqlqueue = Queue.Queue()

ConnectCmd = "connect"
SqlCmd = "SQL"
StopCmd = "stop"
class DbCmd:
    def __init__(self, cmd, params=[]):
        self.cmd = cmd
        self.params = params

class DbWrapper(Thread):
    def __init__(self, path, nr):
        Thread.__init__(self)
        self.path = path
        self.nr = nr
    def run(self):
        global qthreads
        con = sqlite.connect(self.path)
        cur = con.cursor()
        while True:
            s = sqlqueue.get()
            print "Conn %d -> %s -> %s" % (self.nr, s.cmd, s.params)
            if s.cmd == SqlCmd:
                commitneeded = False
                res = []
#               s.params is a list to bundle statements into a "transaction"
                for sql in s.params:
                    cur.execute(sql[0],sql[1])
                    if not sql[0].upper().startswith("SELECT"): 
                        commitneeded = True
                    for row in cur.fetchall(): res.append(row)
                if commitneeded: con.commit()
                s.resultqueue.put(res)
            else:
                _threadex.acquire()
                qthreads -= 1
                _threadex.release()
#               allow other threads to stop
                sqlqueue.put(s)
                s.resultqueue.put(None)
                break

def execSQL(s):
    if s.cmd == ConnectCmd:
        global qthreads
        _threadex.acquire()
        qthreads += 1
        _threadex.release()
        wrap = DbWrapper(s.params, qthreads)
        wrap.start()
    elif s.cmd == StopCmd:
        s.resultqueue = Queue.Queue()
        sqlqueue.put(s)
#       sleep until all threads are stopped
        while qthreads > 0: time.sleep(0.1)
    else:
        s.resultqueue = Queue.Queue()
        sqlqueue.put(s)
        return s.resultqueue.get()

if __name__ == "__main__":
    dbname = "test.db"
    execSQL(DbCmd(ConnectCmd, dbname))
    execSQL(DbCmd(SqlCmd, [("create table people (name_last, age integer);",())]))
#   don't add connections before creating table
    execSQL(DbCmd(ConnectCmd, dbname))
#   insert one row
    execSQL(DbCmd(SqlCmd, [("insert into people (name_last, age) values (?, ?);", ('Smith', 80))]))
#   insert two rows in one transaction
    execSQL(DbCmd(SqlCmd, [("insert into people (name_last, age) values (?, ?);", ('Jones', 55)), 
                           ("insert into people (name_last, age) values (?, ?);", ('Gruns', 25))]))
    for p in execSQL(DbCmd(SqlCmd, [("select * from people", ())])): print p
    execSQL(DbCmd(StopCmd))
    os.remove(dbname)
