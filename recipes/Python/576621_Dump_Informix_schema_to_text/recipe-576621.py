#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: schema_inf.py 3307 2017-11-29 06:18:57Z mn $'

# export Informix schema to text using ODBC
# usable to compare databases that should be the same
#
# schema info:
# http://publib.boulder.ibm.com/infocenter/idshelp/v10/index.jsp?topic=/com.ibm.sqlr.doc/sqlrmst41.htm
#
# useful queries:
# http://pentestmonkey.net/blog/informix-sql-injection-cheat-sheet/
#
# tested with
# client: IBM Informix ODBC Driver 3.50 TC3DE
# server: IBM Informix Dynamic Server Version 11.50.TC2DE
#
# previous versions of ODBC client fails sometimes with:
# dbi.operation-error:
# [Informix][Informix ODBC Driver][Informix]
# Character host variable is too short for the data. in FETCH
#
# Table names that start with '_' are ignored as they are temp tables
#
# https://code.activestate.com/recipes/576621-dump-informix-schema-to-text/
#
# author: Michal Niklas

USAGE = 'usage:\n\tschema_inf.py connect_string\n\t\tconnect string: odbc_database/user/password'

import re
import sys
import time
import traceback

USE_JYTHON = 0

try:
	from com.ziclix.python.sql import zxJDBC
	USE_JYTHON = 1
	USAGE = """usage:
\tschema_inf.py jdbcurl user passwd
example:
\tjython schema_inf.py jdbc:informix-sqli://169.0.1.82:9088/multiso2:INFORMIXSERVER=ol_1150;DELIMIDENT=y; user passwd > db.schema 2> db.err
"""
except:
	USAGE = 'usage:\n\tschema_inf.py connect_string\n\t\tconnect string: odbc_database/user/password'
	USE_JYTHON = 0
	import odbc


DB_ENCODINGS = ('cp1250', 'iso8859_2', 'utf8')

OUT_FILE_ENCODING = 'UTF8'

FILTER_TEMP = """tabtype='T'
AND systables.tabid >= 100
AND tabname[1] <> '_'
"""

if '--no-temp-tables' in sys.argv:
	FILTER_TEMP += """AND tabname NOT LIKE '%tmp%'
AND tabname NOT LIKE '%temp%'
"""

DB_VERSION_SQL = """SELECT FIRST 1 DBINFO('version','full') FROM systables"""

TABLE_NAMES_SQL = """SELECT tabname
FROM systables
WHERE
%s
ORDER BY tabname""" % (FILTER_TEMP)


TABLE_COLUMNS_SQL = """SELECT tabname, colname
FROM syscolumns, systables
WHERE
%s
AND syscolumns.tabid = systables.tabid
ORDER BY tabname, colname
""" % (FILTER_TEMP)

TABLE_INFO_SQL = """SELECT tabname, colname, colno, HEX(coltype),
CASE MOD(coltype, 256)
	WHEN  0 THEN 'char'
	WHEN  1 THEN 'smallint'
	WHEN  2 THEN 'integer'
	WHEN  3 THEN 'float'
	WHEN  4 THEN 'smallfloat'
	WHEN  5 THEN 'decimal(' || (collength / 256)::int || ', ' || mod(collength, 256) || ')'
	WHEN  6 THEN 'serial'
	WHEN  7 THEN 'date'
	WHEN  8 THEN 'money(' || (collength / 256)::int || ', ' || mod(collength, 256) || ')'
	WHEN  9 THEN 'null'
	WHEN 10 THEN 'datetime '  || substr(hex(collength), -2, 1) || ' to ' || substr(hex(collength), -1, 1)
	WHEN 11 THEN 'byte'
	WHEN 12 THEN 'text'
	WHEN 13 THEN 'varchar'
	WHEN 14 THEN 'interval'
	WHEN 15 THEN 'nchar'
	WHEN 16 THEN 'nvarchar'
	WHEN 17 THEN 'int8'
	WHEN 18 THEN 'serial8'
	WHEN 19 THEN 'set'
	WHEN 20 THEN 'multiset'
	WHEN 21 THEN 'list'
	WHEN 22 THEN 'row (unnamed)'
	WHEN 23 THEN 'collection'
	WHEN 40 THEN 'lvarchar fixed-length opaque types'
	WHEN 41 THEN 'blob, boolean, clob variable-length opaque types'
	WHEN 43 THEN 'lvarchar (client-side only)'
	WHEN 45 THEN 'boolean'
	WHEN 52 THEN 'bigint'
	WHEN 53 THEN 'bigserial'
	WHEN 2061 THEN 'idssecuritylabel'
	WHEN 4118 THEN 'row (named)'
	ELSE '???'
END CASE, collength
FROM syscolumns, systables
WHERE
%s
AND syscolumns.tabid = systables.tabid
ORDER BY tabname, colname
""" % (FILTER_TEMP)


