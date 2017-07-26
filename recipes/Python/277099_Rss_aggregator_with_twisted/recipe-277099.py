from twisted.internet import reactor, protocol, defer
from twisted.web import client
import feedparser, time, sys

# You can get this file from http://xoomer.virgilio.it/dialtone/out.py
# Since it's only a list of URLs made in this way:
# out = [  ( 'URL', 'EXTRA_INFOS'),
#          ( 'URL', 'EXTRA_INFOS')
#          ...
#        ]
import out

try:
    import cStringIO as _StringIO
except ImportError:
    import StringIO as _StringIO

rss_feeds = out.rss_feed # This is the HUGE feed list  (730 feeds)

DEFERRED_GROUPS = 60  # Number of simultaneous connections
INTER_QUERY_TIME = 300 # Max Age (in seconds) of each feed in the cache
TIMEOUT = 30 # Timeout in seconds for the web request

# This dict structure will be the following:
# { 'URL': (TIMESTAMP, value) }
cache = {}

class FeederProtocol(object):
    def __init__(self):
        self.parsed = 1
        self.with_errors = 0
        self.error_list = []
        
    def isCached(self, site):
        # Try to get the tuple (TIMESTAMP, FEED_STRUCT) from the dict if it has
        # already been downloaded. Otherwise assign None to already_got
        already_got = cache.get(site[0], None)

        # Ok guys, we got it cached, let's see what we will do
        if already_got:
            # Well, it's cached, but will it be recent enough?
            elapsed_time = time.time() - already_got[0]
            
            # Woooohooo it is, elapsed_time is less than INTER_QUERY_TIME so I
            # can get the page from the memory, recent enough
            if elapsed_time < INTER_QUERY_TIME:
                return True
            
            else:    
                # Uhmmm... actually it's a bit old, I'm going to get it from the
                # Net then, then I'll parse it and then I'll try to memoize it
                # again
                return False
            
        else: 
            # Well... We hadn't it cached in, so we need to get it from the Net
            # now, It's useless to check if it's recent enough, it's not there.
            return False

    def gotError(self, traceback, extra_args):
        # An Error as occurred, print traceback infos and go on
        print traceback, extra_args
        self.with_errors += 1
        self.error_list.append(extra_args)
        print "="*20
        print "Trying to go on..."
        
    def getPageFromMemory(self, data, key=None):
        # Getting the second element of the tuple which is the parsed structure
        # of the feed at address key, the first element of the tuple is the
        # timestamp
        print "Getting from memory..."
        return defer.succeed(cache.get(key,key)[1])

    def parseFeed(self, feed):
        # This is self explaining :)
        print "parsing..."
        try:
            feed+''
            parsed = feedparser.parse(_StringIO.StringIO(feed))
        except TypeError:
            parsed = feedparser.parse(_StringIO.StringIO(str(feed)))
        print "parsed feed"
        return parsed
   
    def memoize(self, feed, addr):
        # feed is the raw structure, just as returned from feedparser.parse()
        # while addr is the address from which the feed was got.
        print "Memoizing",addr,"..."
        if cache.get(addr, None):
            cache[addr] = (time.time(), feed)
        else:
            cache.setdefault(addr, (time.time(),feed))
        return feed
    
    def workOnPage(self, parsed_feed, addr):
        # As usual, addr is the feed address and file is the file in
        # which you can eventually save the structure.
        print "-"*20
        print "finished retrieving"
        print "Feed Version:",parsed_feed.get('version','Unknown')
        
        #
        #  Uncomment the following if you want to print the feeds
        #
        chan = parsed_feed.get('channel', None)
        if chan:
            print chan.get('title', '')
            #print chan.get('link', '')
            #print chan.get('tagline', '')
            #print chan.get('description','')
        print "-"*20
        #items = parsed_feed.get('items', None)
        #if items:
        #    for item in items:
        #        print '\tTitle: ', item.get('title','')
        #        print '\tDate: ', item.get('date', '')
        #        print '\tLink: ', item.get('link', '')
        #        print '\tDescription: ', item.get('description', '')
        #        print '\tSummary: ', item.get('summary','')
        #        print "-"*20
        #print "got",addr
        #print "="*40
        return parsed_feed
        
    def stopWorking(self, data=None):
        print "Closing connection number %d..."%(self.parsed,)
        print "=-"*20
        
        # This is here only for testing. When a protocol/interface will be
        # created to communicate with this rss-aggregator server, we won't need
        # to die after we parsed some feeds just one time.
        self.parsed += 1
        print self.parsed,  self.END_VALUE
        if self.parsed > self.END_VALUE:   #
            print "Closing all..."         #
            for i in self.error_list:      #  Just for testing sake
                print i                    #
            print len(self.error_list)     #
            reactor.stop()                 #

    def getPage(self, data, args):
        return client.getPage(args,timeout=TIMEOUT)

    def printStatus(self, data=None):
        print "Starting feed group..."
            
    def start(self, data=None, std_alone=True):
        d = defer.succeed(self.printStatus())
        for feed in data:
        
            # Now we start telling the reactor that it has
            # to get all the feeds one by one...
            cached = self.isCached(feed)
            if not cached: 
                # When the feed is not cached, it's time to
                # go and get it from the web directly
                d.addCallback(self.getPage, feed[0])
                d.addErrback(self.gotError, (feed[0], 'getting'))
                
                # Parse the feed and if there's some errors call self.gotError
                d.addCallback(self.parseFeed)
                d.addErrback(self.gotError, (feed[0], 'parsing'))
                
                # Now memoize it, if there's some error call self.getError
                d.addCallback(self.memoize, feed[0])
                d.addErrback(self.gotError, (feed[0], 'memoizing'))
                
            else: # If it's cached
                d.addCallback(self.getPageFromMemory, feed[0])
                d.addErrback(self.gotError, (feed[0], 'getting from memory'))
            
            # When you get the raw structure you can work on it
            # to format in the best way you can think of.
            # For any error call self.gotError.
            d.addCallback(self.workOnPage, feed[0])
            d.addErrback(self.gotError, (feed[0], 'working on page'))
            
            # And when the for loop is ended we put 
            # stopWorking on the callback for the last 
            # feed gathered
            # This is only for testing purposes
            if std_alone:
                d.addCallback(self.stopWorking)
                d.addErrback(self.gotError, (feed[0], 'while stopping'))
        if not std_alone:
            return d

