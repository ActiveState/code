#!/usr/bin/env python

#  runcgi.py by Bryan Olson
#  This Python program is free software. You may use it, distribute it,
#  and/or modify it under the same terms as Python itself.

"""
    Tests a cgi script, by launching a simple web server and sending the
    default browser to the target cgi program. Good for testing. Not secure.
"""

import BaseHTTPServer
import CGIHTTPServer
import thread
import os
import webbrowser
import sys
from optparse import OptionParser


def main():

    usage = "runcgi.py [options] target\n" + __doc__

    root_opt = "Set the server root directory. Defaults to the current directory."

    cgibin_opt = ("Set a cgi script directory, relative to the server root. "
        "Option may be given multiple times for multiple script directories. "
        "Defaults to the one directory holding target.")

    port_opt = "Set the server's port number. By default the system chooses it."

    query_opt = "URL query string, without the '?'. The default is no query"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--root", default='.', help=root_opt)
    parser.add_option("-c", "--cgi-bin", action="append", dest="cgibin", help=cgibin_opt)
    parser.add_option("-p", "--port", type='int', default=0, help=port_opt)
    parser.add_option("-q", "--query", default='', help=query_opt)

    (options, args) = parser.parse_args()
    if len(args) != 1:
        print >> sys.stderr, "Error: need exactly one target cgi program."
        parser.print_help()
        sys.exit(-1)

    cgi_target = args[0]
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    os.chdir(options.root)
    cgi_dirs = handler.cgi_directories
    if options.cgibin is not None:
        cgi_dirs[:] = options.cgibin
    else:
        cgi_dirs[:] = [os.path.split(cgi_target)[0]]
    for i in range(len(cgi_dirs)):
        if not cgi_dirs[i].startswith('/'):
            cgi_dirs[i] = '/' + cgi_dirs[i]
        if len(cgi_dirs[i]) > 1 and cgi_dirs[i].endswith('/'):
            cgi_dirs[i] = cgi_dirs[i][:-1]

    httpd = BaseHTTPServer.HTTPServer(('localhost', options.port), handler)
    thread.start_new_thread(httpd.serve_forever, ())

    url = 'http://%s:%d/%s' % ('localhost', httpd.server_port, cgi_target)
    if options.query:
        url = url + '?' + options.query
    try:
        webbrowser.open_new(url)
    except Exception, e:
        print >> sys.stderr, 'Failed automatic web browser launch: %s' % str(e)
        print >> sys.stderr, 'Target URL is:', url

    raw_input("Hit return to exit server.\n\n")
    sys.exit(0)

if __name__ == '__main__':
    main()
