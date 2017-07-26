#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import re
from urllib import unquote
from urllib2 import Request,build_opener


class PagerEngine:
    retag=re.compile("<[^>]+>")
    remultag=re.compile("<[^>]+>(<[^>]+>)+")

    def __init__(self,query):
        query=query.replace(" ","%20")
        query=query.replace("+","%2b")
        query=query.replace("\"","%27")
        self.query=query

        self.results=[]
        self.diccres={}

        self.startIndex=0               ## Start index
        self.increment=10               ## Index increment
        self.lastResult=""
        self.start=None                 ## First index for the search

        self.MoreResults=None


        ########### Overload variables, must be modified per website #############
        self.url=None
        self.queryvar=None
        self.startvar=None

        self.urlRegexp=None            ## Regexp of desired information
        self.nextRegexp=None           ## Regex to know if there are more pages to follow


    def __iter__(self):
        self.start=None
        self.MoreResults=None
        return self

    def addResult(self,res):
        res=self.processResult(res)
        if not isinstance(res,list):
            res=[res]
        for i in res:
            if not str(i) in self.diccres:
                self.diccres[str(i)]=True
                self.results.append(i)


    def next(self):
        while not self.results:
            self.getNewPage()

        if not self.results:
            raise StopIteration

        self.lastResult=self.results.pop()

        if not self.lastResult:
            return self.next()

        return self.lastResult


    def cleanString(self,res):
        res=PagerEngine.remultag.sub(" ",res)
        res=PagerEngine.retag.sub("",res)
        res=res.replace("&nbsp;"," ")
        res=res.replace("&amp;","&")
        res=res.strip()
        return res


    def getNewPage(self):

        if self.MoreResults==False:
            raise StopIteration

        if self.start==None:
            self.start=self.startIndex
        else:
            self.start+=self.increment

        url=self.url.replace("{query}",str(self.query))
        url=url.replace("{startvar}",str(self.start))

        request = Request(url)
        opener = build_opener()
        request.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080418 Ubuntu/7.10 (gutsy) Firefox/2.0.0.14')

        rawResponse=self.preProcess(opener.open(request).read())

        for i in re.findall(self.urlRegexp,rawResponse):
            self.addResult(i)

        if re.findall(self.nextRegexp,rawResponse):
            self.MoreResults=True
        else:
            self.MoreResults=False

    def getResult(self):
        try:
            return self.next()
        except:
            return None

    def getNResults(self,n):
        l=[]
        for i in range(n):
            try:
                l.append(self.next())
            except:
                break

        return l

    # Virtual functions, you can preprocess (html) and postprocess (each result)    
    def preProcess(self,raw):
        return raw

    def processResult (self,res):
        return self.cleanString(res)

########################################################
#Class Examples
######################################################

##GOOGLE##

class GoogleSearch(PagerEngine):
    def __init__(self,query):
        PagerEngine.__init__(self,query)

        self.url="http://www.google.com/search?q={query}&start={startvar}&num=100"

        self.urlRegexp="\"([^\"]+)\" class=l "
        self.nextRegexp=">Next<"
        self.increment=100

## BING ##

class BingSearch(PagerEngine):
    def __init__(self,query):
        PagerEngine.__init__(self,query)

        self.url="http://www.bing.com/search?q={query}&first={startvar}"

        self.urlRegexp="sb_tlst\"><h3><a href=\"([^\"]+)\" onmousedown"
        self.nextRegexp="\)\">Next</a></li>"

        self.startIndex=1
        self.increment=10

## YAHOO ##

class YahooSearch(PagerEngine):
    def __init__(self,query):
        PagerEngine.__init__(self,query)

        self.url="http://search.yahoo.com/search?p={query}&b={startvar}&ei=UTF-8&y=Search&xargs=0&pstart=0"

        self.urlRegexp="class=url>((?:[^<]|<[^/]|</[^s])+)</span>"
        self.nextRegexp=">Next &gt;"

    def processResult(self,res):
        res=self.cleanString(res)

        if "yahoo" in res:
            return None

        res=unquote(res)

        return res

############################################################
# Usage
#################################################

# Getting all google results for a search
for i in GoogleSearch("cooking recipes"):
    print i

# Getting first 5 results in a yahoo search
a=YahooSearch("cooking recipes")
print a.getNResults(5)
