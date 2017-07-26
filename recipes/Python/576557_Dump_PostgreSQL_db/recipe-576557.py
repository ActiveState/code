#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: schema_pg.py 1754 2014-02-14 08:57:52Z mn $'

# export PostgreSQL schema to text
# usable to compare databases that should be the same
#
# PostgreSQL schema info:
# http://www.alberton.info/postgresql_meta_info.html
#
#
# author: Michal Niklas

USAGE = 'usage:\n\tschema_pg.py connect_string\n\t\tconnect string:\n\t\t\thost:[port:]database:user:password\n\t\tor for ODBC:\n\t\t\tdatabase/user/passwd\n\t\tor (pyodbc)\n\t\t\tDriver={PostgreSQL};Server=IP address;Port=5432;Database=myDataBase;Uid=myUsername;Pwd=myPassword;'

import sys
import array
import exceptions

USE_JYTHON = 0

TABLES_ONLY = 0

try:
	from com.ziclix.python.sql import zxJDBC
	USE_JYTHON = 1
	USAGE = """usage:
\tschema_inf.py jdbcurl user passwd
example:
\tjython schema_py.py jdbc:postgresql://isof-test64:5434/gryfcard_mrb?stringtype=unspecified user passwd > db.schema 2> db.err
"""
except:
	USE_JYTHON = 0


DB_ENCODINGS = ('cp1250', 'iso8859_2', 'utf8')

OUT_FILE_ENCODING = 'UTF8'


TABLE_NAMES_SQL = """SELECT DISTINCT table_name
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
ORDER BY 1"""


TABLE_COLUMNS_SQL = """SELECT DISTINCT table_name, column_name
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
ORDER BY 1, 2"""


TABLE_INFO_SQL = """SELECT table_name, column_name, ordinal_position, data_type, is_nullable, character_maximum_length, numeric_precision
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
ORDER BY 1, 2
"""

PRIMARY_KEYS_INFO_SQL = """SELECT t.relname AS table_name, array_to_string(c.conkey, ' ') AS constraint_key
FROM pg_constraint c
LEFT JOIN pg_class t  ON c.conrelid  = t.oid
WHERE c.contype = 'p'
AND position('_' in t.relname ) <> 1
ORDER BY table_name;
"""


INDEXES_INFO_SQL = """SELECT relname, indisunique
FROM pg_class, pg_index
WHERE pg_class.oid = pg_index.indexrelid
AND oid IN (
    SELECT indexrelid
      FROM pg_index, pg_class
     WHERE pg_class.relname='%s'
       AND pg_class.oid=pg_index.indrelid
       AND indisprimary != 't'
     )
ORDER BY 1, 2
"""


INDEXES_COLUMNS_INFO1_SQL = """SELECT relname, indkey
FROM pg_class, pg_index
WHERE pg_class.oid = pg_index.indexrelid
AND pg_class.oid IN (
    SELECT indexrelid
      FROM pg_index, pg_class
     WHERE pg_class.relname='%s'
       AND pg_class.oid=pg_index.indrelid
       AND indisprimary != 't'
)
ORDER BY 1
"""


INDEXES_COLUMNS_INFO2_SQL = """SELECT DISTINCT a.attname
     FROM pg_index c
LEFT JOIN pg_class t
       ON c.indrelid  = t.oid
LEFT JOIN pg_attribute a
       ON a.attrelid = t.oid
      AND a.attnum = ANY(indkey)
    WHERE t.relname = '%s'
      AND a.attnum = %s
"""


FOREIGN_KEYS_INFO_SQL = """SELECT t.relname AS table_name, t2.relname AS references_table
FROM pg_constraint c
LEFT JOIN pg_class t  ON c.conrelid  = t.oid
LEFT JOIN pg_class t2 ON c.confrelid = t2.oid
WHERE c.contype = 'f'
AND position('_' in t.relname ) <> 1
ORDER BY table_name, references_table
"""


DEFAULTS_INFO_SQL = """SELECT table_name, column_name, column_default
FROM information_schema.columns
WHERE column_default IS NOT NULL
AND position('_' in table_name) <> 1
ORDER BY table_name, column_name"""


VIEWS_INFO_SQL = """SELECT viewname, definition
FROM pg_views
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY viewname
"""


