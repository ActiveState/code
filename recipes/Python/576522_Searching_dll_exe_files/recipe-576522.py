#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: which_dll.py 2247 2014-10-06 09:19:53Z mn $'

r"""
Returns the pathnames of the file (.exe or .dll)
which would be loaded/executed in the current environment
it uses some dirs from configuration (SystemDir, WindowsDir)
and dirs from PATH.

To obtain version info it uses code from:
http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/file/tip/win32/Demos/getfilever.py

Example of usage:
c:\tools\pyscripts\scripts>which_dll.py libpq.dll
2008-06-09 02:58:26	  167936 [b]	c:\postgresql\8.3\bin\libpq.dll	ver:8.3.3.8160
2008-03-17 01:47:50	  167936 [b]	c:\tools\libpq.dll	ver:8.3.1.8075
2008-03-17 01:47:50	  167936 [b]	g:\public\libpq.dll	ver:8.3.1.8075
	trying to load "libpq.dll" ...
	c:\postgresql\8.3\bin\libpq.dll loaded

Author: Michal Niklas
"""

USAGE = 'Usage:\n\twhich_dll.py dll_name/exe_name'

import sys
import time
import os
import os.path
import win32api


def get_file_ver(fname):
	# see: http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/file/tip/win32/Demos/getfilever.py
	result = []
	try:
		ver_strings = ('ProductVersion', 'FileVersion')
		pairs = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')
		## \VarFileInfo\Translation returns list of available (language, codepage) pairs that can be used to retreive string info
		## any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle two are language/codepage pair returned from above
		for lang, codepage in pairs:
			#print 'lang: ', lang, 'codepage:', codepage
			for ver_string in ver_strings:
				str_info = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, ver_string)
				result.append('%s %s' % (ver_string, win32api.GetFileVersionInfo(fname, str_info).strip()))
	except:
		pass
	return result


def get_file_info(file_path):
	"""returns string with file name, its modification time and size"""
	s = os.stat(file_path)
	f_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(s[8]))
	f_size = s[6]
	fv = ''
	ver_info = get_file_ver(file_path)
	if ver_info:
		fv = '\t%s' % ('; '.join(ver_info))
	return "%s\t%8s [b]\t%s%s" % (f_date, f_size, file_path, fv)


def which(fname):
	"""searches fname in PATH dirs"""
	if not which_file(fname):
		if '.' not in fname:
			# no extension, so we try some "executable" extensions
			for ext in ('.exe', '.com', '.bat', '.cmd'):
				fname2 = fname + ext
				if which_file(fname2):
					break


def which_file(fname):
	"""prints paths for fname where fname can be found,
	in case of .dll loads it"""
	files = []
	path = win32api.GetEnvironmentVariable('PATH')
	# try paths as described in MSDN
	dirs = [os.getcwd(), win32api.GetSystemDirectory(), win32api.GetWindowsDirectory()] + path.split(';')
	dirs_norm = []
	dirs_l = []
	for d in dirs:
		dn = d.lower()
		if dn not in dirs_l:
			dirs_l.append(dn)
			dirs_norm.append(d)
	for d in dirs_norm:
		fname2 = os.path.join(d, fname)
		if os.path.exists(fname2):
			if fname2 not in files:
				files.append(fname2)
	if files:
		print('\n'.join([get_file_info(f) for f in files]))
	h = 0
	if fname.lower().endswith('.dll'):
		print('\ttrying to load "%s" ...' % (fname))
		try:
			h = win32api.LoadLibrary(fname)
			if h:
				dll_name = win32api.GetModuleFileName(h)
				print('\t%s loaded' % (dll_name))
		except:
			print('\tCannot load "%s" !!!' % (fname))


def main():
	if '--version' in sys.argv:
		print(__version__)
		return
	elif '--help' in sys.argv:
		print(USAGE)
		return
	elif '--test' in sys.argv:
		which('libpq.dll')
		which('libeay32.dll')
		which('msvcr71.dll')
		which('ssleay32.dll')
		which('cmd.exe')
		which('grep')
		which('iclit09b.dll')
		which('non_existient.dll')
		return
	if len(sys.argv) < 2:
		print(USAGE)
	else:
		which(sys.argv[1])


main()