KEYS_INFO_SQL = """select tabname, a.colname column1, b.colname column2,
c.colname column3, d.colname column4, e.colname column5,
f.colname column6, g.colname column7, h.colname column8,
i.colname column9, j.colname column10, k.colname column11,
l.colname column12, m.colname column13, n.colname column14,
o.colname column15, p.colname column16
from sysindexes si, systables st, sysconstraints sc, syscolumns a,
outer syscolumns b,
outer syscolumns c, outer syscolumns d, outer syscolumns e,
outer syscolumns f, outer syscolumns g, outer syscolumns h,
outer syscolumns i, outer syscolumns j, outer syscolumns k,
outer syscolumns l, outer syscolumns m, outer syscolumns n,
outer syscolumns o, outer syscolumns p
WHERE
%s
AND sc.tabid = st.tabid
AND si.idxname = sc.idxname
AND sc.constrtype='%%s'
and st.tabid = si.tabid
and st.tabid = a.tabid
and st.tabid = b.tabid
and st.tabid = c.tabid
and st.tabid = d.tabid
and st.tabid = e.tabid
and st.tabid = f.tabid
and st.tabid = g.tabid
and st.tabid = h.tabid
and st.tabid = i.tabid
and st.tabid = j.tabid
and st.tabid = k.tabid
and st.tabid = l.tabid
and st.tabid = m.tabid
and st.tabid = n.tabid
and st.tabid = o.tabid
and st.tabid = p.tabid
and a.colno = part1
and b.colno = part2
and c.colno = part3
and d.colno = part4
and e.colno = part5
and f.colno = part6
and g.colno = part7
and h.colno = part8
and i.colno = part9
and j.colno = part10
and k.colno = part11
and l.colno = part12
and m.colno = part13
and n.colno = part14
and o.colno = part15
and p.colno = part16
ORDER BY tabname, column1, column2, column3, column4, column5
""" % (FILTER_TEMP.replace('systables.', 'st.'))


INDEXES_INFO_SQL = """SELECT idxname, idxtype
FROM systables, sysindices
WHERE tabname='%s'
AND sysindices.tabid = systables.tabid
AND tabtype='T'
AND systables.tabid >= 100
ORDER BY tabname, idxname
"""

# http://groups.google.pl/group/comp.databases.informix/browse_thread/thread/a488c9bfb3a71c5a?ie=UTF-8&oe=utf-8&q=%22outer+syscolumns+f%22
INDEXES_COLUMNS_INFO_SQL = """select idxtype, a.colname column1, b.colname column2,
c.colname column3, d.colname column4, e.colname column5,
f.colname column6, g.colname column7, h.colname column8,
i.colname column9, j.colname column10, k.colname column11,
l.colname column12, m.colname column13, n.colname column14,
o.colname column15, p.colname column16
from sysindexes si, systables st, syscolumns a,
outer syscolumns b,
outer syscolumns c, outer syscolumns d, outer syscolumns e,
outer syscolumns f, outer syscolumns g, outer syscolumns h,
outer syscolumns i, outer syscolumns j, outer syscolumns k,
outer syscolumns l, outer syscolumns m, outer syscolumns n,
outer syscolumns o, outer syscolumns p
WHERE tabname='%s'
AND tabtype='T'
AND tabname[1] <> '_'
AND st.tabid >= 100
and st.tabid = si.tabid
and st.tabid = a.tabid
and st.tabid = b.tabid
and st.tabid = c.tabid
and st.tabid = d.tabid
and st.tabid = e.tabid
and st.tabid = f.tabid
and st.tabid = g.tabid
and st.tabid = h.tabid
and st.tabid = i.tabid
and st.tabid = j.tabid
and st.tabid = k.tabid
and st.tabid = l.tabid
and st.tabid = m.tabid
and st.tabid = n.tabid
and st.tabid = o.tabid
and st.tabid = p.tabid
and a.colno = part1
and b.colno = part2
and c.colno = part3
and d.colno = part4
and e.colno = part5
and f.colno = part6
and g.colno = part7
and h.colno = part8
and i.colno = part9
and j.colno = part10
and k.colno = part11
and l.colno = part12
and m.colno = part13
and n.colno = part14
and o.colno = part15
and p.colno = part16
ORDER BY tabname, column1, column2, column3, column4, column5
"""


