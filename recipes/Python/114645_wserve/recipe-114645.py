#! /usr/bin/env python

import sys
import time
import random

from socket import *

cardinal = [ 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW' ]

template = """\
HTTP/1.0 200
Content-type : text/html

<html>
    <head>
        <title>Simon's weather station</title>
    </head>
    <body>
        <p><h1>Today's Weather</h1>
        <p><h2>Time: %s</h2>
        <p><h2>Wind Speed: %s knots</h2>
        <p><h2>Wind Direction: %s</h2>
        <p><h2>Temperature: %s deg C</h2>
        <p><h2>Rainfall: %s mm</h2>
    </body>
</html>
"""

port = 8080

def weather():
    # Simulate doing something
    time.sleep(1)
    ws 	= random.randrange( 0, 35 )
    wd 	= random.choice( cardinal )
    t 	= random.randrange( -5, 35 )
    r	= random.randrange( 0, 100 )
    now = time.ctime()
    return template % ( now, ws, wd, t, r )

sock = socket( AF_INET, SOCK_STREAM )
sock.bind(( '', port ))
sock.listen(5)
print 'Creating server:' , sock.getsockname()
while 1:
    newsock, address = sock.accept()
    print 'Client connection from: ', address
    print 'Got: ' + newsock.recv( 1024 )
    w = weather()
    print 'Sending: ' + w
    newsock.send( w )
    newsock.close()
