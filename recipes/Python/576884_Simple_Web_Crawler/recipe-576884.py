# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from urllib2 import urlopen

class Spider(HTMLParser):
    def __init__(self, starting_url, depth, max_span):
        HTMLParser.__init__(self)
        self.url = starting_url
        self.db = {self.url: 1}
        self.node = [self.url]

        self.depth = depth # recursion depth max
        self.max_span = max_span # max links obtained per url
        self.links_found = 0

    def handle_starttag(self, tag, attrs):
        if self.links_found < self.max_span and tag == 'a' and attrs:
            link = attrs[0][1]
            if link[:4] != "http":
                link = '/'.join(self.url.split('/')[:3])+('/'+link).replace('//','/')

            if link not in self.db:
                print "new link ---> %s" % link
                self.links_found += 1
                self.node.append(link)
            self.db[link] = (self.db.get(link) or 0) + 1

    def crawl(self):
        for depth in xrange(self.depth):
            print "*"*70+("\nScanning depth %d web\n" % (depth+1))+"*"*70
            context_node = self.node[:]
            self.node = []
            for self.url in context_node:
                self.links_found = 0
                try:
                    req = urlopen(self.url)
                    res = req.read()
                    self.feed(res)
                except:
                    self.reset()
        print "*"*40 + "\nRESULTS\n" + "*"*40
        zorted = [(v,k) for (k,v) in self.db.items()]
        zorted.sort(reverse = True)
        return zorted

if __name__ == "__main__":
    spidey = Spider(starting_url = 'http://www.7cerebros.com.ar', depth = 5, max_span = 10)
    result = spidey.crawl()
    for (n,link) in result:
        print "%s was found %d time%s." %(link,n, "s" if n is not 1 else "")
