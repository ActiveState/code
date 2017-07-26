###Easy testing of CGI scripts

Originally published: 2008-03-06 12:03:59
Last updated: 2016-11-01 02:27:13
Author: Bryan Olson

Invoking 'runcgi.py target.cgi' starts a built-in web server listening on the localhost adapter, configures the server to run target.cgi as a CGI program, then launches the system's default web browser to get the URL of the target script. The CGI script need not be in Python. The terminal that launched runcgi.py will show the server's log, which reports requests, responses, and errors.