TRIGGERS_INFO_SQL = """SELECT event_object_table, trigger_name, action_orientation, action_timing, event_manipulation, action_statement
FROM information_schema.triggers
WHERE trigger_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY 1, 2, 3, 4, 5"""


_CONN = None

TABLES = []


def init_db_conn(connect_string, username, passwd):
	"""initializes db connections, can work with PyGres or psycopg2"""
	global _CONN
	try:
		dbinfo = connect_string
		print(dbinfo)
		if USE_JYTHON:
			_CONN = zxJDBC.connect(connect_string, username, passwd, 'org.postgresql.Driver')
		elif '/' in connect_string:
			import odbc
			_CONN = odbc.odbc(connect_string)
			print(_CONN)
		elif connect_string.startswith('Driver='):
			import pyodbc
			# Driver={PostgreSQL};Server=IP address;Port=5432;Database=myDataBase;Uid=myUsername;Pwd=myPassword;
			# Driver={PostgreSQL};Server=isof-test64;Port=5435;Database=isof_stable;Uid=postgres;Pwd=postgres;
			_CONN = pyodbc.connect(connect_string)
			print(_CONN)
		else:
			# 'host:[port]:database:user:password'
			arr = connect_string.split(':')
			if len(arr) > 4:
				host = '%s:%s' % (arr[0], arr[1])
				port = int(arr[1])
				dbname = arr[2]
				user = arr[3]
				passwd = arr[4]
			elif len(arr) == 4:
				host = arr[0]
				port = -1
				dbname = arr[1]
				user = arr[2]
				passwd = arr[3]
			else:
				raise exceptions.ImportError('Incorrect connect_string!\n\n%s' % (USAGE))
			if port > 0:
				host = host.split(':')[0]
				sport = 'port=%d' % (port)
			else:
				sport = ''
			dsn = "host=%s %s dbname=%s user=%s password=%s" % (host, sport, dbname, user, passwd)
			print(dsn)
			dbinfo = 'db: %s:%s' % (host, dbname)
			use_pgdb = 0
			try:
				import psycopg2
			except:
				try:
					import pgdb
					use_pgdb = 1
				except:
					raise exceptions.ImportError('No PostgreSQL library, install psycopg2 or PyGres!')
			if not _CONN:
				print(dbinfo)
				if use_pgdb:
					_CONN = pgdb.connect(database=dbname, host=host, user=user, password=passwd)
					print(_CONN)
				else:
					_CONN = psycopg2.connect(dsn)
					print(_CONN)
	except:
		ex = sys.exc_info()
		s = 'Exception: %s: %s\n%s' % (ex[0], ex[1], dbinfo)
		print(s)
		return None
	return _CONN


def db_conn():
	"""access to global db connection"""
	return _CONN


def output_str(fout, line):
	"""outputs line to fout trying various encodings in case of encoding errors"""
	if fout:
		try:
			fout.write(line)
		except (UnicodeDecodeError, UnicodeEncodeError):
			try:
				fout.write(line.encode(OUT_FILE_ENCODING))
			except (UnicodeDecodeError, UnicodeEncodeError):
				ok = 0
				for enc in DB_ENCODINGS:
					try:
						line2 = line.decode(enc)
						#fout.write(line2.encode(OUT_FILE_ENCODING))
						fout.write(line2)
						ok = 1
						break
					except (UnicodeDecodeError, UnicodeEncodeError):
						pass
				if not ok:
					fout.write('!!! line cannot be encoded !!!\n')
					fout.write(repr(line))
		fout.write('\n')
		fout.flush()


def output_line(line, fout=None):
	"""outputs line"""
	line = line.rstrip()
	output_str(fout, line)
	output_str(sys.stdout, line)


def select_qry(querystr):
	"""return rows from SELECT"""
	if querystr:
		cur = db_conn().cursor()
		cur.execute(querystr)
		results = cur.fetchall()
		cur.close()
		return results


def fld2str(fld_v):
	"""converts field value into string"""
	if type(fld_v) == type(1.1):
		fld_v = '%s' % fld_v
		if '.' in fld_v:
			fld_v = fld_v.rstrip('0')
			fld_v = fld_v.rstrip('.')
	else:
		fld_v = '%s' % fld_v
	return fld_v


