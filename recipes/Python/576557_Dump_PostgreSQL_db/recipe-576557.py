#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: schema_pg.py 3307 2017-11-29 06:18:57Z mn $'

# export PostgreSQL schema to text
# usable to compare databases that should be the same
#
# PostgreSQL schema info:
# http://www.alberton.info/postgresql_meta_info.html
#
# https://code.activestate.com/recipes/576557-dump-postgresql-db-schema-to-text/
#
# author: Michal Niklas

USAGE = """usage:
	schema_pg.py connect_string
		connect string:
			host:[port:]database:user:password
		or for ODBC:
			database/user/passwd
		or (pyodbc)
			Driver={PostgreSQL};Server=IP address;Port=5432;Database=myDataBase;Uid=myUsername;Pwd=myPassword;
"""

import array
import exceptions
import sys
import time
import traceback

USE_JYTHON = 0

TABLES_ONLY = '--tables_only' in sys.argv

OUTPUT_FILE = sys.stdout

try:
	from com.ziclix.python.sql import zxJDBC
	USE_JYTHON = 1
	USAGE = """usage:
\tschema_py.py jdbcurl user passwd
example:
\tjython schema_py.py jdbc:postgresql://isof-test64:5434/gryfcard_mrb?stringtype=unspecified user passwd > db.schema 2> db.err
"""
except:
	USE_JYTHON = 0


DB_ENCODINGS = ('cp1250', 'iso8859_2', 'utf8')

OUT_FILE_ENCODING = 'UTF8'


DB_VERSION_SQL = """SELECT version()"""

TABLE_NAMES_SQL = """SELECT DISTINCT table_name
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
AND position('pg_' in table_name) <> 1
AND NOT table_name IN (SELECT viewname FROM pg_views)
ORDER BY 1"""


TABLE_COLUMNS_SQL = """SELECT DISTINCT table_name, column_name
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
AND position('pg_' in table_name) <> 1
AND position('_' in column_name) <> 1
AND NOT table_name IN (SELECT viewname FROM pg_views)
ORDER BY 1, 2"""

TABLE_COLUMN_NAME_BY_IDX = """SELECT column_name
FROM information_schema.columns
WHERE table_name = '%s'
AND ordinal_position = %s"""


TABLE_INFO_SQL = """SELECT table_name, column_name,
case
	when data_type='numeric' and numeric_precision is not null then data_type || '(' || numeric_precision || ',' || numeric_scale || ')'
	when character_maximum_length is not null then data_type || '(' || character_maximum_length || ')'
	else data_type end as data_type,
is_nullable
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
AND position('pg_' in table_name) <> 1
AND NOT table_name IN (SELECT viewname FROM pg_views)
AND position('_' in column_name) <> 1
ORDER BY 1, 2
"""

SQL_TYPES = """SELECT COUNT(*), case when data_type='numeric' and numeric_precision is not null then data_type || '(' || numeric_precision || ',' || numeric_scale || ')' else data_type end
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
AND position('pg_' in table_name) <> 1
AND NOT table_name IN (SELECT viewname FROM pg_views)
AND position('_' in column_name) <> 1
GROUP BY 2
ORDER BY 1 DESC, 2
"""


xxPRIMARY_KEYS_INFO_SQL = """SELECT t.relname AS table_name, array_to_string(c.conkey, ' ') AS constraint_key
FROM pg_constraint c
LEFT JOIN pg_class t  ON c.conrelid  = t.oid
WHERE c.contype = 'p'
AND position('_' in t.relname) <> 1
AND position('pg_' in t.relname) <> 1
ORDER BY table_name;
"""


