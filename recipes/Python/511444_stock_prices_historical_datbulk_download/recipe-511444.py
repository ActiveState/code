#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'gian paolo ciceri <gp.ciceri@gmail.com>'
__version__ = '0.1'
__date__ = '20070401'
__credits__ = "queue and MT code was shamelessly stolen from pycurl example retriever-multi.py"

#
# Usage: python grabYahooDataMt.py -h 
#
#
# for selecting tickers and starting date it uses an input file of this format 
# <ticker> <fromdate as YYYYMMDD>
# like
# ^GSPC 19500103 # S&P 500
# ^N225 19840104 # Nikkei 225

import sys, threading, Queue, datetime
import urllib
from optparse import OptionParser


# this thread ask the queue for job and does it!
class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            try:
                # fetch a job from the queue
                ticker, fromdate, todate = self.queue.get_nowait()
            except Queue.Empty:
                raise SystemExit
            if ticker[0] == "^": 
                tick = ticker[1:]
            else:
                tick = ticker
            filename = downloadTo + "%s_%s.csv" % (tick, todate)
            fp = open(filename, "wb")
            if options.verbose:
                print "last date asked:", todate, todate[0:4], todate[4:6], todate[6:8] 
                print "first date asked:", fromdate, fromdate[0:4], fromdate[4:6], fromdate[6:8]
            quote = dict()
            quote['s'] = ticker
            quote['d'] = str(int(todate[4:6]) - 1)
            quote['e'] = str(int(todate[6:8]))
            quote['f'] = str(int(todate[0:4]))
            quote['g'] = "d" 
            quote['a'] = str(int(fromdate[4:6]) - 1)
            quote['b'] = str(int(fromdate[6:8]))
            quote['c'] = str(int(fromdate[0:4]))
            #print quote
            params = urllib.urlencode(quote)
            params += "&ignore=.csv"

            url = "http://ichart.yahoo.com/table.csv?%s" % params
            if options.verbose:
                print "fetching:", url           
            try:
                f = urllib.urlopen(url)
                fp.write(f.read())
            except:
                import traceback
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()
            fp.close()
            if options.verbose:
                print url, "...fetched"
            else:
                sys.stdout.write(".")
                sys.stdout.flush()



if __name__ == '__main__':

    # today is
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    # parse arguments
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="tickerfile", action="store", default = "./tickers.txt",
    				  help="read ticker list from file, it uses ./tickers.txt as default")
    parser.add_option("-c", "--concurrent", type="int", dest="connections", default = 10, action="store",
    				  help="# of concurrent connections")
    parser.add_option("-d", "--dir", dest="downloadTo", action="store", default = "./rawdata/",
    				  help="save date to this directory, it uses ./rawdata/ as default")
    				  
    parser.add_option("-t", "--todate", dest="todate", default = today, action="store",
    				  help="most recent date needed")
    parser.add_option("-v", "--verbose",
    					  action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
    					  action="store_false", dest="verbose")					 
    (options, args) = parser.parse_args()

    
    tickerfile = options.tickerfile
    downloadTo = options.downloadTo
    connections =  options.connections
    today = options.todate
    

    # get input list
    try:
    	tickers = open(tickerfile).readlines()
    except:
    	parser.error("ticker file %s not found" % (tickerfile,))
    	raise SystemExit
    
    
    # build a queue with (ticker, fromdate, todate) tuples
    queue = Queue.Queue()
    for tickerRow in tickers:
    	#print tickerRow
    	tickerRow = tickerRow.strip()
    	if not tickerRow or tickerRow[0] == "#":
    		continue
    	tickerSplit = tickerRow.split()
    	# ticker, fromdate, todate
    	queue.put((tickerSplit[0], tickerSplit[1], today))

    

    
    # Check args
    assert queue.queue, "no Tickers given"
    numTickers = len(queue.queue)
    connections = min(connections, numTickers)
    assert 1 <= connections <= 255, "too much concurrent connections asked"

    
    if options.verbose:
    	print "----- Getting", numTickers, "Tickers using", connections, "simultaneous connections -----"
    
    
    # start a bunch of threads, passing them the queue of jobs to do
    threads = []
    for dummy in range(connections):
    	t = WorkerThread(queue)
    	t.start()
    	threads.append(t)
    
    
    # wait for all threads to finish
    for thread in threads:
    	thread.join()
    sys.stdout.write("\n")
    sys.stdout.flush()
       	
    # tell something to the user before exiting
    if options.verbose:	   
    	print "all threads are finished - goodbye."
