#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: schema_ora.py 1754 2014-02-14 08:57:52Z mn $'

# export Oracle schema to text
# usable to compare databases that should be the same
#
# Oracle schema info:
# http://www.eveandersson.com/writing/data-model-reverse-engineering
#
#
# author: Michal Niklas, Adam Kopciński-Galik

OPTIONS = """[OPTIONS]
Options:
--tables_only      raport only tables
--separate-files   save tables, views etc in separate files
                   in db_schema directory,
                   tables are defined as CREATE TABLE statement
--sorted-info      for CREATE TABLE add comment with columns
                   sorted by name
--zip              with --separate-files enabled zip all created files
--date-dir         with --separate-files add date and time
                   to db_schema_[date]_[time] directory
                   with -o[=file_name] save file_name
                   in db_schema_[date]_[time] directory
--force-dir        with --separate-files do not check
                   if db_schema directory exists
-o[=file_name]     send results to file instead of stdout
--version          show version
--add-ver-info     add version information
--ver-info-sql[=SELECT  ... FROM ... ORDER BY ...]
                   extend version information by results of this query
"""

USAGE = 'usage:\n\tschema_ora.py tnsentry username passwd %s' % OPTIONS
JUSAGE = """usage:
  jython schema_ora.py jdbcurl user passwd %s
example:
  jython schema_ora.py jdbc:oracle:thin:@127.0.0.1:1521:dbname usr pwd > db.sch
""" % OPTIONS

import codecs
import sys
import os
import zipfile
import os.path
import time
import re

USE_JYTHON = 0

TABLES_ONLY = 0

SCHEMA_DIR = 'db_schema'
if '--date-dir' in sys.argv:
	SCHEMA_DIR += time.strftime("_%y%m%d_%H%M%S", time.localtime())
TABLES_INFO_DIR    = SCHEMA_DIR + '/tables'
VIEWS_INFO_DIR     = SCHEMA_DIR + '/views'
SEQUENCES_INFO_DIR = SCHEMA_DIR + '/sequences'
FUNCTIONS_INFO_DIR = SCHEMA_DIR + '/functions'
PROCEDURES_INFO_DIR = SCHEMA_DIR + '/procedures'
PACKAGES_INFO_DIR = SCHEMA_DIR + '/packages'
INVALID = '_invalid'

CREATED_FILES = []


try:
	from com.ziclix.python.sql import zxJDBC
	USE_JYTHON = 1
	USAGE = JUSAGE
except:
	import cx_Oracle


DB_ENCODINGS = ('cp1250', 'iso8859_2', 'utf8')

OUT_FILE_ENCODING = 'UTF8'


TABLE_AND_VIEWS_NAMES_SQL = """SELECT DISTINCT table_name
FROM user_tab_columns
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
ORDER BY table_name
"""

TABLE_NAMES_SQL = """SELECT DISTINCT table_name
FROM user_tables
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
AND NOT table_name IN (SELECT view_name FROM user_views)
AND NOT table_name IN (SELECT mview_name FROM user_mviews)
ORDER BY table_name
"""


TABLE_COLUMNS_SQL = """SELECT table_name, column_name
FROM user_tab_columns
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
ORDER BY table_name, column_name
"""


TABLE_INFO_SQL = """SELECT table_name, column_name, data_type, nullable,
decode(default_length, NULL, 0, 1) hasdef,
decode(data_type,
	'DATE', '11',
	'NUMBER', data_precision || ',' || data_scale,
	data_length) data_length
FROM user_tab_columns
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
ORDER BY table_name, column_name
"""

PRIMARY_KEYS_INFO_SQL = """SELECT uc.table_name, ucc.column_name
FROM user_constraints uc, user_cons_columns ucc
WHERE uc.constraint_name = ucc.constraint_name
AND uc.constraint_type = 'P'
AND INSTR(uc.table_name, 'X_') <> 1
AND INSTR(uc.table_name, '$') = 0
ORDER BY uc.table_name, ucc.position
"""


