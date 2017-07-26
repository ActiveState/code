#!/usr/local/bin/python
# 31-08-04
#v1.0.0 

# cookie_example.py
# An example showing the usage of cookielib (New to Python 2.4) and ClientCookie

# Copyright Michael Foord
# You are free to modify, use and relicense this code.
# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# If you have any bug reports, questions or suggestions please contact me.
# If you would like to be notified of bugfixes/updates then please contact me and I'll add you to my mailing list.
# E-mail michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html

COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
import os.path

cj = None
ClientCookie = None
cookielib = None

try:                                    # Let's see if cookielib is available
    import cookielib            
except ImportError:
    pass
else:
    import urllib2    
    urlopen = urllib2.urlopen
    cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
    Request = urllib2.Request

if not cookielib:                   # If importing cookielib fails let's try ClientCookie
    try:                                            
        import ClientCookie 
    except ImportError:
        import urllib2
        urlopen = urllib2.urlopen
        Request = urllib2.Request
    else:
        urlopen = ClientCookie.urlopen
        cj = ClientCookie.LWPCookieJar()
        Request = ClientCookie.Request
        
####################################################
# We've now imported the relevant library - whichever library is being used urlopen is bound to the right function for retrieving URLs
# Request is bound to the right function for creating Request objects
# Let's load the cookies, if they exist. 
    
if cj != None:                                  # now we have to install our CookieJar so that it is used as the default CookieProcessor in the default opener handler
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)
    if cookielib:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)

# If one of the cookie libraries is available, any call to urlopen will handle cookies using the CookieJar instance we've created
# (Note that if we are using ClientCookie we haven't explicitly imported urllib2)
# as an example :

theurl = 'http://www.diy.co.uk'         # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
txdata = None                                                                           # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}          # fake a user agent, some websites (like google) don't like automated exploration

try:
    req = Request(theurl, txdata, txheaders)            # create a request object
    handle = urlopen(req)                               # and open it to return a handle on the url
except IOError, e:
    print 'We failed to open "%s".' % theurl
    if hasattr(e, 'code'):
        print 'We failed with error code - %s.' % e.code
else:
    print 'Here are the headers of the page :'
    print handle.info()                             # handle.read() returns the page, handle.geturl() returns the true url of the page fetched (in case urlopen has followed any redirects, which it sometimes does)

print
if cj == None:
    print "We don't have a cookie library available - sorry."
    print "I can't show you any cookies."
else:
    print 'These are the cookies we have received so far :'
    for index, cookie in enumerate(cj):
        print index, '  :  ', cookie        
    cj.save(COOKIEFILE)                     # save the cookies again
