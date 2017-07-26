# create a unique session id
# input - string to use as part of the data used to create the session key.
#         Although not required, it is best if this includes some unique 
#         data from the site, such as it's IP address or other environment 
#         information.  For ZOPE applications, pass in the entire ZOPE "REQUEST"
#         object.
def makeSessionId(st):
	import md5, time, base64
	m = md5.new()
	m.update('this is a test of the emergency broadcasting system')
	m.update(str(time.time()))
	m.update(str(st))
	return string.replace(base64.encodestring(m.digest())[:-3], '/', '$')
