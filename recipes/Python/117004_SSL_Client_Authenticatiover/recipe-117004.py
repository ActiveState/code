#!/usr/bin/env python

import httplib

CERTFILE = '/home/robr/mycert'
HOSTNAME = 'localhost'

conn = httplib.HTTPSConnection(
	HOSTNAME,
	key_file = CERTFILE,
	cert_file = CERTFILE
)
conn.putrequest('GET', '/ssltest/')
conn.endheaders()
response = conn.getresponse()
print response.read()