INDEXES_INFO_SQL = """SELECT ui.table_name, ui.index_name, ui.uniqueness
FROM user_indexes ui
WHERE INSTR(ui.table_name, 'X_') <> 1
AND INSTR(ui.table_name, '$') = 0
ORDER BY ui.table_name, ui.index_name
"""


INDEXES_COLUMNS_INFO_SQL = """SELECT table_name, column_name, index_name, column_position, descend
FROM user_ind_columns
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$')  = 0
ORDER BY table_name, index_name, column_position
"""


COMPOSITE_INDEXES_COLUMNS_INFO_SQL = """SELECT table_name, column_name, index_name, column_position
FROM user_ind_columns
WHERE index_name in (select distinct index_name from USER_IND_COLUMNS where column_position > 1)
AND INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$')  = 0
ORDER BY table_name, index_name, column_position
"""

FUNCTION_INDEXES_INFO_SQL = """SELECT table_name, column_expression, index_name, column_position
FROM user_ind_expressions
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
ORDER BY table_name, index_name, column_position
"""


FOREIGN_KEYS_INFO_SQL = """SELECT uc.table_name, ucc.column_name, ucc.position
, fc.table_name, uic.column_position, uic.column_name
, uc.delete_rule
, uc.constraint_name
FROM user_cons_columns ucc
,user_constraints fc
,user_constraints uc
,user_ind_columns uic
WHERE  uc.constraint_type = 'R'
AND    uc.constraint_name = ucc.constraint_name
AND    fc.constraint_name = uc.r_constraint_name
AND uic.index_name=fc.constraint_name
ORDER BY uc.table_name, ucc.position, uic.column_position
"""


DEFAULTS_INFO_SQL = """SELECT table_name, column_name, data_default
FROM   user_tab_columns
WHERE  default_length IS NOT NULL
AND INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
ORDER BY table_name, column_name
"""


SEQUENCES_INFO_SQL = """SELECT sequence_name FROM user_sequences"""


TSEQUENCES_INFO_SQL = """SELECT sequence_name, min_value, max_value, increment_by, last_number, cache_size, cycle_flag, order_flag
FROM user_sequences
"""


VIEWS_INFO_SQL = """SELECT view_name, text
FROM user_views
ORDER BY view_name"""


MVIEWS_INFO_SQL = """SELECT mview_name, query
FROM user_mviews
ORDER BY mview_name
"""


TRIGGERS_INFO_SQL = """SELECT trigger_name, trigger_type, triggering_event, table_name, trim(chr(13) from trim(chr(10) from description)), trigger_body
FROM user_triggers
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') = 0
ORDER BY table_name, trigger_name
"""


TTABLE_NAMES_SQL = """SELECT DISTINCT table_name
FROM user_tab_columns
WHERE INSTR(table_name, 'X_') <> 1
AND INSTR(table_name, '$') < 1
AND NOT table_name IN (SELECT view_name FROM user_views)
AND NOT table_name IN (SELECT mview_name FROM user_mviews)
ORDER BY table_name
"""


TTABLE_COLUMNS = """SELECT column_name, data_type, nullable,
decode(default_length, NULL, 0, 1) hasdef,
decode(data_type,
	'DATE', '11',
	'NUMBER', data_precision || ',' || data_scale,
	data_length) data_length,
	data_default,
	char_length
FROM user_tab_columns
WHERE table_name='%s'
"""

TTABLE_COLUMNS_SQL = TTABLE_COLUMNS + " ORDER BY column_id "
TTABLE_SORTED_COLUMNS_SQL = TTABLE_COLUMNS + " ORDER BY column_name "

TPRIMARY_KEYS_INFO_SQL = """SELECT ucc.column_name
FROM user_constraints uc, user_cons_columns ucc
WHERE uc.constraint_name = ucc.constraint_name
AND uc.constraint_type = 'P'
AND uc.table_name='%s'
"""


