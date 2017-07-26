#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import psycopg2
import psycopg2.extras
import psycopg2.extensions

DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = "postgres"
SCHEMA = 'postgres'
USER_NAME = 'root'
PASSWORD = 'root'
SHOW_WHITE_SPACE = True # set to False if you need to trim column data

# show table names when called without args
sql = """SELECT table_name FROM information_schema.tables where table_schema = '%s'\n""" % SCHEMA
if len(sys.argv) > 1:
   sql = (" ".join(sys.argv[1:])).strip()

if sql == 'show databases':
   sql = 'select datname as database from pg_database'

if sql == 'show schemas':
	sql = 'select nspname as schema from pg_namespace'

if sql.startswith('describe'):
	sql = """select ordinal_position as index,column_name as column,is_nullable as allow_null,data_type as type FROM information_schema.columns WHERE table_name ='%s' order by ordinal_position  """  % ((sql[len('describe'):]).strip()) 

sys.stderr.write('Connecting to %s...\n' % DATABASE_HOST)
con = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME, host=DATABASE_HOST, password=PASSWORD)

# set autocommit
if  re.search(r'\b(update|insert|delete|drop)\b', sql.lower()):
    print 'Enabling autocommit...'
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
sys.stderr.write("Executing: '%s'\n" % sql)
cur.execute(sql)

rs = []

try:
	rs = cur.fetchall()
except:
	sys.stderr.write('Nothing to fetch.\n')

if not len(rs):
	sys.stderr.write('No results.\n')
	sys.exit(0)

first_row = rs[0]

column_names_with_indexes = [item for item in first_row._index.iteritems()]
sorted_column_names_pairs = sorted(column_names_with_indexes, key=lambda k: k[1])
sorted_column_names = [p[0] for p in sorted_column_names_pairs]

for row in rs:
	row_data =[]
	for idx, col in enumerate(row):
		data = SHOW_WHITE_SPACE and "'" + str(col) + "'" or str(col).strip()
		row_data.append(sorted_column_names[idx].ljust(16) + ': ' + data)
	if len(row) >1:
		sys.stdout.write( '-' * 40 + '\n')
	sys.stdout.write (("\n".join(row_data)).encode('us-ascii', 'xmlcharrefreplace'))
	sys.stdout.write ("\n")
	#print ("\n".join(row_data)).encode('unicode_escape')

cur.close()
con.close()
