"""
LoggingWebMonitor - a central logging server and monitor.

Listens for log records sent from other processes running
in the same box or network.  Collects and saves them
concurrently in a log file.  Shows a summary web page with
the latest N records received.

Usage:

- Add a SocketHandler to your application::

    from logging.handlers import SocketHandler, DEFAULT_TCP_LOGGING_PORT
    socketh = SocketHandler(servername, DEFAULT_TCP_LOGGING_PORT)
    logging.getLogger('').addHandler(socketh)

  where servername is the host name of the logging server ('localhost'
  if run on the same box)

- Start an instance of this script (the logging server).
  This will open two listening sockets:

    - one at DEFAULT_TCP_LOGGING_PORT (9020), listening for
      logging events from your application

    - a web server at DEFAULT_TCP_LOGGING_PORT+1 (9021),
      showing a summary web page with the latest 200
      log records received.  That web page will be
      opened by default, using your preferred web browser.

- You may add additional handlers or filters to this script;
  see fileHandler below.

- Note that several separate processes *cannot* write to the same
  logging file; this script avoids that problem, providing
  the necesary isolation level.

- If you customize the logging system here, make sure `mostrecent`
  (instance of MostRecentHandler) remains attached to the root logger.
  
Author: Gabriel A. Genellina, based on code from Vinay Sajip and
doug.farrell

This has been tested with Python versions 2.3 thru 2.6; on versions
older than 2.5, Ctrl-C handling and the stack trace may not work 
as expected.
"""

import os
import sys
import cPickle
import logging
import logging.handlers
import SocketServer
import BaseHTTPServer
import struct
import threading
import datetime
import cgi
import time

try:
    from collections import deque
except ImportError:
    # pre 2.5
    class deque(list):
        def popleft(self):
            elem = self.pop(0)
            return elem

try:
    reversed 
except NameError:
    # pre 2.4
    def reversed(items):
        return items[::-1]


class MostRecentHandler(logging.Handler):
    'A Handler which keeps the most recent logging records in memory.'

    def __init__(self, max_records=200):
        logging.Handler.__init__(self)
        self.logrecordstotal = 0
        self.max_records = max_records
        try:
            self.db = deque([], max_records)
        except TypeError:
            # pre 2.6
            self.db = deque([])

    def emit(self, record):
        self.logrecordstotal += 1
        try:
            self.db.append(record)
            # pre 2.6
            while len(self.db)>self.max_records:
                self.db.popleft()
        except Exception:
            self.handleError(record)


# taken from the logging package documentation by Vinay Sajip

class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    'Handler for a streaming logging request'

    def handle(self):
        '''
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format.
        '''
        while 1:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LoggingReceiver(SocketServer.ThreadingTCPServer):
    'Simple TCP socket-based logging receiver'

    logname = None

    def __init__(self, host='localhost',
                 port=None,
                 handler=LogRecordStreamHandler):
        if port is None:
            port = logging.handlers.DEFAULT_TCP_LOGGING_PORT
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)


# idea and page layout taken from python-loggingserver by doug.farrell
# http://code.google.com/p/python-loggingserver/

class LogginWebMonitorRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
            fmt='%(asctime)s\n%(name)s\n%(levelname)s\n%(funcName)s (%(filename)s:%(lineno)d)\n%(message)s',
            datefmt=datefmt)

    default_css = """\
body {
  font-family: verdana, arial, helvetica, sans-serif;
}
table {
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  border: 1px solid black;
  margin-top: 3ex;
}
table caption {
  /*font-weight: bold;*/
  text-align: center;
  font-size: larger;
  margin-bottom: 0.5ex;
}
tr {
  font-family: "Lucida Console", monospace;
}
th, td {
  padding: 0.5ex;
}
tr.critical {
  background-color: red;
  color: yellow;
  text-decoration: blink;
}
tr.error {
  background-color: #ff3300; /* red */
  color: yellow;
}
tr.warn, tr.warning {
  background-color: #ffff99; /* yellow */
  color: black;
}
tr.info, td.info {
  background-color: #90EE90; /* lightgreen */
  color: black;
}
tr.debug {
  background-color: #7FFFD4; /* aquamarine */
  color: black;
}
table.vtable tr th {
  font-weight: bold;
  text-align: right;
}
table.htable tr th {
  font-weight: bold;
  text-align: center;
}
table.htable tr.heading,
table.vtable tr th.heading {
  background-color: #E0E0E0;
}
"""

    summary_html = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1">
    <meta http-equiv="refresh" content="5">
    <title>Logging Server Status Page</title>
    <link rel="stylesheet" type="text/css" href="/default.css">
  </head>
  <body>
    <table class="vtable">
      <caption>Logging Server Status Page</caption>
      <tr>
        <th class="heading">Logging Server Start Time</th>
        <td class="info">%(starttime)s</td>
      </tr>
      <tr>
        <th class="heading">Logging Server Up Time</th>
        <td class="info">%(uptime)s</td>
      </tr>
      <tr>
        <th class="heading">Log Records Total</th>
        <td class="info">%(logrecordstotal)s</td>
      </tr>
    </table>
    <table class="htable">
      <caption>Most Recent Log Records</caption>
      <tr class="heading"><th>Date</th><th>Channel</th><th>Level</th><th>Location</th><th>Message</th></tr>
      %(records)s
    </table>
    <p style="text-align:right">
    <a href="http://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="http://jigsaw.w3.org/css-validator/images/vcss"
            alt="Valid CSS">
    </a>
    <a href="http://validator.w3.org/check?uri=referer"><img
        src="http://www.w3.org/Icons/valid-html401"
        alt="Valid HTML 4.01 Strict" height="31" width="88"></a>
    </p>
  </body>