TFOREIGN_KEYS_INFO_SQL = """
SELECT uc.table_name, ucc.column_name, ucc.position
, fc.table_name, uic.column_position, uic.column_name
, uc.delete_rule, uc.constraint_name
FROM user_cons_columns ucc
,user_constraints fc
,user_constraints uc
,user_ind_columns uic
WHERE  uc.constraint_type = 'R'
AND    uc.constraint_name = ucc.constraint_name
AND    fc.constraint_name = uc.r_constraint_name
AND uic.index_name=fc.constraint_name
AND uc.table_name='%s'
ORDER BY uc.constraint_name, ucc.position, uic.column_position
"""


TINDEXES_COLUMNS_INFO_SQL = """SELECT uic.index_name, uic.column_name, ui.index_type, uie.column_expression, ui.uniqueness, uic.column_position
FROM user_ind_columns uic
LEFT JOIN (user_indexes ui) ON uic.index_name = ui.index_name
LEFT JOIN (user_ind_expressions uie) ON uic.index_name = uie.index_name
WHERE uic.table_name='%s'
ORDER BY uic.index_name, uic.column_position
"""


TTRIGGERS_INFO_SQL = """SELECT trigger_name, trim(chr(13) from trim(chr(10) from description)), trigger_body
FROM user_triggers
WHERE
table_name = '%s'
ORDER BY table_name, trigger_name
"""


DB_VERSION_SQL = """SELECT * FROM v$version WHERE banner like 'Oracle%'"""


_CONN = None

CREATED_DIRS = []


def ensure_directory(dname):
	"""creates directory if it not exists"""
	if not os.path.exists(dname):
		os.makedirs(dname)
		CREATED_DIRS.append(dname)


RE_INVALID_FNAME = re.compile(r'[^a-z0-9\.\\/]')


def normalize_fname(fname):
	"""replaces to _ strange chars in filename te be created"""
	fname = fname.lower()
	fname = RE_INVALID_FNAME.sub('_', fname)
	return fname


def open_file_write(fname):
	"""opens file for writing in required encoding"""
	CREATED_FILES.append(fname)
	return codecs.open(fname, 'w', OUT_FILE_ENCODING)


def init_db_conn(connect_string, username, passwd):
	"""initializes database connection"""
	global _CONN
	if not _CONN:
		dbinfo = connect_string
		try:
			if USE_JYTHON:
				dbinfo = 'JDBC: %s, user: %s' % (connect_string, username)
				print('--%s' % (dbinfo))
				_CONN = zxJDBC.connect(connect_string, username, passwd, 'oracle.jdbc.driver.OracleDriver')
			else:
				dbinfo = 'db: %s@%s' % (username, connect_string)
				print('--%s' % (dbinfo))
				_CONN = cx_Oracle.connect(username, passwd, connect_string)
		except:
			ex = sys.exc_info()
			serr = 'Exception: %s: %s\n%s' % (ex[0], ex[1], dbinfo)
			print_err(serr)
			return None
	return _CONN


def db_conn():
	"""returns global database connection"""
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


def print_err(serr):
	"""println on stderr"""
	sys.stderr.write('%s\n' % (serr))


def select_qry(querystr):
	"""executes SQL SELECT query"""
	cur = db_conn().cursor()
	cur.execute(querystr)
	results = cur.fetchall()
	cur.close()
	return results


def run_qry(querystr):
	"""executes SQL update/insert etc"""
	cur = db_conn().cursor()
	cur.execute(querystr)
	cur.close()


def fld2str(fld_v):
	"""converts field value into string"""
	if type(fld_v) == type(1.1):
		fld_v = '%s' % fld_v
		if '.' in fld_v:
			fld_v = fld_v.rstrip('0')
			fld_v = fld_v.rstrip('.')
	else:
		fld_v = '%s' % fld_v
		if fld_v.startswith('SYS_C'):
			fld_v = 'SYS_Cxxx'
	return fld_v


def show_qry(title, querystr, fld_join='\t', row_separator=None, fout=None):
	"""shows SQL query results"""
	rs = select_qry(querystr)
	if rs:
		output_line('\n\n--- %s ---' % (title), fout)
		for row in rs:
			line = fld_join.join([fld2str(s) for s in row])
			output_line(line, fout)
			if row_separator:
				output_line(row_separator, fout)


