# I wanted to touch a particular web page (in order to open/
# close a database connection inside of Zope) so I came
# up with this module which uses urllib2 to make the
# web connection
#
# I was not sure what a 'realm' was, so first I made the
# HTTPRealmFinder to find out what the realm is.
# The HTTPinger calls my required page and acts according
# to the http return code.


import urllib2
from urlparse import urlparse


class HTTPinger:
    def ping(self, url, webuser, webpass):
        scheme, domain, path, x1, x2, x3 = urlparse(url)
        
        finder = HTTPRealmFinder(url)
        realm = finder.get()
        
        handler = urllib2.HTTPBasicAuthHandler()
        handler.add_password(realm, domain, webuser, webpass)
        
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            if e.code == 401:
                print 'not authorized'
            elif e.code == 404:
                print 'not found'
            elif e.code == 503:
                print 'service unavailable'
            else:
                print 'unknown error: '
        else:
            print 'success'


class HTTPRealmFinderHandler(urllib2.HTTPBasicAuthHandler):
    def http_error_401(self, req, fp, code, msg, headers):
        realm_string = headers['www-authenticate']
        
        q1 = realm_string.find('"')
        q2 = realm_string.find('"', q1+1)
        realm = realm_string[q1+1:q2]
        
        self.realm = realm

        
class HTTPRealmFinder:
    def __init__(self, url):
        self.url = url
        scheme, domain, path, x1, x2, x3 = urlparse(url)
        
        handler = HTTPRealmFinderHandler()
        handler.add_password(None, domain, 'foo', 'bar')
        self.handler = handler
        
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

    def ping(self, url):
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            pass

    def get(self):
        self.ping(self.url)
        try:
            realm = self.handler.realm
        except AttributeError:
            realm = None
        
        return realm

    def prt(self):
        print self.get()

if __name__ == '__main__':
    pinger = HTTPinger()
    pinger.ping('https://example.com/nonexistent/path', 'username', 'password')
    pinger = HTTPinger()
    pinger.ping('https://example.com/basic/auth/protected/path', 'username', 'password')

    finder = HTTPRealmFinder('https://example.com/basic/auth/protected/path')
    finder.prt()
