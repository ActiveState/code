from threading import Thread
from Queue import Queue

import apsw

class SingleThreadOnly(object):
    def __init__(self, db):
        self.cnx = apsw.Connection(db) 
        self.cursor = self.cnx.cursor()
    def execute(self, req, arg=None):
        self.cursor.execute(req, arg or tuple())
    def select(self, req, arg=None):
        self.execute(req, arg)
        for raw in self.cursor:
            yield raw
    def close(self):
        self.cnx.close()

class MultiThreadOK(Thread):
    def __init__(self, db):
        super(MultiThreadOK, self).__init__()
        self.db=db
        self.reqs=Queue()
        self.start()
    def run(self):
        cnx = apsw.Connection(self.db) 
        cursor = cnx.cursor()
        while True:
            req, arg, res = self.reqs.get()
            if req=='--close--': break
            cursor.execute(req, arg)
            if res:
                for rec in cursor:
                    res.put(rec)
                res.put('--no more--')
        cnx.close()
    def execute(self, req, arg=None, res=None):
        self.reqs.put((req, arg or tuple(), res))
    def select(self, req, arg=None):
        res=Queue()
        self.execute(req, arg, res)
        while True:
            rec=res.get()
            if rec=='--no more--': break
            yield rec
    def close(self):
        self.execute('--close--')

if __name__=='__main__':

    db='people.db'
    multithread=True
    
    if multithread:
        sql=MultiThreadOK(db)
    else:
        sql=SingleThreadOnly(db)

    sql.execute("create table people(name,first)")
    sql.execute("insert into people values('VAN ROSSUM','Guido')")
    sql.execute("insert into people values(?,?)", ('TORVALDS','Linus'))
    for f, n in sql.select("select first, name from people"):
        print f, n
    sql.close()
