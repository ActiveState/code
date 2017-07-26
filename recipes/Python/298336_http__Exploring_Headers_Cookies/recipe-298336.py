#!/usr/bin/python -u
# 18-08-04
# v1.1.1

# http.py
# A simple CGI script, to explore http headers, cookies etc.

# Copyright Michael Foord
# Free to use, modify and relicense.
# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail or michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html

"""
This CGI script allows you to specify a URL using an HTML form.
It will fetch the specified URL and print the headers from the server.
It will also handle cookies using ClientCookie - if it's available.

It is based on approx.py the CGI-proxy I'm building.
It includes authentication circuitry and I'm using it to understand http authentication.

This script shows using urllib2 to fetch a URL with a request object including User-Agent header and basic authentication.
It also shows the possible http errors - using a dictionary 'borrowed' from BaseHTTPServer
"""

################################################################
# Imports

try:
    import cgitb; cgitb.enable()
except:
    pass
import os, sys, cgi, pickle
from time import strftime
import urllib2

sys.stderr = sys.stdout

READSIZE = 4000
COOKIEFILE = 'cookies.lwp'

try:
    import ClientCookie
    openfun = ClientCookie.urlopen
    reqfun = ClientCookie.Request
    cj = ClientCookie.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)
    opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
    ClientCookie.install_opener(opener)
except:
    ClientCookie = None
    openfun = urllib2.urlopen
    reqfun = urllib2.Request


###############################################################
# Nicked from BaseHTTPServer
# This is the basic table of HTTP errors

errorlist = {   400: ('Bad Request',
                      'The Server thinks your request was malformed.'),
         401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this server.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
              'this proxy before proceeding.'),
        408: ('Request Time-out', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service temporarily overloaded',
              'The server cannot process the request due to a high load'),
        504: ('Gateway timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version not supported', 'Cannot fulfill request.')
                      }
################################################################
# Private functions and variables

SCRIPTNAME = os.environ.get('SCRIPT_NAME', '')                        # the name of the script
versionstring = '1.1.1 18th August, 2004.'
fontline = '<FONT COLOR=#424242 style="font-family:times;font-size:12pt;">'

METHOD = 'GET'
METHOD2 = 'POST'

def getform(valuelist, theform, notpresent=''):
    """This function, given a CGI form, extracts the data from it, based on
    valuelist passed in. Any non-present values are set to '' - although this can be changed.
    (e.g. to return None so you can test for missing keywords - where '' is a valid answer but to have the field missing isn't.)"""
    data = {}
    for field in valuelist:
        if not theform.has_key(field):
            data[field] = notpresent
        else:
            if  type(theform[field]) != type([]):
                data[field] = theform[field].value
            else:
                values = map(lambda x: x.value, theform[field])     # allows for list type values
                data[field] = values
    return data

errormess = "<H1>An Error Has Occurred</H1><BR><B><PRE>"

theformhead = """<HTML><HEAD><TITLE>http.py - Playing With Headers and Cookies</TITLE></HEAD>
<BODY><CENTER>
<H1>Welcome to http.py - <BR>a Python CGI</H1>
<B><I>By Fuzzyman</B></I><BR>
"""+fontline +"Version : " + versionstring + """, Running on : """ + strftime('%I:%M %p, %A %d %B, %Y')+'''.</CENTER>
<BR>'''

HR = '<BR><BR><HR><BR><BR>'

theform = """This CGI script allows you to specify a URL using the form below.<BR>
It will take a look at the specified URL and print the headers from the server.<BR>
It will also print the cookies which ought to be managed by the ClientCookie module.<BR>
<BR>
<H2>Enter the Location</H2>
<FORM METHOD=\"""" + METHOD + '" action="' + SCRIPTNAME + """\">
<input name=url type=text size=45 value=\"%s\" ><BR>
<input type=submit value="Submit"><BR>
</FORM>
<BR><BR><HR><BR><A href="http://www.voidspace.org.uk/atlantibots/pythonutils.html">Voidspace Pythonutils Page</A>
</BODY>
</HTML>
"""

authmess = """<HTML><HEAD><TITLE>Authentication Required</TITLE></HEAD>
<BODY><CENTER>
<H1>Authentication Required</H1>
<B><I>http.py By Fuzzyman</B></I><BR>
"""+fontline +"Version : " + versionstring + """, Running on : """ + strftime('%I:%M %p, %A %d %B, %Y')+'''.</CENTER><BR>
<BR>Please enter your username and password below.<BR>
<FORM METHOD=\"''' + METHOD2 + '" action="' + SCRIPTNAME + """\">Username : 
<input name="name" type=text><BR>Password : 
<input name="pass" type=password><BR>
<input type=hidden value="%s" name="theurl">
<input type=submit value="Submit">
<BR><BR>
"""


err_mess = """<HTML><HEAD><TITLE>%s</TITLE></HEAD>
<BODY><CENTER>
<H1>%s</H1>
<H2>%s</H2>
</CENTER>"""

################################################################
# main body of the script

if __name__ == '__main__':
    print "Content-type: text/html"         # this is the header to the server
    print                                   # so is this blank line
    form = cgi.FieldStorage()           
    data = getform(['url', 'name', 'pass', 'theurl'], form)
    print theformhead
    theurl = data['theurl'] or data['url']
    if not SCRIPTNAME: theurl = 'http://www.google.com/search?hl=en&ie=UTF-8&q=hello&btnG=Google+Search'
    info = 'An error occured before we got the headers.'
    e = ''
    if not theurl: 
        print theform % ''
    else:
        if theurl.find(':') == -1: theurl = 'http://' + theurl
        try:
            req = reqfun(theurl, None, {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
            if data['name'] and data['pass']:
                import base64
                base64string = base64.encodestring('%s:%s' % (data['name'], data['pass']))[:-1]
                req.add_header("Authorization", "Basic %s" % base64string)
            u = openfun(req)
            info = u.info()
        except Exception, e:                      # an error in fetching the page
            if not hasattr(e, 'code'):                  # Means the page doesn't exist 
                the_err = errorlist[404]
                print err_mess % (the_err[0], the_err[0], the_err[1])
                
            elif e.code  == 401:                        # authentication
                print authmess % (theurl)

            elif e.code in errorlist:                   # standard http errors
                the_err = errorlist[e.code]
                print err_mess % (the_err[0], the_err[0], the_err[1])
                
            else:                                       # any others (unknown error - shouldn't happen)
                raise         

        print HR
        print '<PRE>'
        print info
        print
        if e:                               # If an error has occurred - this ought to show the details
            print 'The Error : '
            print e
            print '\nAttributes of the python error object :'
            print dir(e)
            if hasattr(e, 'code'):
                print '\nThe Headers :' 
                print e.headers

        if ClientCookie:
            print
            print 'Cookies :'
            a = 0
            for c in cj:
                a += 1
                print a, c.__repr__()
        else:
            print
            print "ClientCookie isn't installed - so cookie stuff don't work !"

        print
        print 'Content (first', READSIZE, 'bytes) :'
        print u.read(READSIZE).replace('<', '&lt;')
        print '</PRE>'
        print HR
        print theform % theurl

        
        if ClientCookie:
            cj.save(COOKIEFILE)
            


            
"""
TODO/ISSUES
Work out what a realm is !


CHANGELOG
18-08-04        Version 1.1.0
Won't crash if ClientCookie isn't available.

12-08-04        Version 1.1.0
Added support for ClientCookie
Now displays the first 4000 bytes of content too.
My birthday.

02-08-04        Version 1.0.0
My first wedding anniversary.
"""
