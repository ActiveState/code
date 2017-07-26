class hippoFault ( Exception ): pass

class searchHippo:
    """
Python class able to return results from the XML interface at www.searchhippo.com

>>> from searchHippo import searchHippo
>>> hippo = searchHippo ( searchTerms = "bliss", requestSize = 5 )
>>> hippo.records ( 8 )
('GameDev.net - all your game development needs', 'Features Resources Community Directories More News Columns Contests Articles & Resources Books & Software For Beginners Forums GD Showcase IRC Chat Network Job Offers Member Search Hosted S...', 'http://208.148.122.26/r.php?i=7&u=http://www.gamedev.net/&q=bliss', 'http://www.gamedev.net/')
>>> hippo.records ( 9 )
('TOMPAINE.com - A Public Interest Journal', "Home | About Us | Contact Us | Submissions Search The Bush Administration's Dirty Little Secret Bush Policies Don't Protect Nuclear Material From Terrorist Theft by William Hartung The dirt...", 'http://208.148.122.26/r.php?i=8&u=http://www.tompaine.com/&q=bliss', 'http://www.tompaine.com/')

Each hippo record is returned as a four-tuple whose elements are a page title, a description of the page, a click-through URL
for the page and the URL to be displayed with the click-through URL.

The class uses a form of "semi-lazy" execution. That is, if record 'k' is already available then it is returned immediately 
without further action being taken. However, if record 'k' is unavailable then the class attempts to obtain the
records up to 'requestSize' records away from record 'k' from searchHippo, as well as record 'k' itself, if these records 
are not already available.
    """
    def __init__ ( self, searchTerms = None, requestSize = 50 ):
        if searchTerms == None:
            raise hippoFault, "searchHippo needs 'searchTerms'"
        self . _searchTerms = searchTerms
        self . requestSize = requestSize
        self . _records = { }
        self . parser = None
    def records ( self, num ):
        num = num - 1
        if num < 0:
            raise hippoFault, "searchHippo.records expects integer num > 0"
        if ( num + 1 ) in self . _records:
            return self . _records [ num + 1 ]
        else:
            half = self . requestSize / 2
            kLow = num
            while kLow > 0 and not ( kLow - 1 ) in self . _records and ( num - kLow ) < half:
                kLow -= 1
            half = ( self . requestSize + 1 ) / 2
            kHigh = num
            while not ( kHigh + 1 ) in self . _records and ( kHigh + 1 - num ) <= half:
                kHigh += 1
            reqsize = kHigh + 1 - kLow + self . requestSize
            if reqsize > self . requestSize: reqsize = self . requestSize
            self . _get ( kLow, reqsize )
            if ( num + 1 ) in self . _records:
                return self . _records [ num + 1 ]
            else:
                return None
    def _get ( self, startNumber, reqsize ):
        import pyRXP
        from urllib import urlopen

        hippoXML = urlopen ( "http://www.searchhippo.com/qxml.php?q=%s&c=%i&i=%i" % ( self . _searchTerms, self . requestSize, startNumber, ) ) . read ( )
        if self . parser == None: self. parser = pyRXP.Parser()
        tree = self . parser . parse ( hippoXML )
        self . _descend ( tree )
    def _descend ( self, fourTuple ):
        tagName, tagAttrs, content, unused = fourTuple
        if tagName == "RESULTS":
            pass
        elif tagName == "RECORD":
            global NUM
            NUM = tagAttrs [ 'NUM' ]
        elif tagName == "TITLE":
            global TITLE
            TITLE = content [ 0 ]
            return
        elif tagName == "DESCR":
            global DESCR
            DESCR = content [ 0 ]
            return
        elif tagName == "URL":
            global URL
            URL = content [ 0 ]
            return
        elif tagName == "DISPURL":
            global DISPURL
            DISPURL = content [ 0 ]
            return
        for item in content:
            try:
                self . _descend ( item )
            except:
                pass
        if tagName == "RECORD":
            self. _records [ int ( NUM ) ] = ( TITLE, DESCR, URL, DISPURL )
    def _get_searchTerms ( self ):
        return _searchTerms
    searchTerms = property ( None, _get_searchTerms, None, '' )

if __name__ == "__main__":
    hippo = searchHippo ( searchTerms = "snowman", requestSize = 5 )

    for i in xrange ( 10 ):
        item = hippo . records ( i + 1 )
        print "records item", i + 1, " is", item
