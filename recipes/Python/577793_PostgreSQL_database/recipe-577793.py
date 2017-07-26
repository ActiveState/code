#!/usr/bin/env python
import os
import time

username = 'root'
defaultdb = 'postgres'
port = '5433'
backupdir='/www/backup/'
date = time.strftime('%Y-%m-%d')

#GET DB NAMES
get_db_names="psql -U%s -d%s -p%s --tuples-only -c '\l' | awk -F\| '{ print $1 }' | grep -E -v '(template0|template1|^$)'" % (username, defaultdb, port)

#MAKE BACKUP OF SYSTEMGRANTS
os.popen("pg_dumpall -p%s -g|gzip -9 -c > %s/system.%s.gz" % (port, backupdir, date))

#MAKING DB BACKUP
for base in os.popen(get_db_names).readlines():
        base = base.strip()
        fulldir = backupdir + base
        if not os.path.exists(fulldir):
                os.mkdir(fulldir)
        filename = "%s/%s-%s.sql" % (fulldir, base, date)
        os.popen("nice -n 19 pg_dump -C -F c -U%s -p%s %s > %s" % (username, port, base, filename))