def show_qry(title, querystr, fld_join='\t', row_separator=None):
	"""prints rows from SELECT"""
	output_line('\n\n')
	output_line('--- %s ---' % title)
	rs = select_qry(querystr)
	if rs:
		for row in rs:
			output_line(fld_join.join([fld2str(s) for s in row]))
			if row_separator:
				output_line(row_separator)
	else:
		output_line(' -- NO DATA --')


def show_qry_tables(title, querystr, fld_join='\t', row_separator=None):
	"""prints rows from SELECT"""
	output_line('\n\n')
	output_line('--- %s ---' % title)
	cnt = 0
	for tbl in TABLES:
		rs = select_qry(querystr % tbl)
		if rs:
			for row in rs:
				output_line(fld_join.join([str(s) for s in row]))
				cnt += 1
				if row_separator:
					output_line(row_separator)
	if cnt == 0:
		output_line(' -- NO DATA --')


def show_qry_ex(querystr, table, fld_join='\t', row_separator=None):
	rs = select_qry(querystr % table)
	if rs:
		for row in rs:
			output_line("%s%s%s" % (table, fld_join, fld_join.join([str(s) for s in row])))
			if row_separator:
				output_line(row_separator)


def init_session():
	"""place to change db session settings like locale"""
	pass


def show_tables():
	cur = db_conn().cursor()
	cur.execute(TABLE_NAMES_SQL)
	for row in cur.fetchall():
		TABLES.append(row[0])
	cur.close()
	show_qry('tables', TABLE_NAMES_SQL)
	show_qry('table columns', TABLE_COLUMNS_SQL)
	show_qry('columns', TABLE_INFO_SQL)


def show_primary_keys():
	show_qry('primary keys', PRIMARY_KEYS_INFO_SQL)


def show_indexes():
	output_line('\n\n')
	output_line('--- %s ---' % 'indexes')
	for tbl in TABLES:
		show_qry_ex(INDEXES_INFO_SQL, tbl)
	#show_qry('indexes columns', INDEXES_COLUMNS_INFO_SQL)
	output_line('\n\n')
	output_line('--- %s ---' % 'indexes columns')
	cur = db_conn().cursor()
	for tbl in TABLES:
		#print
		#print tbl
		cur.execute(INDEXES_COLUMNS_INFO1_SQL % tbl)
		for row in cur.fetchall():
			idxname = row[0]
			idxflds = '%s' % row[1]
			#print '\n', tbl, '\t', idxname, '\t', idxflds
			for fld in idxflds.split():
				sql = INDEXES_COLUMNS_INFO2_SQL % (tbl, fld)
				cur.execute(sql)
				for row in cur.fetchall():
					output_line("%s\t%s\t%s" % (tbl, idxname, row[0]))


def show_foreign_keys():
	show_qry('foreign keys', FOREIGN_KEYS_INFO_SQL)


def show_defaults():
	show_qry('defaults', DEFAULTS_INFO_SQL)


def show_views():
	show_qry('views', VIEWS_INFO_SQL, '\n', '\n\n')


def get_arg_type(at):
	"""returns type name from type id"""
	cur = db_conn().cursor()
	cur.execute("select pg_catalog.format_type('%s', NULL)" % at)
	row = cur.fetchone()
	return row[0]


def join_arg(arg_name, arg_type, mode='i'):
	"""make string with procedure arguments"""
	if mode == 'o':
		out_s = 'OUT '
	else:
		out_s = ''
	return '%s%s %s' % (out_s, arg_name, arg_type)


def get_subfields(subfield_fld):
	"""changes function arguments names into array of strings, for example:
	   ['code', 'status_str', 'err_desctiption'],
	   various drivers return it as various types"""
	if subfield_fld:
		subfield = subfield_fld
		if isinstance(subfield_fld, array.array):
			subfield = ','.join([str(s) for s in subfield_fld])
			#print('subfield arr: >>%s<<' % (subfield_fld))
			subfield = '%s' % (subfield)
		else:
			subfield = '%s' % (subfield_fld)
		subfield = subfield.replace('{', '')
		subfield = subfield.replace('}', '')
		subfield = subfield.replace('[', '')
		subfield = subfield.replace(']', '')
		subfield = subfield.replace("'", '')
		#print('subfield: >>%s<<' % (subfield))
		arr = subfield.split(',')
		if arr and len(arr) > 0:
			return arr
	return None


