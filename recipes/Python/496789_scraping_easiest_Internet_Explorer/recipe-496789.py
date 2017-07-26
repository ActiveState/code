from win32com.client import Dispatch
from PyRSS2Gen import RSSItem, Guid
import ScrapeNFeed

class ContactPointEvents ( ScrapeNFeed . ScrapedFeed ) :    

    def HTML2RSS ( self, unused_headers, body ) :

        html = Dispatch ( 'htmlfile' ) 
        html . writeln ( body )
        items = [ ]
        count = 0
        for item in html . body . all :
            if item . tagName == 'UL' :
                count += 1
                if count == 4 :
                    break
        theUL = item . all
        for item in theUL :
            if item . tagName == 'LI' :
                title = item . childNodes [ 0 ] . innerText
                link = item . childNodes [ 0 ] . outerHTML
                if item . childNodes . length >= 2 :
                    description = item . innerText
                else :
                    description = ''
                items . append ( RSSItem ( title = title, description = description, link = link ) )
        self . addRSSItems ( items )

ContactPointEvents . load ( "New O'Reilly releases",
         'http://www.oreilly.com/catalog/new.html',
         "New O'Reillys",
         r'new.xml', r'new.pickle',
         managingEditor='wbell@vex.net (Bill Bell)')
