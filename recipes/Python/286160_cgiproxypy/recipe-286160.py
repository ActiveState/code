#!/usr/bin/python

# v0.01

# cgiproxy.py

# Copyright Michael Foord
# Not for use in commercial projects without permission. (Although permission will probably be given).
# If you use this code in a project then please credit me and include a link back.
# If you release the project then let me know (and include this message with my code !)

# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail or michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html

import sys
import cgi
import urllib2

sys.stderr = sys.stdout

HOMEPAGE = 'www.google.co.uk'

######################################################

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


def pagefetch(thepage):
    req = urllib2.Request(thepage)
    u = urllib2.urlopen(req)
    data = u.read()
    return data

        
        
###################################################

if __name__ == '__main__':
    form = cgi.FieldStorage()           
    data = getform(['url'],form)
    if not data['url']: data['url'] = HOMEPAGE
    print "Content-type: text/html"         # this is the header to the server
    print                                   # so is this blank line
    test = pagefetch('http://' + data['url'])
    print test
    