PRIMARY_KEYS_INFO_SQL = """select tc.table_name, kc.column_name
from
    information_schema.table_constraints tc,
    information_schema.key_column_usage kc
where
    tc.constraint_type = 'PRIMARY KEY'
    and tc.table_schema = 'public'
    and position('_' in tc.table_name) <> 1
    and position('pg_' in tc.table_name) <> 1
    and kc.table_name = tc.table_name and kc.table_schema = tc.table_schema
    and kc.constraint_name = tc.constraint_name
order by 1, 2;
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

# http://stackoverflow.com/questions/1567051/introspect-postgresql-8-3-to-find-foreign-keys
FOREIGN_KEYS_INFO_SQL = """SELECT "table", array_agg(columns)::varchar, "foreign table", array_agg("foreign columns")::varchar, conname, 'ALTER TABLE ONLY ' || "table" || ' ADD CONSTRAINT ' || conname || ' FOREIGN KEY (' || trim(both '{}' from array_agg(columns)::varchar) || ') REFERENCES ' || "foreign table" || '(' || trim(both '{}' from array_agg("foreign columns")::varchar) || ');'
FROM (SELECT conrelid::regclass AS "table",
		a.attname as columns,
		confrelid::regclass as "foreign table",
		af.attname as "foreign columns",
		conname
	FROM pg_attribute AS af,
		pg_attribute AS a,
		(SELECT conrelid,
			confrelid,
			conkey[i] AS conkey,
			confkey[i] as confkey,
			conname
		FROM (SELECT conrelid,
				confrelid,
				conkey,
				confkey,
				generate_series(1, array_upper(conkey, 1)) AS i,
				conname
			FROM pg_constraint
				WHERE contype = 'f'
		) AS ss
		) AS ss2
	WHERE af.attnum = confkey
	AND af.attrelid = confrelid
	AND a.attnum = conkey
	AND a.attrelid = conrelid
	AND position('_' in conrelid::regclass::varchar) <> 1
	AND position('pg_' in conrelid::regclass::varchar) <> 1
) AS ss3
GROUP BY "table",
	"foreign table",
	conname
ORDER BY 1, 2, 3, 4;
"""


DEFAULTS_INFO_SQL = """SELECT table_name, column_name, column_default
FROM information_schema.columns
WHERE column_default IS NOT NULL
AND position('_' in table_name) <> 1
AND position('pg_' in table_name) <> 1
AND position('_' in column_name) <> 1
ORDER BY table_name, column_name"""


VIEW_NAMES_SQL = """SELECT DISTINCT table_name
FROM information_schema.columns
WHERE table_schema='public'
AND position('_' in table_name) <> 1
AND position('pg_' in table_name) <> 1
AND table_name IN (SELECT viewname FROM pg_views)
ORDER BY 1
"""


VIEWS_INFO_SQL = """SELECT 'CREATE OR REPLACE VIEW ', viewname, ' AS ', definition
FROM pg_views
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
AND position('_' in viewname) <> 1
AND position('pg_' in viewname) <> 1
ORDER BY viewname
"""


TRIGGERS_INFO_SQL = """SELECT event_object_table, trigger_name, action_orientation, action_timing, event_manipulation, action_statement
FROM information_schema.triggers
WHERE trigger_schema NOT IN ('pg_catalog', 'information_schema')
AND position('_' in event_object_table) <> 1
AND position('pg_' in event_object_table) <> 1
ORDER BY 1, 2, 3, 4, 5"""


xxPROCEDURE_NAMES = """SELECT DISTINCT routine_name
FROM information_schema.routines
WHERE specific_schema NOT IN ('pg_catalog', 'information_schema')
AND position('_' in routine_name) <> 1
AND position('pg_' in routine_name) <> 1
AND position('dblink_' in routine_name) <> 1
AND position('dex_' in routine_name) <> 1
AND position('prsd_' in routine_name) <> 1
AND position('rewrite' in routine_name) <> 1
AND position('_tsquery' in routine_name) < 1
AND routine_name NOT IN ('array_search', 'bytea_export', 'bytea_to_largeobject',
'headline', 'lexize', 'parse', 'rank', 'rank_cd',
'rewrite', 'rewrite_accum', 'rewrite_finish',
'set_curcfg', 'set_curdict', 'set_curprs', )
ORDER BY 1"""


xxPROCEDURE_NAMES = """SELECT DISTINCT routine_name, external_language
FROM information_schema.routines
WHERE specific_schema NOT IN ('pg_catalog', 'information_schema')
AND position('_' in routine_name) <> 1
AND position('pg_' in routine_name) <> 1
AND position('ts_debug' in routine_name) <> 1
AND external_language IN ('SQL', 'PLPGSQL', 'PLPYTHONU')
ORDER BY routine_name, external_language"""


PROCEDURE_NAMES = """SELECT proname, proname || '(' || pg_get_function_arguments(p.oid) || ')', lanname
FROM pg_catalog.pg_proc p
LEFT JOIN pg_catalog.pg_language l ON l.oid = prolang
JOIN pg_catalog.pg_namespace n
        ON n.oid = p.pronamespace
        WHERE n.nspname = 'public'
