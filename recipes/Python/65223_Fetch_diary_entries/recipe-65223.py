#!/usr/bin/env python

import sgmllib, string, urllib

class DiaryParser(sgmllib.SGMLParser):
    
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        self.entries = []
        self.dates = [] 
        self.inHtml = 0
        self.inDate = 0
        self.data = ""
        
    def handle_data(self, data):
        self.data = self.data + data
    
    def unknown_starttag(self, tag, attrs):
        pass
                
    def unknown_endtag(self, tag):
        pass

    def start_html(self, attributes):
        self.inHtml = 1
        self.data = ""
        self.setliteral()
    
    def end_html(self):
        self.entries.append(self.data)
        self.inHtml = 0
    
    def start_date(self, attributes):
        self.data = ""
        self.setliteral()
    
    def end_html(self):
        self.entries.append(self.data)
        self.inHtml = 0
    
    def start_date(self, attributes):
        self.data = ""
        self.inDate = 1
    
    def end_date(self):
        self.dates.append(self.data)
        self.inDate = 0
        

def getEntries(person):
    """ Fetch a Advogato member's diary and return a dictionary in the form
        { date : entry, ... } 
    """
    
    parser = DiaryParser()
    f = urllib.urlopen("http://www.advogato.org/person/%s/diary.xml" % urllib.quote(person))
    
    s = f.read(8192)
    while s:
        parser.feed(s)
        s = f.read(8192)
    
    parser.close()
    result = {}
    for d, e in map(None, parser.dates, parser.entries):
        result[d] = e
    return result


if __name__=='__main__':
    import sys
    print getEntries(sys.argv[1])