def show_procedures():
	argtypes_dict = {}
	output_line('\n\n --- procedures ---')
	cur = db_conn().cursor()
	cur.execute("""SELECT DISTINCT routine_name
        FROM information_schema.routines
        WHERE specific_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY 1""")
	rows = cur.fetchall()
	for rt_row in rows:
		funname = rt_row[0]
		cur.execute("""SELECT CASE
         WHEN pg_proc.proretset
         THEN 'setof ' || pg_catalog.format_type(pg_proc.prorettype, NULL)
         ELSE pg_catalog.format_type(pg_proc.prorettype, NULL) END,
         pg_proc.proargtypes,
         pg_proc.proargnames,
         pg_proc.prosrc,
         pg_proc.proallargtypes,
         pg_proc.proargmodes,
         pg_language.lanname
    FROM pg_catalog.pg_proc
         JOIN pg_catalog.pg_namespace
           ON (pg_proc.pronamespace = pg_namespace.oid)
         JOIN pg_catalog.pg_language
           ON (pg_proc.prolang = pg_language.oid)
   WHERE pg_proc.prorettype <> 'pg_catalog.cstring'::pg_catalog.regtype
     AND (pg_proc.proargtypes[0] IS NULL
      OR pg_proc.proargtypes[0] <> 'pg_catalog.cstring'::pg_catalog.regtype)
     AND NOT pg_proc.proisagg
     AND pg_proc.proname = '%s'
     AND pg_namespace.nspname = 'public'
     AND pg_catalog.pg_function_is_visible(pg_proc.oid);""" % funname)
		for row in cur.fetchall():
			ret_type = row[0]
			args = ''
			argtypes = []
			argmodes = get_subfields(row[5])
			argtypes_str = '%s' % row[1]
			proc_body = '%s' % row[3]
			lang = row[6]
			argtypes_nrs = get_subfields(row[4])
			if argtypes_str:
				if not argtypes_nrs:
					argtypes_nrs = argtypes_str.split()
					argmodes = 'i' * len(argtypes_nrs)
				for at in argtypes_nrs:
					if at:
						if not at in argtypes_dict.keys():
							argtypes_dict[at] = get_arg_type(at)
						ats = argtypes_dict[at]
						argtypes.append(ats)
				argnames = get_subfields(row[2])
				if argnames:
					args = ', '.join([join_arg(a, t, m) for (a, t, m) in zip(argnames, argtypes, argmodes)])

			output_line('\n\n -- >>> %s >>> --' % funname)
			lines = proc_body.split('\n')
			output_line('CREATE FUNCTION %s(%s) RETURNS %s\nAS $$' % (funname, args, ret_type))
			was_line = 0
			for line in lines:
				line = line.rstrip()
				if line or was_line:
					was_line = 1
					output_line(line)
			output_line('$$')
			output_line('  LANGUAGE %s;' % (lang))
			output_line('\n\n -- <<< %s <<< --' % funname)
	cur.close()


def show_triggers():
	show_qry('triggers', TRIGGERS_INFO_SQL, '\n', '\n\n')


def test():
	main('127.0.0.1:music:postgres:postgres')


def main(connect_string):
	username = None
	passwd = None
	if (len(sys.argv) > 2):
		username = sys.argv[2]
	if (len(sys.argv) > 3):
		passwd = sys.argv[3]
	if not init_db_conn(connect_string, username, passwd):
		print('Something is terribly wrong with db connection')
	else:
		init_session()
		show_tables()
		if not TABLES_ONLY:
			show_primary_keys()
			show_indexes()
			show_foreign_keys()
			show_defaults()
			show_views()
			show_triggers()
			show_procedures()
		print('\n\n--- the end ---')


if '--version' in sys.argv:
	print(__version__)
elif '--test' in sys.argv:
	test()
elif '--help' in sys.argv:
	print(USAGE)
elif __name__ == '__main__':
	if '--tables_only' in sys.argv:
		TABLES_ONLY = 1
	if len(sys.argv) < 2:
		#print('arg len: %d' % (len(sys.argv)))
		print(USAGE)
	else:
		main(sys.argv[1])