DEFAULTS_INFO_SQL = """SELECT tabname, colname, type, default
FROM syscolumns, systables, sysdefaults
WHERE
%s
AND syscolumns.tabid = systables.tabid
AND sysdefaults.tabid = systables.tabid
AND syscolumns.colno = sysdefaults.colno
ORDER BY tabname, colname""" % (FILTER_TEMP)


VIEWS_INFO_SQL = """SELECT tabname, tabid
FROM systables
WHERE
%s""" % (FILTER_TEMP.replace("'T'", "'V'"))

VIEWS_TEXT_SQL = """SELECT viewtext
FROM sysviews
WHERE tabid=%s
ORDER BY seqno
"""


TRIGGERS_INFO_SQL = """SELECT tabname, trigname, event
FROM systables, systriggers
WHERE
%s
AND systables.tabid = systriggers.tabid
ORDER BY tabname, trigname""" % (FILTER_TEMP)


PROCEDURES_INFO_SQL = """SELECT procname, numargs, isproc, paramtypes::LVARCHAR, variant, handlesnulls, parallelizable
FROM sysprocedures
WHERE internal='f' AND mode IN ('D', 'd', 'O', 'o')
ORDER BY procname, numargs, procid"""


SQL_TYPES = """SELECT COUNT(*)::int,
CASE MOD(coltype, 256)
	WHEN  0 THEN 'char'
	WHEN  1 THEN 'smallint'
	WHEN  2 THEN 'integer'
	WHEN  3 THEN 'float'
	WHEN  4 THEN 'smallfloat'
	WHEN  5 THEN 'decimal(' || (collength / 256)::int || ', ' || mod(collength, 256) || ')'
	WHEN  6 THEN 'serial'
	WHEN  7 THEN 'date'
	WHEN  8 THEN 'money(' || (collength / 256)::int || ', ' || mod(collength, 256) || ')'
	WHEN  9 THEN 'null'
	WHEN 10 THEN 'datetime '  || substr(hex(collength), -2, 1) || ' to ' || substr(hex(collength), -1, 1)
	WHEN 11 THEN 'byte'
	WHEN 12 THEN 'text'
	WHEN 13 THEN 'varchar'
	WHEN 14 THEN 'interval'
	WHEN 15 THEN 'nchar'
	WHEN 16 THEN 'nvarchar'
	WHEN 17 THEN 'int8'
	WHEN 18 THEN 'serial8'
	WHEN 19 THEN 'set'
	WHEN 20 THEN 'multiset'
	WHEN 21 THEN 'list'
	WHEN 22 THEN 'row (unnamed)'
	WHEN 23 THEN 'collection'
	WHEN 40 THEN 'lvarchar fixed-length opaque types'
	WHEN 41 THEN 'blob, boolean, clob variable-length opaque types'
	WHEN 43 THEN 'lvarchar (client-side only)'
	WHEN 45 THEN 'boolean'
	WHEN 52 THEN 'bigint'
	WHEN 53 THEN 'bigserial'
	WHEN 2061 THEN 'idssecuritylabel'
	WHEN 4118 THEN 'row (named)'
	ELSE '???'
END CASE
FROM syscolumns, systables
WHERE
%s
AND syscolumns.tabid = systables.tabid
GROUP BY 2
ORDER BY 1 desc, 2
""" % (FILTER_TEMP)

_CONN = None

_CONNECT_STRING = None
_USERNAME = None
_PASSWD = None

TABLES = []


def init_db_conn(connect_string, username, passwd):
	"""initializes db connections"""
	global _CONN
	if not _CONN:
		global _CONNECT_STRING
		global _USERNAME
		global _PASSWD
		_CONNECT_STRING = connect_string
		_USERNAME = username
		_PASSWD = passwd
		dbinfo = connect_string
		try:
			if USE_JYTHON:
				output_line(dbinfo)
				_CONN = zxJDBC.connect(connect_string, username, passwd, 'com.informix.jdbc.IfxDriver')
			else:
				(dbname, dbuser, _) = connect_string.split('/', 3)
				dbinfo = 'db: %s:%s' % (dbname, dbuser)
				try:
					_CONN = odbc.odbc(connect_string)
					output_line(dbinfo)
				except KeyboardInterrupt:
					raise
			add_ver_info(connect_string, username)
		except:
			ex = sys.exc_info()
			s = 'Exception: %s: %s\n%s' % (ex[0], ex[1], dbinfo)
			output_line(s)
			return None
	return _CONN


