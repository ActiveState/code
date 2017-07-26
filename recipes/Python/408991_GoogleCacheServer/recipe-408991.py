# 2005/04/05
# v0.1.3
# googleCacheServer.py

# A simple proxy server that fetches pages from the google cache.

# Homepage : http://www.voidspace.org.uk/python/index.html

# Copyright Michael Foord, 2004 & 2005.
# Released subject to the BSD License
# Please see http://www.voidspace.org.uk/documents/BSD-LICENSE.txt

# For information about bugfixes, updates and support, please join the Pythonutils mailing list.
# http://voidspace.org.uk/mailman/listinfo/pythonutils_voidspace.org.uk
# Comments, suggestions and bug reports welcome.
# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# E-mail fuzzyman@voidspace.org.uk

"""
This is a simple implementation of a proxy server that fetches web pages
from the google cache.

It is based on SimpleHTTPServer.

It lets you explore the internet from your browser, using the google cache.
See the world how google sees it.

Alternatively - retro internet - no CSS, no javascript, no images, this is back to the days of MOSAIC !

Run this script and then set your browser proxy settings to localhost:8000

Needs google.py (and a google license key).
See http://pygoogle.sourceforge.net/
and http://www.google.com/apis/

Tested on Windows XP with Python 2.3 and Firefox/Internet Explorer
Also reported to work with Opera/Firefox and Linux

Because the google api will only allow 1000 accesses a day we limit the file types
we will check for.

A single web page may cause the browser to make *many* requests.
Using the 'cached_types' list we try to only fetch pages that are likely to be cached.

We *could* use something like scraper.py to modify the HTML to remove image/script/css URLs instead.

Some useful suggestions and fixes from 'vegetax' on comp.lang.python
"""

import google
import BaseHTTPServer
import shutil
from StringIO import StringIO       # cStringIO doesn't cope with unicode
import urlparse


__version__ = '0.1.0'

cached_types = ['txt', 'html', 'htm', 'shtml', 'shtm', 'cgi', 'pl', 'py'
                'asp', 'php', 'xml']
# Any file extension that returns a text or html page will be cached
google.setLicense(google.getLicense())
googlemarker = '''<i>Google is not affiliated with the authors of this page nor responsible for its content.</i></font></center></td></tr></table></td></tr></table>\n<hr>\n'''
markerlen = len(googlemarker)

import urllib2 
# uncomment the next three lines to over ride automatic fetching of proxy settings
# if you set localhost:8000 as proxy in IE urllib2 will pick up on it
# you can specify an alternate proxy by  passing a dictionary to ProxyHandler
##proxy_support = urllib2.ProxyHandler({}) 
##opener = urllib2.build_opener(proxy_support) 
##urllib2.install_opener(opener) 

class googleCacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "googleCache/" + __version__
    cached_types = cached_types
    googlemarker = googlemarker
    markerlen = markerlen
    txheaders = { 'User-agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)' }
    
    def do_GET(self):
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def send_head(self):
        """Only GET implemented for this.
        This sends the response code and MIME headers.
        Return value is a file object, or None.
        """
        print 'Request :', self.path # traceback to sys.stdout
        url_tuple = urlparse.urlparse(self.path)
        url = url_tuple[2]
        domain = url_tuple[1]
        if domain.find('.google.') != -1:   # bypass the cache for google domains
            req = urllib2.Request(self.path, None, self.txheaders)
            self.send_response(200) 
            self.send_header("Content-type", 'text/html') 
            self.end_headers()
            return urllib2.urlopen(req)
        
        dotloc = url.rfind('.') + 1
        if dotloc and url[dotloc:] not in self.cached_types:
            return None     # not a cached type - don't even try

        print 'Fetching :', self.path # traceback to sys.stdout
        thepage = google.doGetCachedPage(self.path) # XXXX should we check for errors here ?
        headerpos = thepage.find(self.googlemarker)
        if headerpos != -1:
            pos = self.markerlen + headerpos
            thepage = thepage[pos:]
            
        f = StringIO(thepage)       # turn the page into a file like object

        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.send_header("Content-Length", str(len(thepage)))
        self.end_headers()
        return f
    
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)


def test(HandlerClass = googleCacheHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