</html>
"""

    def do_GET(self):
        'Serve a GET request.'
        sts, response, type = self.build_response(self.path)
        self.send_response(sts)
        if sts==301:
            self.send_header('Location', response)
        if type:
            self.send_header('Content-type', type)
            self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        if response:
            self.wfile.write(response)

    def build_response(self, path):
        try:
            if path == '/summary.html':
                return 200, self.summary_page(), 'text/html'
            if path == '/default.css':
                return 200, self.default_css, 'text/css'
            if path == '/':
                return 301, '/summary.html', 'text/html'
            return 404, None, None
        except Exception:
            import traceback
            print >>sys.stderr, 'While handling %r:' % path
            traceback.print_exc(file=sys.stderr)
            return 500, None, None

    def summary_page(self):
        escape = cgi.escape
        mostrecent = self.server.mostrecent

        starttime = escape(self.server.starttime.strftime(self.datefmt))
        uptime = datetime.datetime.now() - self.server.starttime
        uptime = escape(str(datetime.timedelta(uptime.days, uptime.seconds)))
        logrecordstotal = escape(str(mostrecent.logrecordstotal))

        formatter = self.formatter
        items = []
        for record in reversed(list(mostrecent.db)):
            try:
                cells = escape(formatter.format(record)).split('\n', 4)
                cells = ['<td>%s</td>' % cell for cell in cells]
                cells[-1] = cells[-1].replace('\n', '<br>\n') # message & stack trace
                items.append('<tr class="%s">%s\n</tr>' %
                    (escape(record.levelname.lower()), ''.join(cells)))
            except Exception:
                import traceback
                print >>sys.stderr, 'While generating %r:' % record
                traceback.print_exc(file=sys.stderr)
        records = '\n'.join(items)
        d = dict(starttime=starttime,
                 uptime=uptime,
                 logrecordstotal=logrecordstotal,
                 records=records)
        return self.summary_html % d

    def log_message(self, format, *args):
        pass


class LoggingWebMonitor(BaseHTTPServer.HTTPServer):
    'A simple web page for displaying logging records'

    def __init__(self, host='localhost',
                 port=None,
                 handler=LogginWebMonitorRequestHandler):
        if port is None:
            port = logging.handlers.DEFAULT_TCP_LOGGING_PORT + 1
        BaseHTTPServer.HTTPServer.__init__(self, (host, port), handler)
        self.starttime = datetime.datetime.now()


if not hasattr(SocketServer.TCPServer, 'shutdown'):

    # pre 2.6

    _original_get_request = SocketServer.TCPServer.get_request

    def serve_forever(self):
        while not self.quit:
            self.handle_request()

    def shutdown(self):
        self.quit = True

    def get_request(self):
        self.socket.settimeout(30)
        request, client_address = _original_get_request(self)
        request.settimeout(30)
        return request, client_address

    for cls in (LoggingReceiver, LoggingWebMonitor):
        cls.serve_forever = serve_forever
        cls.shutdown = shutdown
        cls.get_request = get_request
        cls.quit = False



def main():
    mostrecent = MostRecentHandler()
    rootLogger = logging.getLogger('')
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.addHandler(mostrecent)

    ## You may add additional handlers like this FileHandler
    ## that logs every message to a file
    ## named after this module name, with extension .log
    #
    #formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    #fileHandler = logging.FileHandler(os.path.splitext(__file__)[0] + '.log')
    #fileHandler.setFormatter(formatter)
    #rootLogger.addHandler(fileHandler)

    webmonitor = LoggingWebMonitor()
    webmonitor.mostrecent = mostrecent
    thr_webmonitor = threading.Thread(target=webmonitor.serve_forever)
    thr_webmonitor.daemon = True
    print '%s started at %s' % (webmonitor.__class__.__name__, webmonitor.server_address)
    thr_webmonitor.start()

    recv = LoggingReceiver()
    thr_recv = threading.Thread(target=recv.serve_forever)
    thr_recv.daemon = True
    print '%s started at %s' % (recv.__class__.__name__, recv.server_address)
    thr_recv.start()

    import webbrowser
    webbrowser.open('http://%s:%s/' % webmonitor.server_address)

    while True:
        try: time.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            recv.shutdown()
            webmonitor.shutdown()
            break

    return 0

if __name__ == '__main__':
    sys.exit(main())
