#!/usr/bin/env python
"""
 $watch.py$ <4:41 PM 5/1/04>
 Watch That Post!
 A simple Python script to "watch" a post. I wrote this to
 watch posts on LiveJournal, but actually you can use it
 to watch any URL.

 Copyright (C) 2004 Premshree Pillai. All rights reserved.
 <http://www.qiksearch.com/>
 <http://www.livejournal.com/~premshree>

 To use the script:
	1. Create a file (e.g., urls.txt) and add the URLs
	   you want to watch - each URL on a new line.
	2. Change the variable period to whatever seconds
	   you want to let the script sleep.
	3. Run the program: python watch.py
"""

import urllib
import re
import sys
import time

def watch():
	urls = "urls.txt" # change this to whatever you want
	separator = " "
	change = 0
	try:
		fp = open(urls,"r")
	except IOError:
		fp = open(urls,"w")
		fp.close()
		sys.exit(0)

	urls_lines = fp.readlines()
	orig_content = ""
	count = 0
	for x in urls_lines:
		orig_content = orig_content + x
	fp.close()

	if len(urls_lines) == 0:
		sys.exit(0)

	rewrite_content = ""
	count = 0
	for url_line in urls_lines:
		url_and_size = re.split(" ", url_line)
		if len(url_and_size) == 1:
			url_and_size = re.split("\n", url_and_size[0])
			rewrite_content = rewrite_content + url_and_size[0] + separator + "0"
			change = 1
		else:
			url = url_and_size[0]
			size = url_and_size[1]
			size2 = len(urllib.urlopen(url).readlines())
			if int(size) != size2:
				print "New comment: " + url
				rewrite_content = rewrite_content + url + separator + str(size2)
				change = 1
			else:
				rewrite_content = rewrite_content + url_line
		#if count < len(urls_lines) - 1:
		#	rewrite_content = rewrite_content + "\n"
		count = count + 1

	if change == 1:
		fp = open(urls,"w")
		fp.write(rewrite_content)
		fp.close()

period = 100 # time in seconds...change it to whatever you want
while 1:
	watch()
	time.sleep(period)