def init_session():
	"""initialization of SQL session"""
	run_qry("ALTER SESSION SET nls_numeric_characters = '.,'")


def get_type_length(data_type, data_length, char_length):
	"""get string with length of field"""
	if data_type == 'NUMBER':
		if data_length == ',':
			return ''
		if data_length == ',0':
			return '(*,0)'
		return '(%s)' % (data_length)
	if data_type == 'RAW':
		return ' (%s)' % (data_length)
	if data_type in ('CHAR', 'VARCHAR2', 'NCHAR', 'NVARCHAR2'):
		return ' (%.0f)' % (char_length)
	return ''


def table_info_row(row):
	"""shows info about table column"""
	column_name = row[0]
	data_type = row[1]
	nullable = row[2]
	hasdef = row[3]
	data_length = row[4]
	data_default = row[5]
	char_length = row[6]
	default_str = nullable_str = ''
	data_length_str = get_type_length(data_type, data_length, char_length)
	if int(hasdef) == 1:
		default_str = ' DEFAULT %s' % (data_default)
	if nullable == 'N':
		nullable_str = ' NOT NULL'
		if default_str.endswith(' '):
			nullable_str = 'NOT NULL'
	if column_name.startswith('_'):
		column_name = '"' + column_name + '"'
	else:
		column_name = column_name.lower()
	return '%(column_name)s %(data_type)s%(data_length)s%(default)s%(nullable)s' % {'column_name': column_name, 'data_type': data_type, 'data_length': data_length_str, 'nullable': nullable_str, 'default': default_str}


def get_table_indices(table, pk_columns=None):
	"""returm table indices"""
	indices_str = ''
	indices = {}
	rs = select_qry(TINDEXES_COLUMNS_INFO_SQL % (table))
	idx_uniques = {}
	for row in rs:
		idx_name = row[0]
		if idx_name.startswith('SYS_'):
			continue
		idx_column = row[1]
		idx_type = row[2]
		idx_expression = row[3]
		idx_unique = row[4]
		if idx_unique != 'UNIQUE':
			idx_unique = ''
		idx_uniques[idx_name] = idx_unique
		if idx_type == 'FUNCTION-BASED NORMAL':
			idx_column = idx_expression
		try:
			indices[idx_name].append(idx_column)
		except KeyError:
			indices[idx_name] = [idx_column, ]
	if indices:
		pk_columns_str = ''
		if pk_columns:
			pk_columns_str = ', '.join(pk_columns).lower()
		idxs = indices.keys()
		idxs.sort()
		idx_lines = []
		for idx in idxs:
			columns_str = ', '.join(indices[idx]).lower()
			if columns_str != pk_columns_str:
				idx_lines.append('CREATE %s INDEX %s ON %s (%s);' % (idx_uniques[idx], idx, table, ', '.join(indices[idx])))
		indices_str = '\n'.join(idx_lines)
	return indices_str


def get_table_triggers(table):
	"""returm table trigger bodies"""
	triggers_str = ''
	triggers_lines = []
	rs = select_qry(TTRIGGERS_INFO_SQL % (table))
	for row in rs:
		trigger_name = row[0].strip().lower()
		description = row[1].strip()
		trigger_body = row[2].strip()
		triggers_lines.append('CREATE OR REPLACE TRIGGER\n%s\n%s\n/\nALTER TRIGGER %s ENABLE;' % (description, trigger_body, trigger_name))
	if triggers_lines:
		triggers_str = '\n\n'.join(triggers_lines)
	return triggers_str


def add_primary_key_ddl(table, sorted_in_comment, lines_ct, lines_sc):
	"""adds information about primary key columns"""
	rs = select_qry(TPRIMARY_KEYS_INFO_SQL % (table))
	pk_columns = []
	for row in rs:
		pk_columns.append(row[0].lower())
	if pk_columns:
		tmp_str = 'PRIMARY KEY (%s)' % (', '.join(pk_columns))
		lines_ct.append(tmp_str)
		if sorted_in_comment:
			lines_sc.append(tmp_str)
	return pk_columns


