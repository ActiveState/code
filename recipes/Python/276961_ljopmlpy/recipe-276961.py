#!/usr/bin/env python
###############################################
##
## ljopml.py <3:58 AM 3/27/04>
## By Premshree Pillai, (C) 2004
## http://www.qiksearch.com/
##
###############################################

import urllib
import cgi
import re

form = cgi.FieldStorage()
if form :
	user = form['user'].value
else :
	print "Content-type:text/html\n\n";
	print """<html>
<head>
	<title>Generate OPML</title>
	<style type="text/css">
	body	{font-family:trebuchet ms,arial,verdana,helvetica; font-size:10pt; text-align:justify}
	a	{text-decoration:underline; font-weight:bold}
	a:hover {background:#CCCCFF; text-decoration:none; font-weight:bold}</style>
</head>
<body>
<h3>Generate an OPML Feed of your LiveJournal Friends list</h3>
<form method="get" action="ljopml.py">
LJ Username: <input type="text" name="user">
<input type="submit" value="Generate OPML">
</form>
By <a href="http://www.livejournal.com/userinfo.bml?user=premshree"><img src="../lj_userinfo.gif" style="vertical-align:bottom; border:0" alt="[info]"></a><a href="http://www.livejournal.com/users/premshree">premshree</a>
</body>
</html>"""

def process():
	url = "http://www.livejournal.com/users/" + user + "/data/foaf"
	try:
		fp = urllib.urlopen(url)
	except IOError:
		print "Content-type:text/html\n\n"
		print "<h1>Error accessing FOAF URL!</h1>"
	url_data = fp.read()
	fp.close()
	print "Content-type:text/xml\n\n"
	print """<?xml version="1.0" encoding="utf-8"?>
<opml version="1.0">
<head>
	<title>LiveJournal Subsriptions</title>
	<dateCreated>GMT</dateCreated>
</head>
<body>
    <outline title="Subscriptions">"""
	
	content = re.split("<foaf:Person>",url_data)
	count = 0
	for x in content :
		m = re.match("[ \t\n]*<foaf:nick>([ \t\w\n]*)",x)
		if m != None :
			if count != 1 :
				rep = m.group(1)
				print "<outline title=\"" + rep + "\" htmlUrl=\"http://www.livejournal.com/users/" + rep + "/\" type=\"rss\" xmlUrl=\"http://www.livejournal.com/users/" + rep + "/data/rss\" />\n";
		count = count + 1
	print "</outline></body></opml>"

if form :
	process()