def db_conn():
	"""access to global db connection"""
	return _CONN


def reload_conn():
	"""refreshes db connection"""
	global _CONN
	_CONN = None
	init_db_conn(_CONNECT_STRING, _USERNAME, _PASSWD)


def show_db_error(querystr):
	"""shows exception info"""
	ex = sys.exc_info()
	s = 'Exception: %s: %s\n\nSomething is terribly wrong with query:\n%s\n\n' % (ex[0], ex[1], querystr)
	output_line('\n\n!!!\n\n%s\n\n!!!\n\n' % (s))
	sys.stderr.write(s)
	traceback.print_exc()
	reload_conn()


RE_DATETIME = re.compile(r'datetime (.) to (.)', re.IGNORECASE)

IFX_DATETYPE = {
	'0': "YEAR",
	'2': "MONTH",
	'4': "DAY",
	'6': "HOUR",
	'8': "MINUTE",
	'A': "SECOND",
	'B': "FRACTION(1)",
	'C': "FRACTION(2)",
	'D': "FRACTION(3)",
	'E': "FRACTION(4)",
	'F': "FRACTION(5)",
	}


def linefilter_datetime(s):
	"""converts 'datetime 0 to 4'
		to 'datetime YEAR to DAY'
	"""
	line = s
	rx = RE_DATETIME.search(line)
	if rx:
		txt = line[rx.start(1):rx.end(2)]
		txt2 = '%s to %s' % (IFX_DATETYPE[rx.group(1)], IFX_DATETYPE[rx.group(2)])
		line = line.replace(txt, txt2)
	return line


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


def output_line(line, linefilter=None):
	"""outputs line"""
	if linefilter:
		line = linefilter(line)
	line = line.rstrip()
	output_str(sys.stdout, line)


def print_err(serr):
	"""println on stderr"""
	sys.stderr.write('%s\n' % (serr))
	output_line('\nERROR! ERROR!\n%s\n' % (serr))


def select_qry(querystr):
	"""return rows from SELECT"""
	if querystr:
		try:
			cur = db_conn().cursor()
			cur.execute(querystr)
			results = cur.fetchall()
			cur.close()
			return results
		except KeyboardInterrupt:
			raise
		except:
			show_db_error(querystr)


def field_str(fld_value):
	"""convert fld to printable text"""
	if not fld_value:
		return ''
	try:
		s = '%s' % (fld_value)
		#s = str(fld_value)
		return s.rstrip()
	except:
		return "???????"


def print_start_info(title):
	output_line('\n\n')
	output_line('--- %s (START) ---' % title)


def print_stop_info(title):
	output_line('--- %s (END) ---' % title)
	output_line('\n\n')


def show_qry(title, querystr, fld_join='\t', row_separator=None, linefilter=None):
	"""prints rows from SELECT"""
	print_start_info(title)
	rs = select_qry(querystr)
	if rs:
		for row in rs:
			output_line(fld_join.join([field_str(s) for s in row]), linefilter=linefilter)
			if row_separator:
				output_line(row_separator)
	else:
		output_line(' -- NO DATA --')
	print_stop_info(title)


def show_qry_ex(querystr, table, fld_join='\t', row_separator=None, linefilter=None):
	"""like show_qry() but with table name as first column"""
	rs = select_qry(querystr % table)
	if rs:
		for row in rs:
			output_line("%s%s%s" % (table, fld_join, fld_join.join([field_str(s) for s in row])), linefilter=linefilter)
			if row_separator:
				output_line(row_separator)


def init_session():
	"""place to change db session settings like locale"""
	pass


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
	show_qry('DB name', "SELECT DBINFO('dbname') FROM systables WHERE tabid = 1")
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
	"""prints table names"""
	cur = db_conn().cursor()
	cur.execute(TABLE_NAMES_SQL)
	for row in cur.fetchall():
		if not row[0].startswith('_'):
			TABLES.append(row[0])
	cur.close()
	show_qry('tables', TABLE_NAMES_SQL)
	show_qry('table columns', TABLE_COLUMNS_SQL)
	show_qry('columns', TABLE_INFO_SQL, linefilter=linefilter_datetime)


def show_primary_keys():
	"""print primary keys"""
	show_qry('primary keys', KEYS_INFO_SQL % ('P'))


