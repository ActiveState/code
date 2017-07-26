#!/usr/bin/env python

"""File downloading from the web.
"""

def download(url):
	"""Copy the contents of a file from a given URL
	to a local file.
	"""
	import urllib
	webFile = urllib.urlopen(url)
	localFile = open(url.split('/')[-1], 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 2:
		try:
			download(sys.argv[1])
		except IOError:
			print 'Filename not found.'
	else:
		import os
		print 'usage: %s http://server.com/path/to/filename' % os.path.basename(sys.argv[0])