AND position('_' in p.proname) <> 1
AND position('pg_' in p.proname) <> 1
AND position('ts_debug' in p.proname) <> 1
ORDER BY 1, 2, 3
"""

_CONN = None

TABLES = []


def init_db_conn(connect_string, username, passwd, show_connection_info, show_version_info=True):
	"""initializes db connections, can work with PyGres or psycopg2"""
	global _CONN
	try:
		dbinfo = connect_string
		if show_connection_info:
			print(dbinfo)
		if USE_JYTHON:
			_CONN = zxJDBC.connect(connect_string, username, passwd, 'org.postgresql.Driver')
		elif '/' in connect_string:
			import odbc
			_CONN = odbc.odbc(connect_string)
			if show_connection_info:
				print(_CONN)
		elif connect_string.startswith('Driver='):
			import pyodbc
			# Driver={PostgreSQL};Server=IP address;Port=5432;Database=myDataBase;Uid=myUsername;Pwd=myPassword;
			# Driver={PostgreSQL};Server=isof-test64;Port=5435;Database=isof_stable;Uid=postgres;Pwd=postgres;
			_CONN = pyodbc.connect(connect_string)
			if show_connection_info:
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
			if show_connection_info:
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
				if show_connection_info:
					print(dbinfo)
				if use_pgdb:
					_CONN = pgdb.connect(database=dbname, host=host, user=user, password=passwd)
					if show_connection_info:
						print(_CONN)
				else:
					_CONN = psycopg2.connect(dsn)
					if show_connection_info:
						print(_CONN)
		if show_version_info:
			add_ver_info(connect_string, username)
	except:
		ex = sys.exc_info()
		s = 'Exception: %s: %s\n%s' % (ex[0], ex[1], dbinfo)
		print(s)
		return None
	return _CONN


def db_conn():
	"""access to global db connection"""
	global _CONN
	return _CONN


def db_close():
	"""closes global db connection"""
	global _CONN
	if _CONN:
		_CONN.close()
	_CONN = None


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
						if not ok:
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
	output_str(OUTPUT_FILE, line)


def print_err(serr):
	"""println on stderr"""
	sys.stderr.write('%s\n' % (serr))
	output_line('\nERROR! ERROR!\n%s\n' % (serr))


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


def print_start_info(title):
	output_line('\n\n')
	output_line('--- %s (START) ---' % title)


def print_stop_info(title):
	output_line('--- %s (END) ---' % title)
	output_line('\n\n')


def show_qry(title, querystr, fld_join='\t', row_separator=None):
	"""prints rows from SELECT"""
	print_start_info(title)
	rs = select_qry(querystr)
	if rs:
		for row in rs:
			output_line(fld_join.join([fld2str(s) for s in row]))
			if row_separator:
				output_line(row_separator)
	else:
		output_line(' -- NO DATA --')
	print_stop_info(title)


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
	global TABLES
	TABLES = []


def add_ver_info(connect_string, username):
	"""add version information"""
	title = 'info'
	print_start_info(title)
	output_line('date: %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	output_line('connect string: %s' % (connect_string))
	output_line('user: %s' % (username))
	script_ver = __version__[5:-2]
	output_line('created by: %s' % (script_ver))
	print_stop_info(title)
	show_qry('DB version', DB_VERSION_SQL)
	show_qry('DB name', 'SELECT current_catalog')
	sel_info_option = '--ver-info-sql'
	for s in sys.argv[1:]:
		if s.startswith(sel_info_option):
			sel = s[len(sel_info_option):].strip('=')
			try:
				show_qry(sel, sel)
			except:
				ex_info = traceback.format_exc()
				serr = '\nSQL: %s\nException: %s\n' % (sel, ex_info)
				print_err(serr)
			break


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
	show_qry('primary keys idxs', PRIMARY_KEYS_INFO_SQL)
	"""
	title = 'primary keys'
	print_start_info(title)
	cur = db_conn().cursor()
	cur.execute(PRIMARY_KEYS_INFO_SQL)
	for row in cur.fetchall():
		pk_flds = []
		tblname = row[0]
		if tblname in TABLES:
			pk_idxs = '%s' % row[1]
			for fld_idx in pk_idxs.split():
				sql = TABLE_COLUMN_NAME_BY_IDX % (tblname, fld_idx)
				cur.execute(sql)
				for row in cur.fetchall():
					pk_flds.append(row[0])
			output_line("%s\t(%s)" % (tblname, '-'.join(pk_flds)))
	print_stop_info(title)"""


def show_indexes():
	title = 'indexes'
	print_start_info(title)
	for tbl in TABLES:
		show_qry_ex(INDEXES_INFO_SQL, tbl)
	#show_qry('indexes columns', INDEXES_COLUMNS_INFO_SQL)
	print_stop_info(title)

	title = 'indexes columns'
	print_start_info(title)
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
	print_stop_info(title)


def show_foreign_keys():
	show_qry('foreign keys', FOREIGN_KEYS_INFO_SQL)


def show_defaults():
	show_qry('defaults', DEFAULTS_INFO_SQL)


def show_views():
	show_qry('view names', VIEW_NAMES_SQL)
	show_qry('views', VIEWS_INFO_SQL, '\n', '\n\n')


def show_types_stat():
	show_qry('column type count', SQL_TYPES)


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
	show_qry('procedure names', PROCEDURE_NAMES)
	argtypes_dict = {}
	title = 'procedures'
	print_start_info(title)
	cur = db_conn().cursor()
	cur.execute(PROCEDURE_NAMES)
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
			args = argtypes_str
			proc_body = '%s' % row[3]
			lang = row[6]
			argtypes_nrs = get_subfields(row[4])
			if argtypes_str:
				if not argtypes_nrs:
					argtypes_nrs = argtypes_str.split()
					argmodes = 'i' * len(argtypes_nrs)
				for at in argtypes_nrs:
					if at:
						if at not in argtypes_dict.keys():
							argtypes_dict[at] = get_arg_type(at)
						ats = argtypes_dict[at]
						argtypes.append(ats)
				if argtypes:
					args = ', '.join(argtypes)
				argnames = get_subfields(row[2])
				if argnames:
					args = ', '.join([join_arg(a, t, m) for (a, t, m) in zip(argnames, argtypes, argmodes)])

			output_line('\n\n -- >>> %s(%s) [%s] >>> --' % (funname, args, lang))
			lines = proc_body.rstrip().split('\n')
			output_line('CREATE OR REPLACE FUNCTION %s(%s) RETURNS %s\nAS $$' % (funname, args, ret_type))
			was_line = 0
			for line in lines:
				line = line.rstrip()
				if line or was_line:
					was_line = 1
					output_line(line)
			output_line('$$')
			output_line('  LANGUAGE %s;' % (lang))
			output_line(' -- <<< %s(%s) [%s] <<< --' % (funname, args, lang))
			output_line('')
			output_line('')
	cur.close()
	print_stop_info(title)


def show_triggers():
	show_qry('triggers', TRIGGERS_INFO_SQL, '\n', '\n\n')


def test():
	info_filer = 'kifdvtp'
	#main('127.0.0.1:music:postgres:postgres', None)
	get_schema('test-baza.heuthesd:5494:pg_flugo:postgres:postgres', 'postgres', 'postgres', info_filer, True)


def get_schema(connect_string, username, passwd, info_filter, show_connection_info):
	db_close()
	t0 = time.time()
	if not init_db_conn(connect_string, username, passwd, show_connection_info):
		print('Something is terribly wrong with db connection')
	else:
		init_session()
		show_tables()
		if not TABLES_ONLY and info_filter:
			if 'k' in info_filter:
				show_primary_keys()
			if 'i' in info_filter:
				show_indexes()
			if 'f' in info_filter:
				show_foreign_keys()
			if 'd' in info_filter:
				show_defaults()
			if 'v' in info_filter:
				show_views()
			if 't' in info_filter:
				show_triggers()
			if 'p' in info_filter:
				show_procedures()
			if 'T' in info_filter:
				show_types_stat()
	t2 = time.time()
	td = t2 - t0
	output_line('\n\nexecution time: %d min %d sec' % (divmod(td, 60)))
	output_line('\n\n-- the end, filter [%s] --' % (info_filter))
	db_close()


def get_info_filter():
	result = ''
	for s in sys.argv[1:]:
		if s.startswith('--info-filter='):
			_, result = s.split('=', 1)
	if not result:
		result = 'kifdvtpT'
	return result


def main():
	if '--version' in sys.argv:
		print(__version__)
		return
	if '--test' in sys.argv:
		test()
		return
	if '--help' in sys.argv:
		print(USAGE)
		return
	args = [x for x in sys.argv[1:] if not x.startswith('-')]
	if not args:
		print(USAGE)
		return
	connect_string = args[0]
	username = None
	passwd = None
	if (len(args) > 1):
		username = args[1]
	if (len(args) > 2):
		passwd = args[2]
	info_filter = get_info_filter()
	get_schema(connect_string, username, passwd, info_filter, False)


if __name__ == '__main__':
	main()
