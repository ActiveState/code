#!/usr/bin/python
# -*- encoding:utf-8 -*-

"""Translate Google's Transcript into srt file.

Takes google's transcript filename as argument (xml extension required).

NB: to get google's transcript, use tihs URL:
http://video.google.com/timedtext?lang=en&v=VIDEO_ID
"""

# srt example
"""1
00:00:20,672 --> 00:00:24,972
Entre l’Australia et la South America,
dans l’Océan South Pacific…"""

# Google's transcript example (first tags)
"""<?xml version="1.0" encoding="utf-8" ?>
<transcript>
<text start="11.927" dur="2.483">
This is a matter of National Security.</text>"""

import re, sys

# Pattern to identify a subtitle and grab start, duration and text.
pat = re.compile(r'<?text start="(\d+\.\d+)" dur="(\d+\.\d+)">(.*)</text>?')

def parseLine(text):
	"""Parse a subtitle."""
	m = re.match(pat, text)
	if m:
		return (m.group(1), m.group(2), m.group(3))
	else:
		return None

def formatSrtTime(secTime):
	"""Convert a time in seconds (google's transcript) to srt time format."""
	sec, micro = str(secTime).split('.')
	m, s = divmod(int(sec), 60)
	h, m = divmod(m, 60)
	return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)

def convertHtml(text):
	"""A few HTML encodings replacements.
	&amp;#39; to '
	&amp;quot; to "
	"""
	return text.replace('&amp;#39;', "'").replace('&amp;quot;', '"')

def printSrtLine(i, elms):
	"""Print a subtitle in srt format."""
	return "{}\n{} --> {}\n{}\n\n".format(i, formatSrtTime(elms[0]), formatSrtTime(float(elms[0])+float(elms[1])), convertHtml(elms[2]))

fileName = sys.argv[1]

def main(fileName):
	"""Parse google's transcript and write the converted data in srt format."""
	with open(sys.argv[1], 'r') as infile:
		buf = []
		for line in infile:
			buf.append(line.rstrip('\n'))
	# Split the buffer to get one string per tag.
	buf = "".join(buf).split('><')
	i = 0
	srtfileName = fileName.replace('.xml', '.srt')
	with open(srtfileName, 'w') as outfile:
		for text in buf:
			parsed = parseLine(text)
			if parsed:
				i += 1
				outfile.write(printSrtLine(i, parsed))
	print('DONE ({})'.format(srtfileName))

if __name__ == "__main__":
	main(fileName)
