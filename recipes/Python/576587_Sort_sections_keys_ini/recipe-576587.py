#!/usr/bin/python
# -*- coding: cp1250 -*-
__version__ = '$Id: sort_ini.py 543 2008-12-19 13:44:59Z mn $'

# author: Michal Niklas

import sys

USAGE = 'USAGE:\n\tsort_ini.py file.ini'

def sort_ini(fname):
	"""sort .ini file: sorts sections and in each section sorts keys"""
	f = file(fname)
	lines = f.readlines()
	f.close()
	section = ''
	sections = {}
	for line in lines:
		line = line.strip()
		if line:
			if line.startswith('['):
				section = line
				continue
			if section:
				try:
					sections[section].append(line)
				except KeyError:
					sections[section] = [line, ]
	if sections:
		sk = sections.keys()
		sk.sort()
		for k in sk:
			vals = sections[k]
			vals.sort()
			print k
			print '\n'.join(vals)
			print


if '--version' in sys.argv:
	print __version__
elif len(sys.argv) < 2:
	print USAGE
else:
	sort_ini(sys.argv[1])