def get_foreign_keys_dict(table):
	"""returns dictionary with info about foreign keys"""
	fk = {}
	rs = select_qry(TFOREIGN_KEYS_INFO_SQL % (table))
	for row in rs:
		_, cn1, _, tn2, _, cn2, dr, cn = row
		try:
			_ = fk[cn][0]
			_ = fk[cn][2]
		except KeyError:
			fk[cn] = [[cn1, ], [tn2, ], [cn2, ], [dr, ]]
	return fk


def add_foreign_key_ddl(table, sorted_in_comment, lines_ct, lines_sc):
	"""adds information about foreign keys"""
	cnt = 0
	rs = select_qry("""SELECT COUNT(*)
			FROM user_constraints
			WHERE constraint_type = 'R' AND table_name='%s'""" % (table))
	for row in rs:
		cnt = int(row[0])
	if cnt > 0:
		fk = get_foreign_keys_dict(table)
		if fk:
			fkk = fk.keys()
			fkk.sort()
			for cn in fkk:
				columns1 = fk[cn][0]
				table2 = fk[cn][1][0]
				columns2 = fk[cn][2]
				dr = fk[cn][3][0]
				if dr == 'CASCADE':
					dr = 'ON DELETE CASCADE'
				else:
					dr = ''
				tmp_str = 'CONSTRAINT %s FOREIGN KEY (%s) REFERENCES %s (%s) %s ENABLE' % (cn, ','.join(columns1), table2, ','.join(columns2), dr)
				lines_ct.append(tmp_str)
				if sorted_in_comment:
					lines_sc.append(tmp_str)


def create_create_table_ddl(table, sorted_in_comment):
	"""creates DDL with CREATE TABLE for table"""
	# gets information about columns
	rs = select_qry(TTABLE_COLUMNS_SQL % (table))
	lines_ct = []
	lines_sc = []
	for row in rs:
		lines_ct.append(table_info_row(row).strip())

	# information about columns but sorted by column name (will be commented)
	# in output, it will be useful for comparing
	if sorted_in_comment:
		rs = select_qry(TTABLE_SORTED_COLUMNS_SQL % (table))
		for row in rs:
			lines_sc.append(table_info_row(row).strip())

	pk_columns = add_primary_key_ddl(table, sorted_in_comment, lines_ct, lines_sc)
	add_foreign_key_ddl(table, sorted_in_comment, lines_ct, lines_sc)

	# creates DDL CREATE TABLE instruction
	#- \n, is required when column has comment
	ct = 'CREATE TABLE %s (\n\t %s\n);' % (table.lower(), '\n\t,'.join(lines_ct))
	if sorted_in_comment:
		sc = 'CREATE TABLE %s (\n-- \t %s\n-- );' % (table.lower(), '\n-- \t,'.join(lines_sc))
		sc = '\n---------- order by column name ----------\n-- ' + sc + '\n---------- order by column name ----------'
		ct = ct + sc
	indices_str = get_table_indices(table, pk_columns)
	triggers_str = get_table_triggers(table)
	return '%s\n\n%s\n\n%s' % (ct, indices_str, triggers_str)


def save_table_definition(table, sorted_in_comment):
	"""saves DDL in a file"""
	s = create_create_table_ddl(table, sorted_in_comment)
	fname = os.path.join(TABLES_INFO_DIR, '%s.sql' % (normalize_fname(table)))
	f = open_file_write(fname)
	output_line(s, f)
	f.close()
	return 1


def show_tables():
	"""shows info tables"""
	show_qry('tables', TABLE_AND_VIEWS_NAMES_SQL)
	show_qry('table columns', TABLE_COLUMNS_SQL)
	show_qry('columns', TABLE_INFO_SQL)


def show_primary_keys():
	"""shows primary keys"""
	show_qry('primary keys', PRIMARY_KEYS_INFO_SQL)


