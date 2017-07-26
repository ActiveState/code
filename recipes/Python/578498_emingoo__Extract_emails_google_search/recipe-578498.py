#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Name: emingoo.py
# Version: 1.0
# Author: pantuts
# Description: Extract emails from Google search results.
# Agreement: You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv3).
# This tool is for educational purposes only. Any damage you make will not affect the author.

import sys, re, time
from urllib.request import Request, urlopen
import urllib.error

def helper():
	print('Usage:./emingoo.py -d domainToSearch -c maxResults[int]')
	print('Default min google search result is 100 and max is 10000.')
	print()

def extract(res, d):
	em_sub = re.sub('<[^<]+?>', '', res) # strip all html tags like <em>
	tmp_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+' + d, em_sub)
	tmp_emails1 = re.findall(r'[a-zA-Z0-9._%+-]+@' + d, em_sub)
	tmp_emails2 = set(tmp_emails + tmp_emails1)
	emails = [x for x in tmp_emails2]
	if len(emails) == 0: print('Sorry, no results found.')
	else:
		for i in emails: print(i); time.sleep(0.01)
	print()

def crawl(d, c):
	if c > 10000:
		print('Sorry your argument -c exceeded on its max search result.')
		sys.exit(0)
	print('Searching emails for ' + d + ' ...')
	print()
	try:
		q = 'http://www.google.com/search?hl=en&num=' + str(c) + '&q=intext%3A%40' + d + '&ie=utf-8'
		req = Request(q)
		req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0')
		res = urlopen(req).read().decode('utf-8')
	except (urllib.error.URLError, urllib.error.HTTPError) as e:
		print(e)
		sys.exit(1)

	extract(res, d)

def main():
	if len(sys.argv) < 3 or len(sys.argv) > 5:
		helper()
		sys.exit(0)
	else:
		if len(sys.argv) == 5:
			domain = sys.argv[2]
			max_res = int(sys.argv[4])
		elif len(sys.argv) == 3:
			domain = sys.argv[2]
			max_res = 100
		else:
			helper()
			sys.exit(0)

	crawl(domain, max_res)

if __name__=='__main__':
	print(' ____  __  __  ____  _  _  ___  _____  _____ ')
	print('( ___)(  \/  )(_  _)( \( )/ __)(  _  )(  _  )')
	print(' )__)  )    (  _)(_  )  (( (_-. )(_)(  )(_)( ')
	print('(____)(_/\/\_)(____)(_)\_)\___/(_____)(_____)')
	print()
	try:
		main()
	except KeyboardInterrupt:
		print('\rKeyboardInterrupt')
		sys.exit(0)
