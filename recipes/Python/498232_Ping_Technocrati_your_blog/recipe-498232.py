#!/usr/bin/python
#
# Written by Mayuresh at gmail dot com
#
# This program posts a blog URL to the Technorati ping server

import xmlrpclib
import socket
import sys
from optparse import OptionParser

TECHNORATI_RPC_PING_SERVER = 'http://rpc.technorati.com/rpc/ping'

usage = """ %prog Blog_name Blog_URL

        Example: %prog YourBlogName http://www.YOURWEBLOGURL.com/
        """
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()

if len(args) != 2:
        parser.error("Invalid options")

print "Submitting the following blog info to %s" % TECHNORATI_RPC_PING_SERVER
print
print "Blog name: %s" % args[0]
print "Blog URL: %s" % args[1]
print
print "Waiting for server response ..."
print

reply = {}

try:
        s = xmlrpclib.Server(TECHNORATI_RPC_PING_SERVER)
        reply = s.weblogUpdates.ping(args[0], args[1])

except socket.error, msg:
        reply['flerror'] = True
        errCode, reply['message'] = msg

except xmlrpclib.ProtocolError, inst:
        reply['flerror'] = True
        reply['message'] = "Error [%s: %s] occured while accesing url %s" %(inst.errcode, inst.errmsg, inst.url)

except xmlrpclib.Fault, inst:
        reply['flerror'] = True
        reply['message'] = inst.faultString

except:
        reply['flerror'] = True
        reply['message'] = "Unknown error occured"

if reply['flerror']:
        print "The server returned an error"
else:
        print "The server returned success"

print
print "Message from the server: %s" % reply['message']

if reply['flerror']:
        sys.exit(1)
else:
        sys.exit()