def show_indexes():
	"""shows indexes"""
	show_qry('indexes', INDEXES_INFO_SQL)
	show_qry('indexes columns', INDEXES_COLUMNS_INFO_SQL)
	show_qry('composite indexes', COMPOSITE_INDEXES_COLUMNS_INFO_SQL)
	show_qry('function indexes', FUNCTION_INDEXES_INFO_SQL)


def show_foreign_keys():
	"""shows foreign keys"""
	show_qry('foreign keys', FOREIGN_KEYS_INFO_SQL)


def show_defaults():
	"""shows default values for columns"""
	show_qry('defaults', DEFAULTS_INFO_SQL)


def show_sequences(separate_files):
	"""shows database sequences"""
	show_qry('sequences', SEQUENCES_INFO_SQL)
	cur = db_conn().cursor()
	if separate_files:
		cur.execute(TSEQUENCES_INFO_SQL)
		rows = cur.fetchall()
		for row in rows:
			sequence_name = row[0]
			min_value = '%.0f' % row[1]
			max_value = '%.0f' % row[2]
			increment_by = '%.0f' % row[3]
			last_number = '%.0f' % row[4]
			cache_size = '%.0f' % row[5]
			cycle_flag = row[6]
			order_flag = row[7]

			if cache_size and cache_size != '0':
				cache_size = 'CACHE ' + cache_size
			else:
				cache_size = 'NOCACHE'

			if order_flag == 'Y':
				order_flag = 'ORDER'
			else:
				order_flag = 'NOORDER'

			if cycle_flag == 'Y':
				cycle_flag = 'CYCLE'
			else:
				cycle_flag = 'NOCYCLE'

			fname = os.path.join(SEQUENCES_INFO_DIR, '%s.sql' % (normalize_fname(sequence_name)))
			fout = open_file_write(fname)
			output_str(fout, "CREATE SEQUENCE %s MINVALUE %s MAXVALUE %s INCREMENT BY %s START WITH %s %s %s %s;\n" % (sequence_name, min_value, max_value, increment_by, last_number, cache_size, order_flag, cycle_flag))
			fout.close()
	cur.close()


def show_views(separate_files):
	"""shows database views"""
	show_qry('views', VIEWS_INFO_SQL, '\n', '\n\n')
	show_qry('materialized views', MVIEWS_INFO_SQL, '\n', '\n\n')
	cur = db_conn().cursor()
	if separate_files:
		cur.execute(VIEWS_INFO_SQL)
		rows = cur.fetchall()
		for row in rows:
			view_name = row[0]
			view_body = row[1]
			fname = os.path.join(VIEWS_INFO_DIR, '%s.sql' % (normalize_fname(view_name)))
			fout = open_file_write(fname)
			output_str(fout, "CREATE OR REPLACE VIEW %s AS\n%s;\n" % (view_name, view_body))
			triggers_str = get_table_triggers(view_name)
			output_str(fout, triggers_str)
			fout.close()
		cur.execute(MVIEWS_INFO_SQL)
		rows = cur.fetchall()
		for row in rows:
			view_name = row[0]
			view_body = row[1]
			fname = os.path.join(VIEWS_INFO_DIR, '%s.sql' % (normalize_fname(view_name)))
			fout = open_file_write(fname)
			output_str(fout, "CREATE MATERIALIZED VIEW %s AS\n%s;\n" % (view_name, view_body))
			indices_str = get_table_indices(view_name)
			output_str(fout, indices_str)
			fout.close()
	cur.close()


def show_normal_procedures(separate_files, title, out_dir=None):
	"""shows valid SQL procedures and functions"""
	return show_procedures("SELECT object_name FROM user_procedures WHERE procedure_name IS NULL AND lower(object_type) = lower('%s') ORDER BY 1", separate_files, title, out_dir)


def show_invalid_procedures(separate_files, title, out_dir=None):
	"""shows invalid SQL procedures and functions"""
	return show_procedures("SELECT object_name FROM user_objects WHERE status = 'INVALID' AND lower(object_type) = lower('%s') ORDER BY 1", separate_files, title, out_dir)


