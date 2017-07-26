#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '$Id: binclock_bcd_curses.py 780 2010-10-19 10:33:34Z mn $'

# binary clock, bcd version
# author: Michal Niklas

import sys
import time
import curses

def bin_old(n):
	"""bin() that works with Python 2.4"""
	if n < 1:
		return '0'
	result = []
	while n:
		if n % 2:
			result.append('1')
		else:
			result.append('0')
		n = n // 2
	result.reverse()
	return ''.join(result)


def bcd_digit(sn):
	"""converts decimal digit char to 4 char binary 0 and 1 representation"""
	n = int(sn)
	try:
		bin_nr = bin(n)[2:]
	except NameError:
		bin_nr = bin_old(n)
	return ('0000' + bin_nr)[-4:]


def add_bcd(n, digits):
	"""add n binary digits to digits"""
	nn = "%02d" % (n)
	digits.append(bcd_digit(nn[0]))
	digits.append(bcd_digit(nn[1]))


def get_stars(digits):
	"""changes digits to vertical picture of clock with stars and dots"""
	digits_arr = []
	for j in range(len(digits[0]) - 1, -1, -1):
		digits2 = []
		for i in range(len(digits)):
				digits2.append(digits[i][j])
		digits_arr.append(''.join(digits2))
	digits_arr.reverse()
	stars = "\n".join(digits_arr)
	stars = stars.replace('0', '.')
	stars = stars.replace('1', '*')
	return stars


def main():
	try:
		try:
			window = curses.initscr()
			while 1:
				digits = []
				window.clear()
				tm = time.localtime()
				add_bcd(tm.tm_hour, digits)
				add_bcd(tm.tm_min, digits)
				add_bcd(tm.tm_sec, digits)
				stars = get_stars(digits)
				line_nr = 0
				for line in stars.split('\n'):
					window.addstr(line_nr, 0, line[:6])
					line_nr += 1
				window.refresh()
				time.sleep(0.5)
		except KeyboardInterrupt:
			pass
	finally:
		# reset terminal
		curses.nocbreak()
		curses.echo()
		curses.endwin()


if '--version' in sys.argv:
	print(__version__)
elif __name__ == '__main__':
	main()
