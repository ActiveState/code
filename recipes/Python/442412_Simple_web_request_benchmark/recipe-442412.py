'''
test_web_server.py
- a script to test some basic metrics of a web server

Sample output:
D:\test_web_server>test_web_server.py -c10 -t15 -p987 -s -f/links.html
**************official results (1934):
           connect  request get some get rest    total
          -------- -------- -------- -------- --------
average:      0.02     0.00     0.02     0.05     0.08
median:       0.02     0.00     0.02     0.04     0.08
std dev:      0.02     0.00     0.01     0.02     0.03
minimum:      0.00     0.00     0.00     0.00     0.01
maximum:      0.47     0.03     0.22     0.27     0.55
approximate requests/second:  128.266347738
Total bytes transferred:      31779488
Bytes transferred per second: 2103208


In this particular run, it was downloading a 16281 byte file called
links.html from a web server running on the local host.

1.1
 - Adds handling of new connection creation failure, includes such failures
   into the connect time, and keeps a running total of failures.
 - Added support for zero total results.
1.2
 - Adds data transfer rates and totals.
1.3
 - Adds support for Host: header for HTTP 1.1 servers.
'''


import sys
import socket
import threading
import Queue
import time
import optparse

results = Queue.Queue()
refused = 0L
transferred = 0L
reflock = threading.Lock()

endtime = None

def worker(host, port, file, include_host):
    C = 0
    D = 0
    if include_host:
        request = 'GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n'%(file, host)
    else:
        request = 'GET /%s HTTP/1.1\r\n\r\n'%file
    
    t = [time.time()]
    
    while time.time() < endtime:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
        except:
            C += 1
            s.close()
            continue
        t.append(time.time())
        s.sendall(request)
        t.append(time.time())
        try:
            while 1:
                _ = s.recv(65536)
                if not _:
                    break
                elif len(t) == 3:
                    t.append(time.time())
                D += len(_)
        except:
            pass
        s.close()
        while len(t) < 5:
            t.append(time.time())
        t2 = []
        x = t.pop(0)
        while t:
            y = t.pop(0)
            t2.append(y-x)
            x = y
        results.put(t2)
        t = [time.time()]
    reflock.acquire()
    global refused, transferred
    refused += C
    transferred += D
    reflock.release()

def _stats(r):
    #returns the median, average, standard deviation, min and max of a sequence
    tot = sum(r)
    avg = tot/len(r)
    sdsq = sum([(i-avg)**2 for i in r])
    s = list(r)
    s.sort()
    return s[len(s)//2], avg, (sdsq/(len(r)-1 or 1))**.5, min(r), max(r)

x = ('average: ', 'median:  ', 'std dev: ', 'minimum: ', 'maximum: ')

def stats(r, e):
    for i in r:
        i.append(sum(i))
    
    s = zip(*map(_stats, zip(*r)))
    print "           connect  request get some get rest    total"
    print "          -------- -------- -------- -------- --------"
    for i,j in zip(x, s):
        print i, "%8.2f %8.2f %8.2f %8.2f %8.2f"%j
    print "approximate requests/second: ", len(r)/float(e)

if __name__ == '__main__':
    usage = "usage: \%prog -c<count> -t<time> -H<host> -p<port> -f<file>"
    
    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--count', dest='count', type='int',
        help='Number of simultaneous threads (default 5)', default=5,
        action='store')
    parser.add_option('-t', '--time', dest='time', type='int',
        help='At least how long in seconds to run the test (default 60)',
        default=60, action='store')
    parser.add_option('-H', '--host', dest='host',
        help='The host of the web server (default localhost)',
        default='localhost', action='store')
    parser.add_option('-i', '--include', dest='include', action='store_true',
        help='if passed, will include Host: header as specified with -H in the request',
        default=False)
    parser.add_option('-p', '--port', dest='port', type='int',
        help='Port to connect to on (default 80)', default=80, action='store')
    parser.add_option('-f', '--file', dest='file',
        help='the file to download', action='store')
    parser.add_option('-s', '--single', dest='single', action='store_true',
        help='if passed, will only produce one table of output', default=False)
    
    options, args = parser.parse_args()
    
    if options.file is None:
        parser.error('need file to fetch')
    
    starttime = time.time()
    endtime = starttime + options.time
    for i in xrange(options.count):
        threading.Thread(target=worker,
            args=(options.host, options.port,
                  options.file.lstrip('/\\'), options.include)).start()
    if not options.single:
        while endtime > time.time():
            time.sleep(.1)
        
        r = []
        while results.qsize():
            r.append(results.get())
        rc = len(r)
        if r:
            print "**************official results (%i):"%(len(r))
            stats(r, options.time)
        
        while threading.activeCount() > 1:
            time.sleep(.1)
        
        r = []
        while results.qsize():
            r.append(results.get())
        if r:
            print "**************late finishers (%i):"%(len(r))
            stats(r, time.time()-endtime)
    
        print "effective requests/second:   ", (rc+len(r))/(time.time()-starttime)
    
    else:
        while threading.activeCount() > 1:
            time.sleep(.1)
        
        r = []
        while results.qsize():
            r.append(results.get())
        if r:
            print "**************official results (%i):"%(len(r))
            stats(r, time.time()-starttime)
    
    print "Total bytes transferred:     ", transferred
    print "Bytes transferred per second:", int(transferred/(time.time()-starttime))
    
    if refused:
        print "Connections refused:         ", refused
    