def show_procedures(sql, separate_files, title, out_dir=None):
	"""shows SQL procedures and functions"""
	output_line('\n\n --- %ss ---' % (title))
	fout = None
	cur = db_conn().cursor()
	cur.execute(sql % (title))
	rows = cur.fetchall()
	for row in rows:
		funname = row[0]
		output_line('\n\n -- >>> %s %s >>> --' % (title, funname))
		if separate_files:
			ensure_directory(out_dir)
			fname = os.path.join(out_dir, '%s.sql' % (normalize_fname(funname)))
			fout = open_file_write(fname)
			output_line('CREATE OR REPLACE', fout)
		cur2 = db_conn().cursor()
		cur2.execute("SELECT text FROM user_source where name = '%s' ORDER BY line" % funname)
		lines = cur2.fetchall()
		for line in lines:
			output_line(line[0], fout)
		if lines:
			output_line('\n/\n', fout)
		cur2.close()
		output_line('\n\n -- <<< %s %s <<< --' % (title, funname))
		if fout:
			fout.close()
	cur.close()


def show_packages(separate_files):
	"""shows SQL packages"""
	output_line('\n\n --- packages ---')
	fout = None
	cur1 = db_conn().cursor()
	cur1.execute("SELECT object_name FROM user_objects WHERE object_type='PACKAGE' ORDER BY 1")
	rows = cur1.fetchall()
	for row in rows:
		funname = row[0]
		output_line('\n\n -- >>> package %s >>> --' % (funname))
		if separate_files:
			fname = os.path.join(PACKAGES_INFO_DIR, '%s.sql' % (normalize_fname(funname)))
			fout = open_file_write(fname)
			output_line('CREATE OR REPLACE', fout)
		cur2 = db_conn().cursor()
		cur2.execute("SELECT text FROM sys.user_source where name = '%s' AND type='PACKAGE' ORDER BY line" % funname)
		lines = cur2.fetchall()
		for line in lines:
			output_line(line[0], fout)
		if(lines):
			output_line('\n/\n', fout)
		output_line('\n')
		cur2.close()
		cur3 = db_conn().cursor()
		cur3.execute("SELECT text FROM sys.user_source where name = '%s' AND type='PACKAGE BODY' ORDER BY line" % funname)
		lines = cur3.fetchall()
		if(lines):
			output_line('\nCREATE OR REPLACE ', fout)
		for line in lines:
			output_line(line[0], fout)
		if(lines):
			output_line('\n/\n', fout)
		cur3.close()
		if fout:
			fout.close()
		output_line('\n\n -- <<< package %s <<< --' % (funname))
	cur1.close()


def show_triggers():
	"""shows SQL triggers"""
	show_qry('triggers', TRIGGERS_INFO_SQL, '\n', '\n-- end trigger --\n')


def save_files_in_zip():
	"""saves created files in zip file"""
	if not CREATED_FILES:
		output_line('-- nothing to zip')
	else:
		zip_name = os.path.join(SCHEMA_DIR + '.zip')
		output_line('creating zip %s ...' % (zip_name))
		zip_f = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
		for fn in CREATED_FILES:
			fne = fn.encode(OUT_FILE_ENCODING)
			#print('storing %s...' % (fne))
			zip_f.write(fne)
			os.remove(fne)
		zip_f.close()
		clean_up()


