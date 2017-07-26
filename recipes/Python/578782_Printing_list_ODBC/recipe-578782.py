#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: odbc_sources.py 1696 2013-12-10 11:03:08Z mn $'

# shows ODBC data sources with driver info

# author: Michal Niklas

import odbc


def show_odbc_sources():
	sl = []
	source = odbc.SQLDataSources(odbc.SQL_FETCH_FIRST)
	while source:
		dsn, driver = source
		sl.append('%s [%s]' % (dsn, driver))
		source = odbc.SQLDataSources(odbc.SQL_FETCH_NEXT)
	sl.sort()
	print('\n'.join(sl))


if __name__ == '__main__':
	show_odbc_sources()
