#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: pyodbc_sources.py 1736 2014-01-28 10:36:41Z mn $'

# shows ODBC data sources with driver info

# author: Michal Niklas

import pyodbc


def show_odbc_sources():
	sources = pyodbc.dataSources()
	dsns = sources.keys()
	dsns.sort()
	sl = []
	for dsn in dsns:
		sl.append('%s [%s]' % (dsn, sources[dsn]))
	print('\n'.join(sl))


if __name__ == '__main__':
	show_odbc_sources()
