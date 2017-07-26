# puts a 'Hello, World!' file at http://myserver.com/dav/testfile

import httplib
dav_server = httplib.HTTPConnection('myserver.com')
dav_server.request('PUT', '/dav/testfile', 'Hello, World!')
dav_response = dav_server.getresponse()
dav_server.close()
if not (200 <= dav_response.status < 300):
	raise Exception(dav_response.read())
