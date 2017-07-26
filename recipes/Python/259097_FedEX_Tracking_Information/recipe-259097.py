"""
This script uses the FedEx web site to download tracking information
from the web form.

Current version has US and English hardcoded in the URL.  Should be trivial to modify to support other locations/locales.

Version history

1.0     12/6/03     CBM     Initial Release
"""
__version__="1.0"
__author__="Chris Moffitt"

import sgmllib, urllib, httplib
import string
import sys, os
from optparse import OptionParser


class FedexParser(sgmllib.SGMLParser):
    """Parse the return from the FedEx site"""
    
    def __init__(self, verbose =0):
        self.results = ""
        sgmllib.SGMLParser.__init__(self, verbose)
        self.inResultsTable = False
        self.output = []
        self.tempout = []
        self.inTable = False
        self.inTD = False
        self.inResultsArea = False
        self.inTR = False
        self.collectResults = False

    def start_td(self, args="none"):
        self.inTD = True
        
    def end_td(self, args="none"):
        self.inTD = False
        
    def start_tr(self, args="none"):
        self.inTR = True

    def end_tr(self, args="none"):
        self.inTR = False
        if self.collectResults:
            self.output.append(self.tempout)
            self.tempout = []
        if self.inResultsArea:
            self.collectResults = True
           
    def start_table(self, args="none"):
        self.inTable = True
        
    def end_table(self, args="none"):
        self.inTable = False
        self.collectResults = False
        self.inResultsArea = False

    def handle_data(self, data):
        if self.inTD and self.inTable and self.inTR and "Scan Activity" in data:
            self.inResultsArea = True
        if self.collectResults and self.inTD:
            self.tempout.append(string.rstrip(data))
            
    def returnresults(self):
        return(self.output)

if __name__ == '__main__':
    usage = "usage: %prog [-v] firstTracking# secondTracking#"
    parser = OptionParser(usage, version="%prog 1.0")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",
                      help="Display all tracking data")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("Must enter at least one item to track")

    for num in args:
        readFedEx = FedexParser()
        postData = urllib.urlencode( {"action":"track",
                                       "cntry_code":"ca_english",
                                       "tracknumbers":num} )
        fedExURL = "http://www.fedex.com/cgi-bin/tracking?%s" % postData
        fedExPost = urllib.urlopen(fedExURL)
        fedExResults = fedExPost.read()
        fedExPost.close()
        readFedEx.feed(fedExResults)
        readFedEx.close()
        results = readFedEx.returnresults()
        print "Tracking Results for %s:" % num
        if len(results) < 2:
            print "Error - Invalid tracking number\n"
            continue
        if options.verbose:
            for line in results:
                print string.join(line),"\n"
        else:
            print string.join(results[0]),"\n"

    
    