def add_ver_info(separate_files, connect_string, username):
	"""add version information"""
	f = None
	if separate_files:
		ver_file = os.path.join(SCHEMA_DIR, 'version.txt')
		f = open_file_write(ver_file)
	output_line('>>> ver info')
	output_line('date: %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), f)
	output_line('connect string: %s' % (connect_string), f)
	output_line('user: %s' % (username), f)
	script_ver = __version__[5:-2]
	output_line('created by: %s' % (script_ver), f)
	show_qry('DB version', DB_VERSION_SQL, fout=f)
	show_qry('DB name', 'SELECT ora_database_name FROM dual', fout=f)
	sel_info_option = '--ver-info-sql'
	for s in sys.argv[1:]:
		if s.startswith(sel_info_option):
			sel = s[len(sel_info_option):].strip('=')
			try:
				show_qry(sel, sel, fout=f)
			except:
				ex = sys.exc_info()
				serr = '\nSQL: %s\nException: %s: %s\n' % (sel, ex[0], ex[1])
				print_err(serr)
			break
	output_line('<<< ver info')
	if f:
		f.close()


def show_additional_info(separate_files):
	"""shows info about primary keys, procedures, triggers etc"""
	show_primary_keys()
	show_indexes()
	show_foreign_keys()
	show_defaults()
	show_sequences(separate_files)
	show_views(separate_files)
	show_triggers()
	show_normal_procedures(separate_files, 'function', FUNCTIONS_INFO_DIR)
	show_invalid_procedures(separate_files, 'function', FUNCTIONS_INFO_DIR + INVALID)
	show_normal_procedures(separate_files, 'procedure', PROCEDURES_INFO_DIR)
	show_invalid_procedures(separate_files, 'procedure', PROCEDURES_INFO_DIR + INVALID)
	show_packages(separate_files)


def clean_up():
	"""removes created directories after zipping files"""
	for dn in CREATED_DIRS:
		os.rmdir(dn)
	os.rmdir(SCHEMA_DIR)


def dump_db_info(separate_files, out_f, stdout):
	"""saves information about database schema in file/files"""
	test = '--test' in sys.argv
	if test or separate_files:
		for dn in (TABLES_INFO_DIR, VIEWS_INFO_DIR, SEQUENCES_INFO_DIR, FUNCTIONS_INFO_DIR, PROCEDURES_INFO_DIR, PACKAGES_INFO_DIR):
			ensure_directory(dn)

		if not test:
			sorted_in_comment = '--sorted-info' in sys.argv
			rs = select_qry(TABLE_NAMES_SQL)
			if rs:
				for row in rs:
					table = row[0]
					save_table_definition(table, sorted_in_comment)
	else:
		show_tables()
	if not TABLES_ONLY and not test:
		show_additional_info(separate_files)
	output_line('\n\n--- the end ---')
	if out_f:
		out_f.close()
		sys.stdout = stdout
	if '--zip' in sys.argv:
		save_files_in_zip()


def get_option_value(prefix):
	"""returns FILENAME for -o prefix and -oFILENAME or -o=FILENAME"""
	result = None
	for s in sys.argv:
		if s.startswith(prefix):
			result = s[len(prefix):]
			if result.startswith('='):
				result = result[1:]
	return result


def main():
	"""main function"""
	conn_args = [s for s in sys.argv[1:] if not s.startswith('-')]
	if len(conn_args) != 3:
		print(USAGE)
		return 0
	connect_string, username, passwd = conn_args
	separate_files = '--separate-files' in sys.argv
	if separate_files:
		if os.path.exists(SCHEMA_DIR):
			if not '--force-dir' in sys.argv:
				print_err('Output directory "%s" already exists,\nuse --force-dir or --date-dir option!' % (SCHEMA_DIR))
				return 0
	stdout = sys.stdout
	out_f = None
	out_fn = get_option_value('-o')
	if out_fn:
		if '--date-dir' in sys.argv:
			os.mkdir(SCHEMA_DIR)
			out_fn = os.path.join(SCHEMA_DIR, out_fn)
		out_f = open(out_fn, 'w')
		sys.stdout = out_f
		CREATED_FILES.append(out_fn)

	if not init_db_conn(connect_string, username, passwd):
		print_err('Something is terribly wrong with db connection')
		return 0
	init_session()
	if '--add-ver-info' in sys.argv:
		add_ver_info(separate_files, connect_string, username)
	dump_db_info(separate_files, out_f, stdout)


if '--version' in sys.argv:
	print(__version__)
elif __name__ == '__main__':
	if '--tables_only' in sys.argv:
		TABLES_ONLY = 1
	if len(sys.argv) < 4:
		print(USAGE)
	else:
		main()
