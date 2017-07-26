#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re
import sys
def check_server(address, port):
	# Create a TCP socket
	s = socket.socket()
	print "Attempting to connect to %s on port %s" % (address, port)
	try:
		s.connect((address, port))
		print "Connected to %s on port %s" % (address, port)
		return True
	except socket.error, e:
		print "Connection to %s on port %s failed: %s" % (address, port, e)
		return False

if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser()
	
	parser.add_option("-a", "--address", dest="address", default='localhost', help="ADDRESS for server", metavar="ADDRESS")
	
	parser.add_option("-p", "--port", dest="port", type="int", default=80, help="PORT for server", metavar="PORT")
	
	(options, args) = parser.parse_args()
	print 'options: %s, args: %s' % (options, args)
	check = check_server(options.address, options.port)
	print 'check_server returned %s' % check
	
	sys.exit(not check)
