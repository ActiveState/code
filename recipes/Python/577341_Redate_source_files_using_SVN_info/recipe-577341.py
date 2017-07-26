#!/usr/bin/env python
# -*- coding: utf8 -*-

__version__ = '$Id: svn_redater.py 748 2010-07-30 09:59:56Z mn $'

USAGE = "svn_redater.py\n\tredate source files according to svn data"

"""
Iterates through a directory, reading the data from svn info that looks like:
   $Id: svn_redater.py 748 2010-07-30 09:59:56Z mn $
from source files.
Parses the datetime from svn info and if it differs from file
modification datetime then changes file datetime

author: Michal Niklas
"""

import re
import os
import os.path
import sys
import time

ALL_CNT = 0
CHANGED_CNT = 0
DEBUG = 0

# which file should be checked
EXTENSIONS = ('.py', '.pas', '.inc', '.java', '.c', '.cpp', '.h',)


def log_error(s):
	sys.stderr.write('%s\n' % (s))


def show_fdt(fdt):
	"""human readable format of file modification datetime"""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(fdt))


def svndtinfo2time(ts):
	"""changes svn date ('2009-10-30 13:17:45') to number of seconds since 1970-01-01"""
	tpl = time.strptime(ts+'UTC', '%Y-%m-%d %H:%M:%S%Z')
	return time.mktime(tpl)


dt_re = re.compile(r'\d+ (\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)Z ')

def extract_svn_dt(line):
	"""change svn info:
		'$Id: svn_redater.py 748 2010-07-30 09:59:56Z mn $'
	into 
		'2009-10-30 13:17:45'"""
	result = None
	rx = dt_re.search(line)
	if rx:
		result = rx.group(1)
	return result


def redate_file(fn):
	"""redates file if file modification datetime differs from svn info"""
	global ALL_CNT, CHANGED_CNT
	ALL_CNT += 1
	svn_dt = None
	s = os.stat(fn)
	file_time = s[8]
	if DEBUG:
		print(fn)
	f = open(fn, 'rb')
	try:
		for line in f.readlines():
			if '$Id:' in line:
				svn_dt = extract_svn_dt(line)
				break
	finally:
		f.close()
	if svn_dt:
		svn_time = svndtinfo2time(svn_dt)
		secs_diff = file_time - svn_time
		MAX_DIFF = 130.0
		if secs_diff > MAX_DIFF or secs_diff < -MAX_DIFF:
			print "%s    %s -> %s" % (fn, show_fdt(file_time), show_fdt(svn_time))
			os.utime(fn, (svn_time, svn_time))
			CHANGED_CNT += 1


def process_dir(_, dir_name, files):
	"""looks for source files in dir"""
	sys.stdout.write('%-70s\r' % (dir_name))
	for fname in files:
		can_change = False
		fnl = fname.lower()
		for ext in EXTENSIONS:
			if fnl.endswith(ext):
				can_change = True
				break
		if can_change:
			fname = os.path.join(dir_name, fname)
			if os.path.isfile(fname):
				redate_file(fname)


def main():
	os.path.walk('.', process_dir, None)
	print '\nChecked: %d\nChanged %d\n' % (ALL_CNT, CHANGED_CNT)


if '--version' in sys.argv:
	print __version__
else:
	if __name__ == '__main__':
		if '--help' in sys.argv:
			print USAGE
		else:
			main()
