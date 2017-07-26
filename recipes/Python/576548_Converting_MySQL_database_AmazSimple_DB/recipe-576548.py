#!/usr/bin/env python
access_key = ''
secret_key = ''
import boto
import MySQLdb
from MySQLdb import cursors
import threading

db_user = ''
db_name = ''

db = MySQLdb.connect(user=db_user,db=db_name,cursorclass=cursors.DictCursor)
c = db.cursor()
sdb = boto.connect_sdb(access_key, secret_key)

def get_or_create_domain(domain):
    try:
        d = sdb.get_domain(domain)
    except boto.exception.SDBResponseError:
        d = sdb.create_domain(domain)
    return d

def get_primary_key(table_name, cursor):
    """
    Returns a dictionary of fieldname -> infodict for the given table,
    where each infodict is in the format:
        {'primary_key': boolean representing whether it's the primary key,
         'unique': boolean representing whether it's a unique index}
    """
    cursor.execute("SHOW INDEX FROM %s" % table_name)
    indexes = {}
    for row in cursor.fetchall():
        if row['Key_name'] == 'PRIMARY':
            return row['Column_name']
    raise("Table %s does not have a primary key" % table_name)

class BotoWorker(threading.Thread):
    def __init__(self, name, record, domain):
        self.domain = domain
        self.name = name
        self.record = record
        threading.Thread.__init__(self)

    def run(self):
            print "inserting %s" % self.name
            item = self.domain.new_item(self.name)
            for key, value in self.record.items():
                try:
                    item[key] = value
                except UnicodeDecodeError:
                    item[key] = 'unicode error'

def main():
    c.execute("show tables;")
    for table in c.fetchall():
        table = table["Tables_in_%s" % db]
        print "loading data from %s" % table
        total = c.execute("select * from %s" % table)
        print "fetched %s items from mysql" % total

        for record in c.fetchall():
            name = record.pop(get_primary_key(table, c))
            thread_started = False
            while not thread_started:
                if threading.activeCount() < 10:
                    print "got a thread %s" % threading.activeCount()
                    BotoWorker(name=name, record=record, domain=get_or_create_domain(table)).start()
                    thread_started = True

if __name__ == '__main__':
    main()