class FeederFactory(protocol.ClientFactory):
    protocol = FeederProtocol()
    def __init__(self, std_alone=False):
        self.feeds = self.getFeeds()
        self.std_alone = std_alone
        
        self.protocol.factory = self
        self.protocol.END_VALUE = len(self.feeds) # this is just for testing

        if std_alone:
            self.start(self.feeds)

    def start(self, addresses):
        # Divide into groups all the feeds to download
        if len(addresses) > DEFERRED_GROUPS:
            url_groups = [[] for x in xrange(DEFERRED_GROUPS)]
            for i, addr in enumerate(addresses):
                url_groups[i%DEFERRED_GROUPS].append(addr)
        else:
            url_groups = [[addr] for addr in addresses]
            
        for group in url_groups:
            if not self.std_alone:
                return self.protocol.start(group, self.std_alone)
            else:
                self.protocol.start(group, self.std_alone)

    def getFeeds(self, where=None):
        # This is used when you call a COMPLETE refresh of the feeds,
        # or for testing purposes
        #print "getting feeds"
        # This is to get the feeds we want
        if not where: # We don't have a database, then we use the local
                      # variabile rss_feeds
            return rss_feeds
        else: return None
        
if __name__=="__main__":
    f = FeederFactory(std_alone=True)
    reactor.run()
