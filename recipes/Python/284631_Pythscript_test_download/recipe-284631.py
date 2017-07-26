from HTMLParser import HTMLParser
import urllib
import time
import Queue
import threading
import urlparse

MIRRORS_URL = 'http://fedora.redhat.com/download/mirrors.html'
MAX_THREADS = 50
HTTP_TIMEOUT = 60.0   # Max. seconds to wait for a response

class UrlFinder(HTMLParser):

    '''Subclass of the HTMLParser object.  Records the HREF attributes
    of anchor tags if the scheme is 'http' and the anchor occurs in
    the 'content' section of the page.'''
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.mirrorLinks = []  

        # True if we're currently in the 'content' section
        self.isInMirrors = False
        
    def handle_comment(self, data):

        # The comments have spaces before and after, but don't count
        # on that.
        data = data.strip()

        if 'content BEGIN' == data:
            self.isInMirrors = True
        elif 'content END' == data:
            self.isInMirrors = False

    def handle_starttag(self, tag, attrs):
        if self.isInMirrors:
            attrs = dict(attrs) # Convert from tuple of tuples to dict
            if 'a' == tag and 'http' == urllib.splittype(attrs['href'])[0]:
                self.mirrorLinks.append(attrs['href'])

# Record the start time, so we can print a nice message at the end
processStartTime = time.time()

# Create the parser, get the 'mirrors' page from Redhat,
# and extract the URLs
print "Getting mirrors list...",
parser = UrlFinder()
parser.feed(urllib.urlopen(MIRRORS_URL).read())


print len(parser.mirrorLinks), "mirrors found."
numThreads = min(MAX_THREADS, len(parser.mirrorLinks))
print "Testing bandwidth with", numThreads, "threads..."

# Build a queue to feed the worker threads
workQueue = Queue.Queue()
for url in parser.mirrorLinks:
    workQueue.put(url)

def TestUrl(workQueue, resultQueue):

    ''' Worker thread procedure.  Test how long it takes to return the
    mirror index page, and stuff the results into resultQueue.'''
    
    def SubthreadProc(url, result):

        ''' Subthread procedure.  Actually get the mirror index page
        in a subthread, so that we can time out using join rather than
        wait for a very slow server.  Passing in a list for result
        lets us simulate pass-by-reference, since callers cannot get
        the return code from a Python thread.'''
        
        startTime = time.time()
        try:
            data = urllib.urlopen(url).read()
        except Exception:
            # Could be a socket error or an HTTP error--either way, we
            # don't care--it's a failure to us.
            result.append(-1)
        else:
            elapsed = int((time.time() - startTime) * 1000)
            result.append(elapsed)

            
    while 1:
        # Contine pulling data from the work queue until it's empty
        try:
            url = workQueue.get(0)
        except Queue.Empty:
            # work queue is empty--exit the thread proc.
            return

        # Create a single subthread to do the actual work
        result = []
        subThread = threading.Thread(target=SubthreadProc, args=(url, result))

        # Daemonize the subthread so that even if a few are hanging
        # around when the process is done, the process will exit.
        subThread.setDaemon(True)

        # Run the subthread and wait for it to finish, or time out
        subThread.start()
        subThread.join(HTTP_TIMEOUT)

        if [] == result:
            # Subthread hasn't give a result yet.  Consider it timed out.
            resultQueue.put((url, "TIMEOUT"))
        elif -1 == result[0]:
            # Subthread returned an error from geturl.
            resultQueue.put((url, "FAILED"))
        else:
            # Subthread returned a time.  Store it.
            resultQueue.put((url, result[0]))
        

workers = []
resultQueue = Queue.Queue()

# Create worker threads to load-balance the retrieval
for threadNum in range(0, numThreads):
    workers.append(threading.Thread(target=TestUrl,
                                    args=(workQueue,resultQueue)))
    workers[-1].start()

# Wait for all the workers to finish
for w in workers:
    w.join()

# Separate the successes from failures
timings = []
failures = []
while not resultQueue.empty():
    url, result = resultQueue.get(0)
    if isinstance(result, str):
        failures.append((result, url))
    else:
        timings.append((result, url))

# Sort by increasing time or result string
timings.sort()
failures.sort()

# Print the results
print "\nMirrors (ordered fastest to slowest)"
for result, url in timings:
    print "%7d %s" % (result, url)
for result, url in failures:
    print "%7s %s" % (result, url)

print "\nProcess completed in ", time.time() - processStartTime, " seconds."