def show_indexes():
	"""print indexes"""
	title = 'indexes'
	print_start_info(title)
	for tbl in TABLES:
		show_qry_ex(INDEXES_INFO_SQL, tbl)
	#show_qry('indexes columns', INDEXES_COLUMNS_INFO_SQL)
	print_stop_info(title)

	title = 'indexes columns'
	print_start_info(title)
	for tbl in TABLES:
		show_qry_ex(INDEXES_COLUMNS_INFO_SQL, tbl)
	print_stop_info(title)


def show_foreign_keys():
	"""print forign keys"""
	show_qry('foreign keys', KEYS_INFO_SQL % ('R'))


def show_defaults():
	"""print defaults"""
	show_qry('defaults', DEFAULTS_INFO_SQL)


def show_views():
	"""print views"""
	title = 'views'
	print_start_info(title)
	cur = db_conn().cursor()
	try:
		cur.execute(VIEWS_INFO_SQL)
		for row in cur.fetchall():
			tabname = row[0]
			tabid = row[1]
			querystr = VIEWS_TEXT_SQL % tabid
			try:
				cur2 = db_conn().cursor()
				cur2.execute(querystr)
				output_line(tabname)
				vt = []
				for row2 in cur2.fetchall():
					vt.append(row2[0])
				vtt = ''.join(vt)
				output_line(vtt.rstrip())
				output_line('')
			except:
				show_db_error(querystr)
	except:
		show_db_error(VIEWS_INFO_SQL)
	print_stop_info(title)


def show_types_stat():
	show_qry('column type count', SQL_TYPES, linefilter=linefilter_datetime)


def get_body(qry):
	"""joins body of stored procedure or trigger"""
	body_lines = ['', ]
	if qry:
		rs = select_qry(qry)
		if rs:
			for row in rs:
				body_lines.append(field_str(row[0]))
	return ''.join(body_lines)


def show_procedures():
	"""show procedures and functions"""
	show_qry('procedures/functions', PROCEDURES_INFO_SQL)
	title = 'procedures/functions bodies'
	print_start_info(title)
	querystr1 = """SELECT procid, procname
FROM sysprocedures
WHERE internal='f' AND mode IN ('D', 'd', 'O', 'o')
ORDER BY procname, numargs, procid"""
	querystr2 = """SELECT data
FROM sysprocbody
WHERE procid=%s
AND datakey='T'
ORDER BY seqno
	"""
	rs = select_qry(querystr1)
	if rs:
		for row in rs:
			funname = row[1]
			body = get_body(querystr2 % row[0])
			output_line('\n\n -- >>> %s >>> --' % funname)
			output_line(body)
			output_line('\n\n -- <<< %s <<< --' % funname)
	print_stop_info(title)


def show_triggers():
	"""show triggers"""
	show_qry('triggers', TRIGGERS_INFO_SQL)
	title = 'triggers bodies'
	print_start_info(title)
	querystr1 = """SELECT trigid, tabname, trigname
FROM systables, systriggers
WHERE tabtype='T'
AND systables.tabid >= 100
AND systables.tabid = systriggers.tabid
ORDER BY tabname, trigname"""
	querystr2 = """SELECT data FROM systrigbody
WHERE trigid=%s
AND (datakey = 'D')
ORDER BY seqno
	"""
	querystr3 = """SELECT data FROM systrigbody
WHERE trigid=%s
AND (datakey = 'A')
ORDER BY seqno
"""
	rs = select_qry(querystr1)
	if rs:
		for row in rs:
			trigname = 'trigger %s' % (row[2])
			trigid = row[0]
			for row in rs:
				body_def = get_body(querystr2 % trigid)
				body_txt = get_body(querystr3 % trigid)
				output_line('\n\n -- >>> %s >>> --' % trigname)
				output_line(body_def)
				output_line(body_txt)
				output_line('\n\n -- <<< %s <<< --' % trigname)
	print_stop_info(title)


def get_info_filter():
	result = ''
	for s in sys.argv[1:]:
		if s.startswith('--info-filter='):
			_, result = s.split('=', 1)
	if not result:
		result = 'kifdvtpT'
	return result


def main():
	"""main"""
	if '--version' in sys.argv:
		print(__version__)
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
	if not init_db_conn(connect_string, username, passwd):
		output_line('Something is terribly wrong with db connection')
	else:
		tables_only = '--tables-only' in sys.argv
		info_filter = get_info_filter()
		t0 = time.time()
		init_session()
		show_tables()
		if not tables_only and info_filter:
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


if __name__ == '__main__':
	main()
