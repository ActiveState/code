#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011 (C) by Rémi Thebault <remi.thebault - at - gmail - dot - com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys
import os
from optparse import OptionParser
from fnmatch import fnmatch



usage = '''
   linecount.py [Options] Targets
   
      Targets must be list of valid files or directories
	
   Ex for a C++ project :
      linecount.py --exts="h cc" --excludes="*build*" myprojectroot'''


sh_exts = 'sh py pl rb'.split()
c_exts = 'h hpp c cc cpp cxx java cs'.split()
m_exts = 'm'.split()

# the few following lines will try to fetch terminal width for better output
# 	1st try for POSIX systems (Linux, MacOSX)
#	2nd try for MS systems
# if failure, defaults to 80
termwidth = 80
try:
	import fcntl, termios, struct
	cr = struct.unpack('hh', fcntl.ioctl(sys.stdout.fileno(),
			termios.TIOCGWINSZ, '1234'))
	(h, termwidth) = cr
except:
	try:
		from ctypes import windll, create_string_buffer
		# stdin handle is -10
		# stdout handle is -11
		# stderr handle is -12
		h = windll.kernel32.GetStdHandle(-11)
		csb = create_string_buffer(22)
		res = windll.kernel32.GetConsoleScreenBufferInfo(h, csb)
		if res:
			import struct
			(bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx,
							maxy) = struct.unpack("hhhhHhhhhhh", csb.raw)
			termwidth = right - left + 1
	except:
		pass


# some output formatting utility
defaultFmtTag = '\033[0m'
boldFmtTag = '\033[1;1m'
redFmtTag = '\033[91m'
greenFmtTag = '\033[92m'

def boldFmt(str, closeTag=defaultFmtTag):
	return boldFmtTag + str + closeTag

def greenFmt(str, closeTag=defaultFmtTag):
	return greenFmtTag + str + closeTag

def redFmt(str, closeTag=defaultFmtTag):
	return redFmtTag + str + closeTag


def errorMsg(mes):
	sys.stderr.write(boldFmt(redFmt('Error: ' + mes)) + '\n')




def getExt(file):
	(root, ext) = os.path.splitext(file)
	if len(ext) > 0:
		return ext[1:]
	return ''


def fileMatches(file, options):
	if options.excludes:
		for exc in options.excludes:
			if fnmatch(file, exc):
				return False
	if options.syntax:
		return True
	ext = getExt(file)
	if options.exts:
		if ext in options.exts:
			if ext in sh_exts or ext in c_exts or ext in m_exts:
				return True
	else:
		return True
	return False


def doCFile(file):
	count = 0
	f = open(file, 'r')
	
	incomment = False
	
	for line in f:
		line = line.strip()
		if incomment:
			end = line.find('*/')
			if end < 0:
				continue
			else:
				incomment = False
				line = line[end+2:]
		if len(line) == 0:
			continue
		if line.startswith('//'):
			continue
		ind = line.find('/*')
		if ind >= 0:
			incomment = True
			ind2 = line[ind+2:].find('*/') >= 0
			if ind2 >= 0:
				incomment = False
			if ind > 0 or ind2 < len(line)-2:
				count += 1
			continue
		count += 1
	return count


def doRegularFile(file, cmtStr):
	count = 0
	f = open(file, 'r')
	for line in f:
		line = line.strip()
		if len(line) > 0 and not line.startswith(cmtStr):
			count += 1
	return count


def doShFile(file):
	return doRegularFile(file, '#')


def doMFile(file):
	return doRegularFile(file, '%')



formatstr = '{0:.<' + str(termwidth-11) + '}' + boldFmt(greenFmt('{1:>5d} lines'))
filecount = 0

def doFile(file, options):
	global formatstr
	global filecount
	if options.syntax:
		if options.syntax == 'S':
			count = doShFile(file)
		elif options.syntax == 'C':
			count = doCFile(file)
		elif options.syntax == 'M':
			count = doMFile(file)
	else:
		ext = getExt(file)
		count = 0
		if ext in sh_exts:
			count = doShFile(file)
		elif ext in c_exts:
			count = doCFile(file)
		elif ext in m_exts:
			count = doMFile(file)
	
	print formatstr.format(file, count)
	filecount += 1
	return count


def doDir(dir, options):
	files = sorted(os.listdir(dir))
	count = 0
	for file in files:
		fname = os.path.join(dir, file)
		if os.path.islink(fname):
			continue
		if os.path.isdir(fname) and options.recurs:
			count += doDir(fname, options)
		elif fileMatches(fname, options):
			count += doFile(fname, options)
	return count


if __name__ == '__main__':
	
	parser = OptionParser(usage)
	parser.add_option('-e', '--exts', dest='exts', action='store',
			help='list of extensions of files to be parsed (mandatory if a dir '
			+ ' is in targets')
	parser.add_option('-x', '--excludes', dest='excludes', action='store',
			help='Blob syntax list of files to be excluded from count '
			'(only useful when parsing dirs)')
	parser.add_option('-s', '--syntax', dest='syntax', action='store',
			help='Force parsing mode to the given syntax ' +
			'(S: Shell-style, C: C-style, M: Matlab-style). If not specified, '
			'syntax is based on file extension')
	parser.add_option('-r', '--non-recursive', dest='recurs',
			action='store_false', default=True,
			help='Do not enter subdirectories recursively')
	
	(options, args) = parser.parse_args()
	
	if len(args) == 0:
		parser.print_help()
		errorMsg('you must specify a destination')
		sys.exit(1)
	
	args = sorted(args)
	for dest in args:
		if os.path.exists(dest) and os.path.isdir(dest):
			if not options.exts:
				parser.print_help()
				errorMsg('option ' + greenFmt('-e', redFmtTag) + ' or ' +
						 greenFmt('--exts', redFmtTag) + ' is needed')
				sys.exit(1)
			break
	
	if options.exts:
		options.exts = options.exts.split()
	if options.excludes:
		options.excludes = options.excludes.split()
	if options.syntax:
		if not options.syntax in 'S C M'.split():
			parser.print_help()
			errorMsg('accepted values for ' + greenFmt('--syntax', redFmtTag) + ' are:\n' +
					 '     S     for shell-style\n' +
					 '     C     for C-style\n' +
					 '     M     for matlab-style')
			sys.exit(1)
	
	count = 0
	err = 0
	printresume = len(args) > 1
	
	for dest in args:
		if os.path.exists(dest):
			if os.path.isdir(dest):
				c = doDir(dest, options)
				if len(args)>1:
					print repr(c) + ' lines of code in ' + dest
				count += c
				printresume = True
			elif os.path.isfile(dest):
				if fileMatches(dest, options):
					count += doFile(dest, options)
				else:
					errorMsg('file ' + dest + ' doesn\'t match your options')
					err += 1
		else:
			errorMsg('target ' + dest + ' is not valid')
			err += 1
	
	if err == 0 or count > 0:
		if printresume:
			resume = 'total count : ' + repr(count) + ' line'
			if count > 1:
				resume += 's'
			resume += ' of code in ' + repr(filecount)+ ' file'
			if filecount > 1:
				resume += 's'
			print boldFmt(greenFmt(resume))
	else:
		parser.print_help()
		errorMsg('Aborting because of errors')
		sys.exit(1)
	
	sys.exit(0)
